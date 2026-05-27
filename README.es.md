# SEO as Code Toolkit

> **Idiomas:** [English](README.md) | [Español](README.es.md)

Sistema SEO automatizado para extraer, analizar y reportar datos de:

- Google Search Console (GSC)
- Google Analytics 4 (GA4)
- Chrome UX Report (CrUX)
- (Base de trabajo para Screaming Frog)

Este repositorio implementa un enfoque **SEO-as-Code**: procesos repetibles, trazables con Git, y listos para ejecución operativa en equipos.

## Qué resolvimos

- Estructura de proyecto clara por fuente de datos (`scripts/gsc`, `scripts/ga4`, `scripts/crux`).
- Scripts de análisis enterprise por canal.
- Script maestro para lanzar análisis end-to-end.
- Carpeta de `reports` organizada por fuente.
- Comandos listos para ejecución desde terminal (`reports/**/code`).
- Control de versiones con Git + GitHub.
- Protección de secretos y ficheros sensibles via `.gitignore`.

## Arquitectura del proyecto

```text
proyecto_seo/
  scripts/
    maestro_analisis_enterprise.py
    gsc/
      gsc_fetch.py
      gsc_oauth.py
      gsc_analyze_enterprise.py
    ga4/
      ga4_oauth.py
      ga4_extract.py
      ga4_analyze_enterprise.py
    crux/
      crux_api_test.py
      crux_analyze_enterprise.py
    sf/
      leer_sf.py
      limpiar_sf.py
  data/
    raw/
    processed/
  reports/
    gsc/
    ga4/
    crux/
    code/
  .gitignore
```

## Scripts clave

### Maestro (todo en uno)

- `scripts/maestro_analisis_enterprise.py`
- Ejecuta en secuencia: GSC + GA4 + CrUX.
- Centraliza parámetros de negocio para umbrales y origen.

Ejemplo:

```bash
python scripts/maestro_analisis_enterprise.py --origin "https://studiorethinkibiza.com"
```

### GSC Enterprise

- `scripts/gsc/gsc_analyze_enterprise.py`
- KPIs: clicks, impressions, CTR ponderado, posición ponderada.
- Análisis: top queries, top pages, oportunidades SEO, canibalización.
- Salida: CSV + resumen ejecutivo en `reports/gsc/`.

Ejemplo:

```bash
python scripts/gsc/gsc_analyze_enterprise.py --min-impressions 500 --low-ctr-threshold 0.02 --position-floor 4
```

### GA4 Enterprise

- `scripts/ga4/ga4_extract.py` para extracción.
- `scripts/ga4/ga4_analyze_enterprise.py` para análisis.
- KPIs: sessions, users, pageviews, pages/session.
- Análisis: performance por canal, top source/medium, tendencia diaria.
- Salida: CSV + resumen ejecutivo en `reports/ga4/`.

Ejemplo:

```bash
python scripts/ga4/ga4_analyze_enterprise.py --input "C:\Users\emami\proyecto_seo\data\raw\ga4_traffic_last30days.csv"
```

### CrUX Enterprise

- `scripts/crux/crux_analyze_enterprise.py`
- Consulta API CrUX por origin.
- Analiza Core Web Vitals: LCP, INP, CLS (p75 y distribución).
- Evalúa pass/fail por umbrales oficiales.
- Salida: CSV + resumen ejecutivo en `reports/crux/`.

Ejemplo:

```bash
python scripts/crux/crux_analyze_enterprise.py --origin "https://studiorethinkibiza.com"
```

## Cómo ejecutar rápido (copy/paste)

Se incluyen comandos preparados en:

- `reports/gsc/code/`
- `reports/ga4/code/`
- `reports/crux/code/`
- `reports/code/` (maestro)

Puedes ejecutar `*.ps1` o `*.bat` directamente desde PowerShell.

## Dónde ver resultados

Cada ejecución genera archivos versionados por timestamp en:

- `reports/gsc/`
- `reports/ga4/`
- `reports/crux/`

Tipos de entregables:

- `*_executive_summary_*.md` (lectura ejecutiva)
- `*.csv` (detalle analítico para BI/Excel/QA)

## Seguridad y buenas prácticas

- Secretos y credenciales excluidos por `.gitignore`:
  - `Credentials/`
  - `*.pickle`
  - `scripts/**/ga_credentials.json`
  - `scripts/**/service_account.json`
  - `scripts/**/crux_key.txt`
  - `.env*`
- Flujo recomendado:
  1. Extraer datos.
  2. Analizar por fuente o con maestro.
  3. Revisar reportes.
  4. Commit de cambios de código (no de secretos).

## Roadmap (siguiente iteración)

- Integrar análisis de Screaming Frog enterprise.
- Generar scorecards unificados (SEO visibility + CWV + traffic quality).
- Automatizar ejecución diaria/semanal (scheduler).
- Publicar salidas en dashboard ejecutivo.

## Autor

Proyecto desarrollado por **Emanuel / SEO as Code** para operación SEO data-driven a nivel empresa.
