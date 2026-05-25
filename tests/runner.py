"""Load both rag_query engines as Python modules (folder names contain hyphens, so
importlib.util is the cleanest way to get them on the path) and expose a
single search(engine, query, mode, top_k) call. The model and DB handles are
cached inside each engine's module, so the second query is fast.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parent.parent
ENGINE_PATHS = {
    "sqlite": REPO_ROOT / "sqlite-rag" / "rag_query.py",
    "lance": REPO_ROOT / "lance-db-rag" / "rag_query.py",
}

_MODULE_CACHE: dict[str, ModuleType] = {}


def _load(engine: str) -> ModuleType:
    if engine in _MODULE_CACHE:
        return _MODULE_CACHE[engine]
    path = ENGINE_PATHS[engine]
    # The lance-db-rag query script does `from bge import BGE`, which only resolves
    # if its own folder is on sys.path. Add it before importing.
    folder = str(path.parent)
    if folder not in sys.path:
        sys.path.insert(0, folder)
    spec = importlib.util.spec_from_file_location(f"_engine_{engine}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {engine} engine from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _MODULE_CACHE[engine] = mod
    return mod


def search(engine: str, query: str, mode: str = "hybrid", top_k: int = 8) -> list[dict]:
    mod = _load(engine)
    return mod.search(query, mode=mode, top_k=top_k)


def engines() -> list[str]:
    return list(ENGINE_PATHS.keys())
