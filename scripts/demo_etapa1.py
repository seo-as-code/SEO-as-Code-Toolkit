"""Demo Etapa 1: extrae GSC + GA4 + CrUX + Screaming Frog a CSV."""
import argparse
import json
import os
import subprocess
import sys

import pandas as pd
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
DATA_RAW = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed")

GSC_SCRIPT = os.path.join(SCRIPTS_DIR, "gsc", "gsc_oauth.py")
GA4_SCRIPT = os.path.join(SCRIPTS_DIR, "ga4", "ga4_extract.py")
CRUX_SCRIPT = os.path.join(SCRIPTS_DIR, "crux", "crux_api_test.py")
SF_CLEAN_SCRIPT = os.path.join(SCRIPTS_DIR, "sf", "limpiar_sf.py")
SF_INPUT_CANDIDATES = ("sf_html.csv", "internos_html.csv")
SF_OUTPUT = os.path.join(DATA_PROCESSED, "sf_limpio.csv")
SF_AUDIT_OUTPUT = os.path.join(DATA_PROCESSED, "sf_audit.csv")


def find_sf_input() -> str | None:
    for name in SF_INPUT_CANDIDATES:
        path = os.path.join(DATA_RAW, name)
        if os.path.exists(path):
            return path
    sf_files = sorted(
        [f for f in os.listdir(DATA_RAW) if f.startswith("sf") and f.endswith(".csv")],
        key=lambda f: os.path.getmtime(os.path.join(DATA_RAW, f)),
        reverse=True,
    )
    return os.path.join(DATA_RAW, sf_files[0]) if sf_files else None


def run_script(path: str, label: str, cwd: str | None = None) -> bool:
    print(f"\n--- {label} ---")
    result = subprocess.run([sys.executable, path], cwd=cwd or BASE_DIR)
    ok = result.returncode == 0
    print(f"{'OK' if ok else 'FALLO'}: {label}")
    return ok


def summarize_csv(path: str, label: str) -> None:
    if not os.path.exists(path):
        print(f"  {label}: (no generado)")
        return
    df = pd.read_csv(path)
    print(f"  {label}: {len(df)} filas -> {path}")


def crux_status() -> str:
    sys.path.insert(0, SCRIPTS_DIR)
    from lib.site_config import site_origin  # noqa: E402

    key_file = os.path.join(SCRIPTS_DIR, "crux", "crux_key.txt")
    with open(key_file, "r", encoding="utf-8") as f:
        api_key = f.read().strip()

    url = f"https://chromeuxreport.googleapis.com/v1/records:queryRecord?key={api_key}"
    payload = {
        "origin": site_origin(),
        "metrics": ["largest_contentful_paint", "cumulative_layout_shift", "interaction_to_next_paint"],
    }
    response = requests.post(url, json=payload, timeout=30)
    data = response.json()
    if "error" in data:
        return f"sin datos CrUX ({data['error'].get('message', 'error')})"
    record = data.get("record", {})
    metrics = record.get("metrics", {})
    parts = []
    for name, label in [
        ("largest_contentful_paint", "LCP"),
        ("interaction_to_next_paint", "INP"),
        ("cumulative_layout_shift", "CLS"),
    ]:
        p75 = metrics.get(name, {}).get("percentiles", {}).get("p75")
        if p75 is not None:
            parts.append(f"{label} p75={p75}")
    return ", ".join(parts) if parts else "respuesta OK sin metricas"


def main() -> None:
    parser = argparse.ArgumentParser(description="Demo Etapa 1: GSC + GA4 + CrUX + SF")
    parser.add_argument("--skip-gsc", action="store_true", help="Saltar export GSC")
    parser.add_argument("--skip-ga4", action="store_true", help="Saltar export GA4")
    parser.add_argument("--skip-crux", action="store_true", help="Saltar test CrUX")
    parser.add_argument("--skip-sf", action="store_true", help="Saltar limpieza SF")
    args = parser.parse_args()

    print("=" * 50)
    print("  DEMO ETAPA 1 — SEO-as-Code")
    print("  GSC + GA4 + CrUX + Screaming Frog")
    print("=" * 50)

    results: dict[str, bool] = {}

    if not args.skip_gsc:
        results["GSC"] = run_script(GSC_SCRIPT, "Google Search Console", cwd=os.path.join(SCRIPTS_DIR, "gsc"))
    if not args.skip_ga4:
        results["GA4"] = run_script(GA4_SCRIPT, "Google Analytics 4")
    if not args.skip_crux:
        results["CrUX"] = run_script(CRUX_SCRIPT, "Chrome UX Report (test API)")
    if not args.skip_sf:
        sf_input = find_sf_input()
        if sf_input:
            results["SF"] = run_script(SF_CLEAN_SCRIPT, "Screaming Frog (limpiar crawl)")
        else:
            print("\n--- Screaming Frog ---")
            print("  AVISO: falta export en data/raw/ (sf_html.csv)")
            results["SF"] = False

    print("\n" + "=" * 50)
    print("  RESUMEN ETAPA 1")
    print("=" * 50)

    gsc_files = sorted(
        [f for f in os.listdir(DATA_RAW) if f.startswith("gsc_oauth") and f.endswith(".csv")],
        reverse=True,
    )
    if gsc_files:
        summarize_csv(os.path.join(DATA_RAW, gsc_files[0]), "GSC")
    summarize_csv(os.path.join(DATA_RAW, "ga4_last30days.csv"), "GA4")
    summarize_csv(SF_OUTPUT, "SF (limpio)")
    summarize_csv(SF_AUDIT_OUTPUT, "SF (audit)")

    if not args.skip_crux:
        print(f"  CrUX: {crux_status()}")

    print("\nFuentes:")
    for name, ok in results.items():
        print(f"  [{('OK' if ok else 'FALLO')}] {name}")

    print("\nSiguiente:")
    print("  Etapa 2 (enterprise): py .\\scripts\\maestro_analisis_enterprise.py --origin https://studiorethinkibiza.com")
    print("  Etapa 3 (AI):        cd ai-seo-toolkit && py .\\scripts\\orchestrator\\ai_seo_master.py --gsc RUTA_GSC")
    print("  Index Monitor:       cd proyecto_seo-index && .\\scripts\\run.ps1")


if __name__ == "__main__":
    main()
