import argparse
import sys

from sf_utils import AUDIT_RENAME, load_sf_csv, rename_columns


def main() -> None:
    parser = argparse.ArgumentParser(description="Vista previa del export Screaming Frog.")
    parser.add_argument("--input", "-i", default="", help="CSV de SF (default: sf_html.csv)")
    args = parser.parse_args()

    df, input_path = load_sf_csv(args.input or None)
    df = rename_columns(df, AUDIT_RENAME)

    print(f"Archivo: {input_path}")
    print(f"Filas: {len(df)} | Columnas originales mapeadas: {len(df.columns)}")
    print()
    print("Columnas:")
    for col in df.columns:
        print(f"  - {col}")
    print()
    print(df.head())


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
