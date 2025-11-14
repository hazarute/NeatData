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

    def __init__(self, custom_path: Optional[str] = None) -> None:
        self.logger = logging.getLogger("PipelineManager")
        self.custom_path = Path(custom_path or Path(__file__).parent / "custom")
        self.core_modules = {descriptor.key: descriptor for descriptor in load_core_modules()}
        self.custom_modules = self._discover_custom_modules()
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
