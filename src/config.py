from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.yaml"
ENV_PATH = ROOT / ".env"

def _load_env() -> None:
    """
    Load environment variables from .env into os.environ for THIS process.
    """    
    load_dotenv(dotenv_path=ENV_PATH)

def _load_yaml() -> Dict[str, Any]:
    """
    Load configuration from config.yaml file.
    """
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing config.yaml at: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
    if not isinstance(cfg, dict):
        raise RuntimeError("config.yaml did not parse into a dict")
    return cfg

def _get_env_required(name: str) -> str:
    """
    Get a required environment variable, raising an error if not found.
    """
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

# ---- Load once at import time (module singleton behaviour) ----
_load_env()
CFG: Dict[str, Any] = _load_yaml()

def get_datasource(name: str | None = None) -> Dict[str, Any]:
    """
    Return a datasource config dict with secrets resolved.

    If name is None, use runtime.datasource from config.yaml
    """
    ds_name = name or CFG.get("runtime", {}).get("datasource")
    if not ds_name:
        raise RuntimeError("No datasource specified. Set runtime.datasource in config.yaml")

    ds_all = CFG.get("api_datasource", {})
    if ds_name not in ds_all:
        raise RuntimeError(f"Datasource `{ds_name}` not found in api_datasources")

    ds = ds_all[ds_name]
    if not isinstance(ds, dict):
        raise RuntimeError(f"Datasource `{ds_name}` config must be a dict")

    # Resolve secret if configured
    env_key_name = ds.get("api_key_env")
    if env_key_name:
        api_key = _get_env_required(env_key_name)
        # Inject resolved key without mutating original dict
        ds = {**ds, "api_key": api_key}

    return ds

def get_cfg() -> Dict[str, Any]:
    """
    Return raw parsed YAML config (no secret injection).
    Useful for general parameters later.
    """
    return CFG