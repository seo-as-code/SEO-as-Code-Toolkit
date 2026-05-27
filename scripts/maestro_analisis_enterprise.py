import argparse
import os
import subprocess
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

GSC_ANALYZER = os.path.join(SCRIPTS_DIR, "gsc", "gsc_analyze_enterprise.py")
GA4_ANALYZER = os.path.join(SCRIPTS_DIR, "ga4", "ga4_analyze_enterprise.py")
CRUX_ANALYZER = os.path.join(SCRIPTS_DIR, "crux", "crux_analyze_enterprise.py")


def run_step(command: list[str], label: str) -> None:
    print(f"\n=== {label} ===")
    print(" ".join(command))
    result = subprocess.run(command)
    if result.returncode != 0:
        raise RuntimeError(f"Paso fallido: {label} (exit code {result.returncode})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Maestro enterprise para analisis SEO (GSC + GA4 + CrUX).")
    parser.add_argument("--gsc-input", default="", help="Ruta CSV GSC. Si vacio, usa el mas reciente.")
    parser.add_argument("--ga4-input", default=os.path.join(BASE_DIR, "data", "raw", "ga4_traffic_last30days.csv"))
    parser.add_argument("--origin", required=True, help="Origin para CrUX, ej: https://studiorethinkibiza.com")
    parser.add_argument("--crux-key-file", default=os.path.join(SCRIPTS_DIR, "crux", "crux_key.txt"))
    parser.add_argument("--min-impressions", type=int, default=300)
    parser.add_argument("--low-ctr-threshold", type=float, default=0.02)
    parser.add_argument("--position-floor", type=float, default=4.0)
    args = parser.parse_args()

    gsc_cmd = [
        sys.executable,
        GSC_ANALYZER,
        "--output-dir",
        os.path.join(BASE_DIR, "reports", "gsc"),
        "--min-impressions",
        str(args.min_impressions),
        "--low-ctr-threshold",
        str(args.low_ctr_threshold),
        "--position-floor",
        str(args.position_floor),
    ]
    if args.gsc_input:
        gsc_cmd.extend(["--input", args.gsc_input])

    ga4_cmd = [
        sys.executable,
        GA4_ANALYZER,
        "--input",
        args.ga4_input,
        "--output-dir",
        os.path.join(BASE_DIR, "reports", "ga4"),
    ]

    crux_cmd = [
        sys.executable,
        CRUX_ANALYZER,
        "--origin",
        args.origin,
        "--key-file",
        args.crux_key_file,
        "--output-dir",
        os.path.join(BASE_DIR, "reports", "crux"),
    ]

    run_step(gsc_cmd, "GSC analysis")
    run_step(ga4_cmd, "GA4 analysis")
    run_step(crux_cmd, "CrUX analysis")

    print("\nAnalisis enterprise completado.")
    print("Revisa las carpetas:")
    print(f"- {os.path.join(BASE_DIR, 'reports', 'gsc')}")
    print(f"- {os.path.join(BASE_DIR, 'reports', 'ga4')}")
    print(f"- {os.path.join(BASE_DIR, 'reports', 'crux')}")


if __name__ == "__main__":
    main()
