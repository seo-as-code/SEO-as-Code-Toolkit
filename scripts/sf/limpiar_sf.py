import argparse
import sys

from sf_utils import (
    AUDIT_COLUMNS,
    AUDIT_RENAME,
    DATA_PROCESSED,
    LIMPIO_COLUMNS,
    filter_html,
    filter_limpio,
    load_sf_csv,
    rename_columns,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Procesa export Screaming Frog: sf_audit.csv (Tier 1+2) y sf_limpio.csv (on-page)."
    )
    parser.add_argument(
        "--input",
        "-i",
        default="",
        help="CSV de SF (default: data/raw/sf_html.csv o internos_html.csv)",
    )
    args = parser.parse_args()

    df, input_path = load_sf_csv(args.input or None)
    df = rename_columns(df, AUDIT_RENAME)

    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    audit_path = DATA_PROCESSED / "sf_audit.csv"
    audit_df = filter_html(df)
    audit_cols = [c for c in AUDIT_COLUMNS if c in audit_df.columns]
    audit_df = audit_df[audit_cols]
    audit_df.to_csv(audit_path, index=False, encoding="utf-8")

    limpio_path = DATA_PROCESSED / "sf_limpio.csv"
    limpio_df = filter_limpio(df)
    limpio_cols = [c for c in LIMPIO_COLUMNS if c in limpio_df.columns]
    limpio_df = limpio_df[limpio_cols]
    limpio_df.to_csv(limpio_path, index=False, encoding="utf-8")

    print(f"Entrada:  {input_path}")
    print(f"Filas raw: {len(df)} | audit (HTML): {len(audit_df)} | limpio (HTML 200 indexable): {len(limpio_df)}")
    print(f"Columnas audit: {len(audit_cols)} | limpio: {len(limpio_cols)}")
    print(f"Audit:  {audit_path}")
    print(f"Limpio: {limpio_path}")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
