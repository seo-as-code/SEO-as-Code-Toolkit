import os
import sys
import subprocess

# ============================
# CONFIGURACIÓN DE RUTAS
# ============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
GSC_DIR = os.path.join(SCRIPTS_DIR, "gsc")
GA4_DIR = os.path.join(SCRIPTS_DIR, "ga4")
CRUX_DIR = os.path.join(SCRIPTS_DIR, "crux")
SF_DIR = os.path.join(SCRIPTS_DIR, "sf")

CREDENTIALS_DIR = os.path.join(BASE_DIR, "Credentials")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DATA_DIR = os.path.join(BASE_DIR, "data")

# ============================
# FUNCIONES AUXILIARES
# ============================

def run_script(path):
    """Ejecuta un script Python externo."""
    if not os.path.exists(path):
        print(f"❌ ERROR: No se encontró el script: {path}")
        return
    
    print(f"\n▶ Ejecutando: {path}\n")
    subprocess.run([sys.executable, path])


# ============================
# MÓDULOS DEL MENÚ
# ============================

def modulo_gsc():
    print("\n=== GOOGLE SEARCH CONSOLE ===")
    print("1. Autenticación OAuth")
    print("2. Extraer datos GSC")
    print("3. Análisis básico")
    print("4. Análisis avanzado")
    print("5. Enviar sitemap")
    print("0. Volver")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        run_script(os.path.join(GSC_DIR, "gsc_oauth.py"))
    elif opcion == "2":
        run_script(os.path.join(GSC_DIR, "gsc_fetch.py"))
    elif opcion == "3":
        run_script(os.path.join(GSC_DIR, "analisis_gsc.py"))
    elif opcion == "4":
        print("\nIntroduce la ruta del archivo CSV a analizar:")
        file_path = input("Archivo: ")

        script_path = os.path.join(GSC_DIR, "analisis_gsc_pro.py")
        subprocess.run([sys.executable, script_path, "--file", file_path])
    elif opcion == "5":
        run_script(os.path.join(GSC_DIR, "enviar_sitemap.py"))
    elif opcion == "0":
        return
    else:
        print("❌ Opción no válida")


def modulo_ga4():
    print("\n=== GOOGLE ANALYTICS 4 ===")
    print("1. Autenticación OAuth")
    print("2. Extraer datos GA4")
    print("0. Volver")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        run_script(os.path.join(GA4_DIR, "ga4_oauth.py"))
    elif opcion == "2":
        run_script(os.path.join(GA4_DIR, "ga4_extract.py"))
    elif opcion == "0":
        return
    else:
        print("❌ Opción no válida")


def modulo_crux():
    print("\n=== CORE WEB VITALS (CrUX API) ===")
    print("1. Test API CrUX")
    print("0. Volver")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        run_script(os.path.join(CRUX_DIR, "crux_api_test.py"))
    elif opcion == "0":
        return
    else:
        print("❌ Opción no válida")


def modulo_sf():
    print("\n=== SCREAMING FROG ===")
    print("1. Leer CSV")
    print("2. Limpiar datos")
    print("0. Volver")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        run_script(os.path.join(SF_DIR, "leer_sf.py"))
    elif opcion == "2":
        run_script(os.path.join(SF_DIR, "limpiar_sf.py"))
    elif opcion == "0":
        return
    else:
        print("❌ Opción no válida")


# ============================
# MENÚ PRINCIPAL
# ============================

def main():
    while True:
        print("\n==============================")
        print("     SCRIPT MAESTRO SEO")
        print("==============================")
        print("1. Google Search Console")
        print("2. Google Analytics 4")
        print("3. Core Web Vitals (CrUX)")
        print("4. Screaming Frog")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            modulo_gsc()
        elif opcion == "2":
            modulo_ga4()
        elif opcion == "3":
            modulo_crux()
        elif opcion == "4":
            modulo_sf()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("❌ Opción no válida")


if __name__ == "__main__":
    main()
