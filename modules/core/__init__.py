"""Core cleaning modules exposed by the NeatData pipeline.

Each module inside this package MUST expose two attributes:
- META: dict including key, name, description, defaults
- process(df, **kwargs): function returning a pandas DataFrame
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import Callable, Dict, List

@dataclass(frozen=True)
class ModuleDescriptor:
    key: str
    name: str
    description: str
    defaults: Dict
    process: Callable
    order: int = 0

_PACKAGE_ROOT = Path(__file__).parent


def load_core_modules() -> List[ModuleDescriptor]:
    descriptors: List[ModuleDescriptor] = []
    for module_path in sorted(_PACKAGE_ROOT.glob("*.py")):
        if module_path.name.startswith("_") or module_path.name == "__init__.py":
            continue
        module_name = module_path.stem
        module = import_module(f"modules.core.{module_name}")
        meta = getattr(module, "META", {})
        key = meta.get("key", module_name)
        name = meta.get("name", module_name.replace("_", " ").title())
        description = meta.get("description", "")
        defaults = meta.get("defaults", {})
        order = meta.get("order", 0)
        descriptors.append(
            ModuleDescriptor(
                key=key,
                name=name,
                description=description,
                defaults=defaults,
                process=getattr(module, "process"),
                order=order,
            )
        )
    return sorted(descriptors, key=lambda descriptor: descriptor.order)


__all__ = ["load_core_modules", "ModuleDescriptor"]
