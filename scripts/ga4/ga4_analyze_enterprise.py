import argparse
import os
from datetime import datetime

import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_INPUT = os.path.join(BASE_DIR, "data", "raw", "ga4_traffic_last30days.csv")
DEFAULT_OUTPUT = os.path.join(BASE_DIR, "reports", "ga4")


def normalize_channel(source_medium: str) -> str:
    value = str(source_medium).lower()
    if "google / organic" in value or "bing / organic" in value or "yahoo / organic" in value:
        return "Organic Search"
    if "direct" in value:
        return "Direct"
    if "email" in value:
        return "Email"
    if "facebook" in value or "instagram" in value or "linkedin" in value or "t.co" in value:
        return "Social"
    if "cpc" in value or "ppc" in value or "paid" in value:
        return "Paid Search"
    if "referral" in value:
        return "Referral"
    return "Other"


def run_analysis(input_csv: str) -> dict:
    df = pd.read_csv(input_csv)
    expected_cols = {"date", "source_medium", "sessions", "users", "pageviews"}
    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas en GA4: {sorted(missing)}")
    if df.empty:
        raise ValueError("El CSV de GA4 esta vacio.")

    df["date"] = pd.to_datetime(df["date"].astype(str), format="%Y%m%d", errors="coerce")
    for col in ["sessions", "users", "pageviews"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    df["channel_group"] = df["source_medium"].apply(normalize_channel)
    df["pages_per_session"] = (df["pageviews"] / df["sessions"].replace(0, pd.NA)).fillna(0)
    df["sessions_per_user"] = (df["sessions"] / df["users"].replace(0, pd.NA)).fillna(0)

    total_sessions = int(df["sessions"].sum())
    total_users = int(df["users"].sum())
    total_pageviews = int(df["pageviews"].sum())

    channel_perf = (
        df.groupby("channel_group", dropna=False)[["sessions", "users", "pageviews"]]
        .sum()
        .sort_values("sessions", ascending=False)
        .reset_index()
    )
    channel_perf["sessions_share"] = (channel_perf["sessions"] / max(total_sessions, 1)).round(4)

    source_perf = (
        df.groupby("source_medium", dropna=False)[["sessions", "users", "pageviews"]]
        .sum()
        .sort_values("sessions", ascending=False)
        .head(50)
        .reset_index()
    )

    daily = (
        df.groupby("date", dropna=False)[["sessions", "users", "pageviews"]]
        .sum()
        .sort_index()
        .reset_index()
    )
    daily["sessions_change_pct"] = daily["sessions"].pct_change().replace([pd.NA, pd.NaT], 0).fillna(0)

    return {
        "kpis": {
            "rows": int(len(df)),
            "total_sessions": total_sessions,
            "total_users": total_users,
            "total_pageviews": total_pageviews,
            "avg_pages_per_session": float((total_pageviews / total_sessions) if total_sessions else 0),
        },
        "channel_perf": channel_perf,
        "source_perf": source_perf,
        "daily": daily,
    }


def export_report(results: dict, input_csv: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    channel_path = os.path.join(output_dir, f"ga4_channels_{ts}.csv")
    source_path = os.path.join(output_dir, f"ga4_sources_{ts}.csv")
    daily_path = os.path.join(output_dir, f"ga4_daily_{ts}.csv")
    md_path = os.path.join(output_dir, f"ga4_executive_summary_{ts}.md")

    results["channel_perf"].to_csv(channel_path, index=False, encoding="utf-8")
    results["source_perf"].to_csv(source_path, index=False, encoding="utf-8")
    results["daily"].to_csv(daily_path, index=False, encoding="utf-8")

    k = results["kpis"]
    lines = [
        "# GA4 Enterprise Summary",
        "",
        f"- Input: `{input_csv}`",
        f"- Rows analyzed: **{k['rows']}**",
        f"- Sessions: **{k['total_sessions']}**",
        f"- Users: **{k['total_users']}**",
        f"- Pageviews: **{k['total_pageviews']}**",
        f"- Pages per session: **{k['avg_pages_per_session']:.2f}**",
        "",
        "## Files generated",
        f"- `{channel_path}`",
        f"- `{source_path}`",
        f"- `{daily_path}`",
    ]
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[GA4] Summary: {md_path}")
    print(f"[GA4] Channels: {channel_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Enterprise analyzer for GA4 exports.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to GA4 CSV export.")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT, help="Output directory.")
    args = parser.parse_args()

    results = run_analysis(args.input)
    export_report(results, input_csv=args.input, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
