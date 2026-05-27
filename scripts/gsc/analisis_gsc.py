import pandas as pd

# Cambia el nombre del archivo si tu CSV tiene otra fecha
FILE = "gsc_oauth_2026-04-26_2026-05-26.csv"

df = pd.read_csv(FILE)

print("\n=== TOP 10 CONSULTAS POR CLICS ===")
top_queries = df.groupby("query")["clicks"].sum().sort_values(ascending=False).head(10)
print(top_queries)

print("\n=== TOP 10 PÁGINAS POR CLICS ===")
top_pages = df.groupby("page")["clicks"].sum().sort_values(ascending=False).head(10)
print(top_pages)

print("\n=== OPORTUNIDADES SEO (muchas impresiones, pocos clics) ===")
oportunidades = df[(df["impressions"] > 200) & (df["clicks"] < 5)].sort_values("impressions", ascending=False).head(10)
print(oportunidades[["query", "page", "impressions", "clicks", "position"]])

print("\n=== CONSULTAS CON PEOR POSICIÓN (posición > 20) ===")
malas_posiciones = df[df["position"] > 20].sort_values("position", ascending=False).head(10)
print(malas_posiciones[["query", "page", "position", "impressions"]])

print("\n=== PÁGINAS CON CTR BAJO (CTR < 0.01) ===")
ctr_bajo = df[df["ctr"] < 0.01].sort_values("ctr").head(10)
print(ctr_bajo[["page", "query", "ctr", "impressions"]])
