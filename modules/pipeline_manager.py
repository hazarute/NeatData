"""Dynamic pipeline manager with core/custom plugin discovery."""

from __future__ import annotations

import importlib.util
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import pandas as pd

from modules.core import ModuleDescriptor, load_core_modules


@dataclass
class PipelineStep:
    key: str
    name: str
    origin: str
    process: Any
    params: Dict[str, Any]


class PipelineManager:
    """Builds and executes a dataframe cleaning pipeline."""

    def __init__(self, custom_path: Optional[str] = None, selected_modules_list: Optional[Iterable[str]] = None) -> None:
        """Initialize PipelineManager.

        Args:
            custom_path: optional path to `modules/custom` directory.
            selected_modules_list: iterable of module keys or names selected by the GUI.
                If provided, `run_pipeline` will execute only the modules listed here.
        """
        self.logger = logging.getLogger("PipelineManager")
        self.custom_path = Path(custom_path or Path(__file__).parent / "custom")
        # load core descriptors keyed by descriptor.key
        self.core_modules = {descriptor.key: descriptor for descriptor in load_core_modules()}
        # discover custom descriptors
        self.custom_modules = self._discover_custom_modules()
        # list provided by GUI (module keys or display names)
        self.selected_modules_list: List[str] = list(selected_modules_list) if selected_modules_list is not None else []
        self.steps: List[PipelineStep] = []

    def available_core_modules(self) -> Dict[str, ModuleDescriptor]:
        return self.core_modules

    def available_custom_modules(self, refresh: bool = False) -> Dict[str, ModuleDescriptor]:
        if refresh:
            self.custom_modules = self._discover_custom_modules()
        return self.custom_modules

    def refresh_custom_modules(self) -> Dict[str, ModuleDescriptor]:
        self.custom_modules = self._discover_custom_modules()
        return self.custom_modules

    def build_pipeline(
        self,
        *,
        core_keys: Optional[Iterable[str]] = None,
        custom_keys: Optional[Iterable[str]] = None,
        param_overrides: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> None:
        """Reset pipeline steps based on requested modules."""

        param_overrides = param_overrides or {}
        steps: List[PipelineStep] = []
        # If a caller passes None for core_keys it indicates "use default";
        # to avoid implicitly running all core modules when the caller
        # explicitly provided an empty list (no selection), we distinguish
        # None vs empty list. Same for custom.
        core_iter = core_keys if core_keys is not None else self.core_modules.keys()
        custom_iter = custom_keys if custom_keys is not None else []

        for origin, keys, registry in (
            ("core", core_iter, self.core_modules),
            ("custom", custom_iter, self.available_custom_modules()),
        ):
            for key in keys:
                descriptor = registry.get(key)
                if not descriptor:
                    self.logger.warning("%s modülü bulunamadı: %s", origin.capitalize(), key)
                    continue
                params = {**descriptor.defaults, **param_overrides.get(key, {})}
                steps.append(
                    PipelineStep(
                        key=descriptor.key,
                        name=descriptor.name,
                        origin=origin,
                        process=descriptor.process,
                        params=params,
                    )
                )
        self.steps = steps

    def add_step(self, func, kwargs=None, *, key: Optional[str] = None, name: Optional[str] = None, origin: str = "manual") -> None:
        """Append an ad-hoc callable to the pipeline."""

        self.steps.append(
            PipelineStep(
                key=key or func.__name__,
                name=name or func.__name__,
                origin=origin,
                process=func,
                params=kwargs or {},
            )
        )

    def set_steps(self, steps: List[PipelineStep]) -> None:
        self.steps = steps

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("Pipeline %d adım ile başlatılıyor", len(self.steps))
        frame = df.copy()
        for index, step in enumerate(self.steps, start=1):
            self.logger.info("Adım %s/%s: %s", index, len(self.steps), step.name)
            try:
                frame = step.process(frame, **step.params)
            except Exception as exc:  # pylint: disable=broad-except
                raise RuntimeError(f"Pipeline adımı hata verdi ({step.key}): {exc}") from exc
        return frame

    def _find_descriptor(self, identifier: str) -> Optional[ModuleDescriptor]:
        """Find a ModuleDescriptor by key or name (case-insensitive).

        Returns the descriptor from core or custom registry, or None if not found.
        """
        if not identifier:
            return None
        ident = identifier.strip()
        # direct key match
        desc = self.core_modules.get(ident) or self.custom_modules.get(ident)
        if desc:
            return desc
        # case-insensitive key/name match
        lower = ident.lower()
        for d in list(self.core_modules.values()) + list(self.custom_modules.values()):
            if (getattr(d, "key", "").lower() == lower) or (getattr(d, "name", "").lower() == lower):
                return d
        return None

    def run_pipeline(self, df: pd.DataFrame) -> pd.DataFrame:
        """Run only the modules listed in `selected_modules_list`.

        Behavior:
        - If `selected_modules_list` is empty or None, the pipeline is a no-op and returns the input frame.
        - Each entry in `selected_modules_list` may be a module `key` or a human-friendly `name`.
        - Modules are executed in the order provided by `selected_modules_list`.
        """
        frame = df.copy()
        if not self.selected_modules_list:
            self.logger.info("Hiç modül seçilmedi; pipeline çalıştırılmıyor.")
            return frame

        # Ensure we have up-to-date custom modules
        self.refresh_custom_modules()

        for sel in self.selected_modules_list:
            descriptor = self._find_descriptor(sel)
            if not descriptor:
                self.logger.warning("Seçili modül bulunamadı: %s (atlandı)", sel)
                continue
            self.logger.info("Çalıştırılıyor: %s (%s)", descriptor.name, descriptor.key)
            params = getattr(descriptor, "defaults", {}) or {}
            try:
                frame = descriptor.process(frame, **params)
            except Exception as exc:  # pylint: disable=broad-except
                raise RuntimeError(f"Seçili modül '{descriptor.key}' çalışırken hata: {exc}") from exc

        return frame

    def _discover_custom_modules(self) -> Dict[str, ModuleDescriptor]:
        registry: Dict[str, ModuleDescriptor] = {}
        if not self.custom_path.exists():
            return registry
        for file in sorted(self.custom_path.glob("*.py")):
            if file.name.startswith("_"):
                continue
            module_name = f"modules.custom.{file.stem}"
            spec = importlib.util.spec_from_file_location(module_name, file)
            if not spec or not spec.loader:
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  # type: ignore[attr-defined]
            meta = getattr(module, "META", {})
            key = meta.get("key", file.stem)
            descriptor = ModuleDescriptor(
                key=key,
                name=meta.get("name", file.stem.replace("_", " ").title()),
                description=meta.get("description", "Özel eklenti"),
                defaults=meta.get("defaults", {}),
                process=getattr(module, "process"),
            )
            registry[key] = descriptor
        return registry
