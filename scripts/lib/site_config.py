import os

import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE_CONFIG_PATH = os.path.join(BASE_DIR, "config", "site.local.yaml")
SITE_CONFIG_EXAMPLE = os.path.join(BASE_DIR, "config", "site.local.yaml.example")


def load_site_config() -> dict:
    if not os.path.exists(SITE_CONFIG_PATH):
        raise FileNotFoundError(
            "No existe config/site.local.yaml. "
            f"Copia {SITE_CONFIG_EXAMPLE} a config/site.local.yaml y rellena tu sitio."
        )
    with open(SITE_CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def gsc_site_url(cfg: dict | None = None) -> str:
    data = cfg or load_site_config()
    site = data.get("gsc_site_url") or data.get("site", {}).get("gsc_site_url")
    if not site:
        raise ValueError("Define gsc_site_url en config/site.local.yaml")
    return site if site.endswith("/") else f"{site}/"


def site_origin(cfg: dict | None = None) -> str:
    data = cfg or load_site_config()
    origin = data.get("origin") or data.get("site", {}).get("origin")
    if not origin:
        raise ValueError("Define origin en config/site.local.yaml")
    return origin.rstrip("/")


def sitemap_url(cfg: dict | None = None) -> str:
    data = cfg or load_site_config()
    url = data.get("sitemap_url") or data.get("site", {}).get("sitemap_url")
    if not url:
        raise ValueError("Define sitemap_url en config/site.local.yaml")
    return url
