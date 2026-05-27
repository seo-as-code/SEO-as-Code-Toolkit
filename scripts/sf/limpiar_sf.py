import pandas as pd

# Cargar CSV original
df = pd.read_csv(r"C:\Users\emami\proyecto_seo\data\raw\internos_todo.csv")

# Renombrar columnas de español → inglés para trabajar más fácil
df = df.rename(columns={
    "Dirección": "Address",
    "Tipo de contenido": "Content Type",
    "Código de respuesta": "Status Code",
    "Indexabilidad": "Indexability",
    "Título 1": "Title 1",
    "Meta description 1": "Meta Description 1",
    "Elemento de enlace canónico 1": "Canonical Link Element 1",
    "H1-1": "H1-1",
    "Recuento de palabras": "Word Count",
    "Tamaño (bytes)": "Size (Bytes)"
})

# Seleccionar solo columnas SEO importantes
columnas_seo = [
    "Address",
    "Status Code",
    "Content Type",
    "Indexability",
    "Title 1",
    "Meta Description 1",
    "Canonical Link Element 1",
    "H1-1",
    "Word Count",
    "Size (Bytes)"
]

df = df[columnas_seo]

# Filtrar solo HTML
df = df[df["Content Type"].str.contains("html", na=False)]

# Filtrar solo status 200
df = df[df["Status Code"] == 200]

# Filtrar solo indexables
df = df[df["Indexability"].str.contains("Indexable", na=False)]

# Guardar archivo limpio
output = r"C:\Users\emami\proyecto_seo\data\processed\sf_limpio.csv"
df.to_csv(output, index=False)

print("✔ Archivo limpio generado en:")
print(output)


