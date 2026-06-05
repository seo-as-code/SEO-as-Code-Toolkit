import argparse
import os
import sys
from datetime import datetime

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_INPUT = os.path.join(BASE_DIR, "data", "raw", "ga4_last30days.csv")
DEFAULT_OUTPUT = os.path.join(BASE_DIR, "reports", "ga4")
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))


def site_origin_safe() -> str:
    try:
        from lib.site_config import site_origin  # noqa: E402

        return site_origin()
    except Exception:
        return ""


def normalize_channel(source_medium: str) -> str:
    value = str(source_medium).lower()
    if "google / organic" in value or "bing / organic" in value or "yahoo / organic" in value:
        return "Organic Search"
    if "direct" in value:
        return "Direct"
    if "email" in value:
        return "Email"
    if "facebook" in value or "instagram" in value or "linkedin" in value or "t.co" in value or "ig /" in value:
        return "Social"
    if "cpc" in value or "ppc" in value or "paid" in value:
        return "Paid Search"
    if "referral" in value:
        return "Referral"
    return "Other"


def build_page_url(page_path: str, origin: str) -> str:
    path = str(page_path).strip()
    if not path or path == "nan":
        return ""
    if path.startswith("http"):
        return path
    if not origin:
        return path
    return f"{origin.rstrip('/')}{path if path.startswith('/') else '/' + path}"


def run_analysis(input_csv: str) -> dict:
    df = pd.read_csv(input_csv)
    expected_cols = {"date", "source_medium", "page_path", "sessions", "users", "pageviews"}
    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas en GA4: {sorted(missing)}")
    if df.empty:
        raise ValueError("El CSV de GA4 esta vacio.")

    origin = site_origin_safe()
    df["date"] = pd.to_datetime(df["date"].astype(str), format="%Y%m%d", errors="coerce")
    for col in ["sessions", "users", "pageviews"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    if "page_title" not in df.columns:
        df["page_title"] = ""
    else:
        df["page_title"] = df["page_title"].fillna("").astype(str)

    df["page_path"] = df["page_path"].fillna("").astype(str)
    df["channel_group"] = df["source_medium"].apply(normalize_channel)
    df["page_url"] = df["page_path"].apply(lambda p: build_page_url(p, origin))

    total_sessions = int(df["sessions"].sum())
    total_users = int(df["users"].sum())
    total_pageviews = int(df["pageviews"].sum())
    period_start = df["date"].min()
    period_end = df["date"].max()

    flow_keys = ["channel_group", "source_medium", "page_path", "page_url", "page_title"]

    # Dia a dia: cuando + de donde + a que URL
    traffic_flow_daily = (
        df.groupby(["date", *flow_keys], dropna=False)[["sessions", "users", "pageviews"]]
        .sum()
        .reset_index()
        .sort_values(["date", "sessions", "pageviews"], ascending=[False, False, False])
    )
    traffic_flow_daily["date"] = traffic_flow_daily["date"].dt.strftime("%Y-%m-%d")

    # Resumen del periodo completo (sin fecha)
    traffic_flow = (
        df.groupby(flow_keys, dropna=False)[["sessions", "users", "pageviews"]]
        .sum()
        .reset_index()
        .sort_values(["sessions", "pageviews"], ascending=False)
    )
    traffic_flow["sessions_share"] = (traffic_flow["sessions"] / max(total_sessions, 1)).round(4)

    landing_pages_daily = (
        df.groupby(["date", "page_path", "page_url", "page_title", "source_medium"], dropna=False)[
            ["sessions", "users", "pageviews"]
        ]
        .sum()
        .reset_index()
        .sort_values(["date", "sessions", "pageviews"], ascending=[False, False, False])
    )
    landing_pages_daily["date"] = landing_pages_daily["date"].dt.strftime("%Y-%m-%d")

    top_landing_pages = (
        df.groupby(["page_path", "page_url", "page_title"], dropna=False)[["sessions", "users", "pageviews"]]
        .sum()
        .reset_index()
        .sort_values(["sessions", "pageviews"], ascending=False)
    )
    top_landing_pages["sessions_share"] = (top_landing_pages["sessions"] / max(total_sessions, 1)).round(4)

    # Principal fuente de cada landing page
    source_by_page = (
        df.groupby(["page_path", "source_medium"], dropna=False)["sessions"]
        .sum()
        .reset_index()
        .sort_values(["page_path", "sessions"], ascending=[True, False])
    )
    top_source_per_page = source_by_page.groupby("page_path", as_index=False).first()
    top_source_per_page = top_source_per_page.rename(columns={"source_medium": "top_source_medium"})
    top_landing_pages = top_landing_pages.merge(
        top_source_per_page[["page_path", "top_source_medium"]], on="page_path", how="left"
    )

    channel_perf = (
        df.groupby("channel_group", dropna=False)[["sessions", "users", "pageviews"]]
        .sum()
        .sort_values("sessions", ascending=False)
        .reset_index()
    )
    channel_perf["sessions_share"] = (channel_perf["sessions"] / max(total_sessions, 1)).round(4)

    channel_daily = (
        df.groupby(["date", "channel_group"], dropna=False)[["sessions", "users", "pageviews"]]
        .sum()
        .reset_index()
        .sort_values(["date", "sessions"], ascending=[False, False])
    )
    channel_daily["date"] = channel_daily["date"].dt.strftime("%Y-%m-%d")

    source_perf = (
        df.groupby("source_medium", dropna=False)[["sessions", "users", "pageviews"]]
        .sum()
        .sort_values("sessions", ascending=False)
        .reset_index()
    )
    source_perf["sessions_share"] = (source_perf["sessions"] / max(total_sessions, 1)).round(4)

    source_daily = (
        df.groupby(["date", "source_medium"], dropna=False)[["sessions", "users", "pageviews"]]
        .sum()
        .reset_index()
        .sort_values(["date", "sessions"], ascending=[False, False])
    )
    source_daily["date"] = source_daily["date"].dt.strftime("%Y-%m-%d")

    daily = (
        df.groupby("date", dropna=False)[["sessions", "users", "pageviews"]]
        .sum()
        .sort_index()
        .reset_index()
    )
    daily["date"] = daily["date"].dt.strftime("%Y-%m-%d")
    daily["sessions_change_pct"] = daily["sessions"].pct_change().replace([pd.NA, pd.NaT], 0).fillna(0).round(4)

    return {
        "kpis": {
            "rows": int(len(df)),
            "period_start": period_start.strftime("%Y-%m-%d") if pd.notna(period_start) else "",
            "period_end": period_end.strftime("%Y-%m-%d") if pd.notna(period_end) else "",
            "total_sessions": total_sessions,
            "total_users": total_users,
            "total_pageviews": total_pageviews,
            "avg_pages_per_session": float((total_pageviews / total_sessions) if total_sessions else 0),
            "unique_landing_pages": int(df["page_path"].nunique()),
            "unique_sources": int(df["source_medium"].nunique()),
        },
        "traffic_flow_daily": traffic_flow_daily,
        "traffic_flow": traffic_flow,
        "landing_pages_daily": landing_pages_daily,
        "top_landing_pages": top_landing_pages,
        "channel_perf": channel_perf,
        "channel_daily": channel_daily,
        "source_perf": source_perf,
        "source_daily": source_daily,
        "daily": daily,
    }


def export_report(results: dict, input_csv: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    xlsx_path = os.path.join(output_dir, f"ga4_report_{ts}.xlsx")
    md_path = os.path.join(output_dir, f"ga4_executive_summary_{ts}.md")

    k = results["kpis"]
    kpis_df = pd.DataFrame(
        [
            {"metrica": "Input", "valor": input_csv},
            {"metrica": "Periodo inicio", "valor": k["period_start"]},
            {"metrica": "Periodo fin", "valor": k["period_end"]},
            {"metrica": "Filas analizadas", "valor": k["rows"]},
            {"metrica": "Sesiones totales", "valor": k["total_sessions"]},
            {"metrica": "Usuarios totales", "valor": k["total_users"]},
            {"metrica": "Pageviews totales", "valor": k["total_pageviews"]},
            {"metrica": "Paginas por sesion", "valor": round(k["avg_pages_per_session"], 2)},
            {"metrica": "Landing pages unicas", "valor": k["unique_landing_pages"]},
            {"metrica": "Fuentes unicas", "valor": k["unique_sources"]},
        ]
    )

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        kpis_df.to_excel(writer, sheet_name="KPIs", index=False)
        results["traffic_flow_daily"].to_excel(writer, sheet_name="Origen y destino", index=False)
        results["landing_pages_daily"].to_excel(writer, sheet_name="Landing pages por dia", index=False)
        results["traffic_flow"].to_excel(writer, sheet_name="Resumen periodo", index=False)
        results["top_landing_pages"].to_excel(writer, sheet_name="Top landing pages", index=False)
        results["channel_daily"].to_excel(writer, sheet_name="Canales por dia", index=False)
        results["channel_perf"].to_excel(writer, sheet_name="Canales", index=False)
        results["source_daily"].to_excel(writer, sheet_name="Fuentes por dia", index=False)
        results["source_perf"].to_excel(writer, sheet_name="Fuentes", index=False)
        results["daily"].to_excel(writer, sheet_name="Tendencia diaria", index=False)

    top_flow = results["traffic_flow_daily"].head(5)
    flow_lines = []
    for _, row in top_flow.iterrows():
        dest = row["page_url"] or row["page_path"]
        flow_lines.append(
            f"- **{row['date']}** | {row['source_medium']} -> `{dest}` — {int(row['sessions'])} sesiones"
        )

    summary = [
        "# GA4 Enterprise Summary",
        "",
        f"- Input: `{input_csv}`",
        f"- Periodo: **{k['period_start']}** a **{k['period_end']}**",
        f"- Sesiones: **{k['total_sessions']}** | Usuarios: **{k['total_users']}** | Pageviews: **{k['total_pageviews']}**",
        f"- Landing pages unicas: **{k['unique_landing_pages']}** | Fuentes: **{k['unique_sources']}**",
        "",
        "## Archivo unico",
        f"- `{xlsx_path}`",
        "",
        "### Hojas",
        "- **Origen y destino** — fecha + fuente + URL (cuando, de donde y a donde)",
        "- **Landing pages por dia** — fecha + pagina + fuente",
        "- **Resumen periodo** — totales 30 dias sin desglose diario",
        "- **Canales / Fuentes por dia** — evolucion diaria por canal y source/medium",
        "- **Tendencia diaria** — totales del sitio por dia",
        "",
        "## Top 5 flujos recientes (fecha + origen -> destino)",
        *flow_lines,
    ]
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary) + "\n")

    print(f"[GA4] Summary: {md_path}")
    print(f"[GA4] Report: {xlsx_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Enterprise analyzer for GA4 exports.")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to GA4 CSV export.")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT, help="Output directory.")
    args = parser.parse_args()

    results = run_analysis(args.input)
    export_report(results, input_csv=args.input, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
