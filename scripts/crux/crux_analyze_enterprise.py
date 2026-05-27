import argparse
import json
import os
from datetime import datetime

import pandas as pd
import requests


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_OUTPUT = os.path.join(BASE_DIR, "reports", "crux")
DEFAULT_KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crux_key.txt")


def extract_metric(metrics: dict, key: str) -> dict:
    payload = metrics.get(key, {})
    percentile = payload.get("percentiles", {}).get("p75")
    histogram = payload.get("histogram", [])
    good = histogram[0].get("density", 0) if len(histogram) > 0 else 0
    needs = histogram[1].get("density", 0) if len(histogram) > 1 else 0
    poor = histogram[2].get("density", 0) if len(histogram) > 2 else 0
    return {
        "metric": key,
        "p75": percentile,
        "good_density": good,
        "needs_improvement_density": needs,
        "poor_density": poor,
    }


def pass_status(metric: str, p75_value: float) -> str:
    thresholds = {
        "largest_contentful_paint": 2500,
        "interaction_to_next_paint": 200,
        "cumulative_layout_shift": 0.1,
    }
    threshold = thresholds.get(metric)
    if threshold is None or p75_value is None:
        return "unknown"
    return "pass" if p75_value <= threshold else "fail"


def query_crux(origin: str, key_file: str) -> dict:
    if not os.path.exists(key_file):
        raise FileNotFoundError(f"No existe la API key de CrUX: {key_file}")
    with open(key_file, "r", encoding="utf-8") as f:
        api_key = f.read().strip()

    url = f"https://chromeuxreport.googleapis.com/v1/records:queryRecord?key={api_key}"
    payload = {
        "origin": origin,
        "metrics": [
            "largest_contentful_paint",
            "cumulative_layout_shift",
            "interaction_to_next_paint",
        ],
    }
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()


def analyze(payload: dict) -> tuple[pd.DataFrame, dict]:
    record = payload.get("record", {})
    metrics = record.get("metrics", {})
    rows = [
        extract_metric(metrics, "largest_contentful_paint"),
        extract_metric(metrics, "interaction_to_next_paint"),
        extract_metric(metrics, "cumulative_layout_shift"),
    ]
    df = pd.DataFrame(rows)
    df["status"] = df.apply(lambda r: pass_status(r["metric"], r["p75"]), axis=1)

    summary = {
        "origin": record.get("key", {}).get("origin"),
        "collection_period": record.get("collectionPeriod", {}),
        "pass_rate": float((df["status"] == "pass").sum() / max(len(df), 1)),
    }
    return df, summary


def export(df: pd.DataFrame, summary: dict, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(output_dir, f"crux_vitals_{ts}.csv")
    md_path = os.path.join(output_dir, f"crux_executive_summary_{ts}.md")

    df.to_csv(csv_path, index=False, encoding="utf-8")

    lines = [
        "# CrUX Enterprise Summary",
        "",
        f"- Origin: `{summary.get('origin')}`",
        f"- Vitals passing rate: **{summary.get('pass_rate', 0):.0%}**",
        "",
        "## Files generated",
        f"- `{csv_path}`",
    ]
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[CrUX] Summary: {md_path}")
    print(f"[CrUX] Vitals table: {csv_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Enterprise CrUX analyzer from API.")
    parser.add_argument("--origin", required=True, help="Origin to query (e.g. https://example.com)")
    parser.add_argument("--key-file", default=DEFAULT_KEY_FILE, help="Path to crux_key.txt")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT, help="Output directory")
    args = parser.parse_args()

    payload = query_crux(origin=args.origin, key_file=args.key_file)
    df, summary = analyze(payload)
    export(df, summary, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
