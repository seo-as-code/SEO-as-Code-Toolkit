import argparse
import glob
import os
from datetime import datetime

import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
REPORT_DIR = os.path.join(BASE_DIR, "reports", "gsc")


def latest_gsc_file() -> str:
    patterns = [
        os.path.join(RAW_DIR, "gsc_*.csv"),
        os.path.join(BASE_DIR, "gsc_*.csv"),
    ]
    candidates = []
    for pattern in patterns:
        candidates.extend(glob.glob(pattern))
    if not candidates:
        raise FileNotFoundError("No se encontro ningun CSV GSC (gsc_*.csv)")
    return max(candidates, key=os.path.getmtime)


def safe_div(num: float, den: float) -> float:
    if den == 0:
        return 0.0
    return num / den


def run_analysis(input_csv: str, min_impressions: int, low_ctr_threshold: float, pos_floor: float) -> dict:
    df = pd.read_csv(input_csv)
    expected_cols = {"page", "query", "clicks", "impressions", "ctr", "position"}
    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas en GSC: {sorted(missing)}")
    if df.empty:
        raise ValueError("El CSV de GSC esta vacio.")

    for col in ["clicks", "impressions", "ctr", "position"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    total_clicks = float(df["clicks"].sum())
    total_impressions = float(df["impressions"].sum())
    weighted_ctr = safe_div(total_clicks, total_impressions)
    weighted_position = safe_div((df["position"] * df["impressions"]).sum(), total_impressions)

    top_queries = (
        df.groupby("query", dropna=False)[["clicks", "impressions"]]
        .sum()
        .assign(ctr=lambda x: x["clicks"] / x["impressions"].replace(0, pd.NA))
        .fillna(0)
        .sort_values("clicks", ascending=False)
        .head(25)
        .reset_index()
    )

    top_pages = (
        df.groupby("page", dropna=False)[["clicks", "impressions"]]
        .sum()
        .assign(ctr=lambda x: x["clicks"] / x["impressions"].replace(0, pd.NA))
        .fillna(0)
        .sort_values("clicks", ascending=False)
        .head(25)
        .reset_index()
    )

    opportunities = (
        df[
            (df["impressions"] >= min_impressions)
            & (df["ctr"] <= low_ctr_threshold)
            & (df["position"] >= pos_floor)
            & (df["position"] <= 20)
        ]
        .sort_values(["impressions", "position"], ascending=[False, True])
        .head(200)
        .copy()
    )

    cannibalization = (
        df.groupby("query", dropna=False)
        .agg(
            pages=("page", "nunique"),
            clicks=("clicks", "sum"),
            impressions=("impressions", "sum"),
            best_position=("position", "min"),
        )
        .query("pages > 1")
        .sort_values(["pages", "impressions"], ascending=[False, False])
        .head(200)
        .reset_index()
    )

    return {
        "df": df,
        "top_queries": top_queries,
        "top_pages": top_pages,
        "opportunities": opportunities,
        "cannibalization": cannibalization,
        "kpis": {
            "rows": int(len(df)),
            "total_clicks": int(total_clicks),
            "total_impressions": int(total_impressions),
            "weighted_ctr": weighted_ctr,
            "weighted_position": weighted_position,
        },
    }


def export_report(results: dict, input_csv: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    q_path = os.path.join(output_dir, f"gsc_top_queries_{ts}.csv")
    p_path = os.path.join(output_dir, f"gsc_top_pages_{ts}.csv")
    o_path = os.path.join(output_dir, f"gsc_opportunities_{ts}.csv")
    c_path = os.path.join(output_dir, f"gsc_cannibalization_{ts}.csv")
    md_path = os.path.join(output_dir, f"gsc_executive_summary_{ts}.md")

    results["top_queries"].to_csv(q_path, index=False, encoding="utf-8")
    results["top_pages"].to_csv(p_path, index=False, encoding="utf-8")
    results["opportunities"].to_csv(o_path, index=False, encoding="utf-8")
    results["cannibalization"].to_csv(c_path, index=False, encoding="utf-8")

    k = results["kpis"]
    summary = [
        "# GSC Enterprise Summary",
        "",
        f"- Input: `{input_csv}`",
        f"- Rows analyzed: **{k['rows']}**",
        f"- Total clicks: **{k['total_clicks']}**",
        f"- Total impressions: **{k['total_impressions']}**",
        f"- Weighted CTR: **{k['weighted_ctr']:.2%}**",
        f"- Weighted avg position: **{k['weighted_position']:.2f}**",
        "",
        "## Files generated",
        f"- `{q_path}`",
        f"- `{p_path}`",
        f"- `{o_path}`",
        f"- `{c_path}`",
    ]
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary) + "\n")

    print(f"[GSC] Summary: {md_path}")
    print(f"[GSC] Top queries: {q_path}")
    print(f"[GSC] Opportunities: {o_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Enterprise analyzer for GSC exports.")
    parser.add_argument("--input", default="", help="Path to GSC CSV export.")
    parser.add_argument("--output-dir", default=REPORT_DIR, help="Output directory for reports.")
    parser.add_argument("--min-impressions", type=int, default=300, help="Minimum impressions filter.")
    parser.add_argument("--low-ctr-threshold", type=float, default=0.02, help="Low CTR threshold.")
    parser.add_argument("--position-floor", type=float, default=4.0, help="Minimum position for opportunities.")
    args = parser.parse_args()

    input_csv = args.input or latest_gsc_file()
    results = run_analysis(
        input_csv=input_csv,
        min_impressions=args.min_impressions,
        low_ctr_threshold=args.low_ctr_threshold,
        pos_floor=args.position_floor,
    )
    export_report(results, input_csv=input_csv, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
