import os
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_CSV = os.path.join(BASE_DIR, "data", "raw", "ga4_traffic_last30days.csv")
OUTPUT_TXT = os.path.join(BASE_DIR, "data", "raw", "ga4_traffic_last30days_analysis.txt")


def analyze_ga4(csv_path: str = INPUT_CSV, output_path: str = OUTPUT_TXT) -> str:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No existe el archivo de entrada: {csv_path}")

    df = pd.read_csv(csv_path)
    if df.empty:
        raise ValueError("El CSV existe, pero no contiene filas.")

    df["date"] = pd.to_datetime(df["date"].astype(str), format="%Y%m%d", errors="coerce")
    for col in ["sessions", "users", "pageviews"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    total_sessions = int(df["sessions"].sum())
    total_users = int(df["users"].sum())
    total_pageviews = int(df["pageviews"].sum())

    # Top 5 sources by sessions
    top_sources = (
        df.groupby("source_medium", dropna=False)[["sessions", "users", "pageviews"]]
        .sum()
        .sort_values("sessions", ascending=False)
        .head(5)
    )

    # Daily trend
    daily = (
        df.groupby("date", dropna=False)[["sessions", "users", "pageviews"]]
        .sum()
        .sort_index()
    )

    lines = [
        "GA4 ANALYSIS - LAST EXPORT",
        "==========================",
        f"Input file: {csv_path}",
        "",
        "Global totals",
        f"- Sessions: {total_sessions}",
        f"- Users: {total_users}",
        f"- Pageviews: {total_pageviews}",
        "",
        "Top 5 source / medium by sessions",
    ]

    if top_sources.empty:
        lines.append("- No source data available")
    else:
        for source, row in top_sources.iterrows():
            lines.append(
                f"- {source}: sessions={int(row['sessions'])}, users={int(row['users'])}, pageviews={int(row['pageviews'])}"
            )

    lines.append("")
    lines.append("Daily trend")
    if daily.empty:
        lines.append("- No daily data available")
    else:
        for idx, row in daily.iterrows():
            date_label = "NaT" if pd.isna(idx) else idx.strftime("%Y-%m-%d")
            lines.append(
                f"- {date_label}: sessions={int(row['sessions'])}, users={int(row['users'])}, pageviews={int(row['pageviews'])}"
            )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Analysis exported: {output_path}")
    return output_path


if __name__ == "__main__":
    analyze_ga4()
