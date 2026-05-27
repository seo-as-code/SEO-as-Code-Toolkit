import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Análisis SEO de datos GSC")
parser.add_argument("--file", required=True, help="Archivo CSV de GSC")
parser.add_argument("--limit", type=int, default=20, help="Número de resultados a mostrar")
parser.add_argument("--min_impressions", type=int, default=500, help="Impresiones mínimas para oportunidades SEO")
parser.add_argument("--max_clicks", type=int, default=10, help="Clics máximos para oportunidades SEO")

args = parser.parse_args()

df = pd.read_csv(args.file)

print("\n=== TOP QUERIES ===")
print(df.groupby("query")["clicks"].sum().sort_values(ascending=False).head(args.limit))

print("\n=== TOP PAGES ===")
print(df.groupby("page")["clicks"].sum().sort_values(ascending=False).head(args.limit))

print("\n=== OPORTUNIDADES SEO ===")
oportunidades = df[(df["impressions"] > args.min_impressions) & (df["clicks"] < args.max_clicks)]
print(oportunidades.head(args.limit))

print("\n=== CANIBALIZACIÓN ===")
canibal = df.groupby("query")["page"].nunique()
print(canibal[canibal > 1].sort_values(ascending=False).head(args.limit))
