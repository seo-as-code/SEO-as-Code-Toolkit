import os
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"

DEFAULT_INPUT_NAMES = ("sf_html.csv", "internos_html.csv")

# Tier 1 — imprescindibles
TIER1_RENAME = {
    "Dirección": "Address",
    "Tipo de contenido": "Content Type",
    "Código de respuesta": "Status Code",
    "Respuesta": "Response",
    "Indexabilidad": "Indexability",
    "Estado de indexabilidad": "Indexability Status",
    "Título 1": "Title 1",
    "Longitud del título 1": "Title 1 Length",
    "Meta description 1": "Meta Description 1",
    "Longitud de la meta description 1": "Meta Description 1 Length",
    "H1-1": "H1-1",
    "Elemento de enlace canónico 1": "Canonical Link Element 1",
    "Meta robots 1": "Meta Robots 1",
    "X-Robots-Tag 1": "X-Robots-Tag 1",
    "Recuento de palabras": "Word Count",
    "Nivel de profundidad": "Crawl Depth",
    "Enlaces internos": "Inlinks",
    "URL de redirección": "Redirect URL",
    "Tipo de redirección": "Redirect Type",
}

# Tier 2 — auditoría técnica
TIER2_RENAME = {
    "Semiduplicados (N.º)": "Near Duplicates",
    "Coincidencia de similitud más cercana": "Closest Similarity Match",
    "Tiempo de respuesta": "Response Time",
    "Tamaño (bytes)": "Size (Bytes)",
    "Transferido (bytes)": "Transferred (Bytes)",
    "H1-2": "H1-2",
    "H2-1": "H2-1",
    "H2-2": "H2-2",
    "Enlaces salientes externos": "External Outlinks",
    "Versión HTTP": "HTTP Version",
    "Last Modified": "Last Modified",
}

AUDIT_RENAME = {**TIER1_RENAME, **TIER2_RENAME}

AUDIT_COLUMNS = list(AUDIT_RENAME.values())

# Tier 1 + lo mejor de Tier 2 para análisis on-page rápido
LIMPIO_COLUMNS = [
    "Address",
    "Status Code",
    "Content Type",
    "Indexability",
    "Indexability Status",
    "Title 1",
    "Title 1 Length",
    "Meta Description 1",
    "Meta Description 1 Length",
    "H1-1",
    "H2-1",
    "Canonical Link Element 1",
    "Meta Robots 1",
    "X-Robots-Tag 1",
    "Word Count",
    "Crawl Depth",
    "Inlinks",
    "Response Time",
    "Size (Bytes)",
    "Transferred (Bytes)",
    "Near Duplicates",
    "Closest Similarity Match",
    "Redirect URL",
    "Redirect Type",
    "HTTP Version",
    "Last Modified",
]


def resolve_input(explicit: str | None = None) -> Path:
    if explicit:
        path = Path(explicit)
        if not path.is_absolute():
            path = BASE_DIR / path
        if not path.exists():
            raise FileNotFoundError(f"No existe el CSV de Screaming Frog: {path}")
        return path

    for name in DEFAULT_INPUT_NAMES:
        candidate = DATA_RAW / name
        if candidate.exists():
            return candidate

    sf_files = sorted(DATA_RAW.glob("sf*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if sf_files:
        return sf_files[0]

    searched = ", ".join(str(DATA_RAW / n) for n in DEFAULT_INPUT_NAMES)
    raise FileNotFoundError(
        f"No se encontro export de Screaming Frog en data/raw.\n"
        f"Buscado: {searched}\n"
        "Exporta el crawl como sf_html.csv en data/raw/"
    )


def load_sf_csv(path: Path | str | None = None) -> tuple[pd.DataFrame, Path]:
    input_path = resolve_input(str(path) if path else None)
    df = pd.read_csv(input_path, encoding="utf-8")
    return df, input_path


def rename_columns(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    present = {src: dst for src, dst in mapping.items() if src in df.columns}
    missing = [src for src in mapping if src not in df.columns]
    if missing:
        print(f"AVISO: columnas no encontradas en el CSV ({len(missing)}): {', '.join(missing[:5])}"
              + ("..." if len(missing) > 5 else ""))
    return df.rename(columns=present)


def filter_html(df: pd.DataFrame) -> pd.DataFrame:
    if "Content Type" not in df.columns:
        return df
    return df[df["Content Type"].astype(str).str.contains("html", case=False, na=False)]


def filter_limpio(df: pd.DataFrame) -> pd.DataFrame:
    out = filter_html(df)
    if "Status Code" in out.columns:
        out = out[out["Status Code"] == 200]
    if "Indexability" in out.columns:
        out = out[out["Indexability"].astype(str).str.contains("Indexable", na=False)]
    return out
