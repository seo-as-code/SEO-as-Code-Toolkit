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

## Comandos de terminal (chuleta)

Tabla ordenada con **todos los comandos** del pipeline (datos, análisis enterprise, módulos AI 01–12):

→ **[comandos/COMANDOS_TERMINAL.md](comandos/COMANDOS_TERMINAL.md)**

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
    demo_etapa1.py
    sf/
      sf_utils.py
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
python scripts/maestro_analisis_enterprise.py --origin "https://your-domain.com"
```

### GSC Enterprise

- `scripts/gsc/gsc_analyze_enterprise.py`
- KPIs: clicks, impressions, CTR ponderado, posición ponderada.
- Análisis: top queries, top pages, oportunidades SEO, canibalización.
- Salida: Excel (`gsc_report_*.xlsx`, 5 hojas) + resumen `.md` en `reports/gsc/`.

Ejemplo:

```bash
python scripts/gsc/gsc_analyze_enterprise.py --min-impressions 500 --low-ctr-threshold 0.02 --position-floor 4
```

### GA4 Enterprise

- `scripts/ga4/ga4_extract.py` para extracción (incluye `page_path` y `page_title`).
- `scripts/ga4/ga4_analyze_enterprise.py` para análisis.
- KPIs: sesiones, usuarios, pageviews, landing pages únicas, rango de fechas.
- Análisis: **origen → destino con fecha** (source/medium + URL), landing pages, canales y fuentes por día.
- Salida: **un Excel** (`ga4_report_*.xlsx`, 9 hojas) + resumen `.md` en `reports/ga4/`.

Hojas principales del Excel:

| Hoja | Contenido |
|------|-----------|
| Origen y destino | Fecha + fuente + URL de destino + sesiones |
| Landing pages por día | Fecha + página + fuente |
| Resumen periodo | Totales 30 días sin desglose diario |
| Canales / Fuentes por día | Evolución diaria por canal y source/medium |

Ejemplo:

```bash
python scripts/ga4/ga4_analyze_enterprise.py --input "C:\Users\emami\proyecto_seo\data\raw\ga4_last30days.csv"
```

### Screaming Frog

- Exporta el crawl en SF y guarda `data/raw/sf_html.csv` (también acepta `internos_html.csv`).
- `scripts/sf/sf_utils.py` — columnas Tier 1/2 y filtros compartidos.
- `scripts/sf/limpiar_sf.py` genera dos salidas en `data/processed/`:

| Archivo | Uso | Filtros |
|---------|-----|---------|
| `sf_audit.csv` | Auditoría técnica (404, noindex, redirects…) | Solo HTML |
| `sf_limpio.csv` | On-page + cruce GSC / módulo AI 07 | HTML + 200 + indexable |

Ejemplo:

```bash
python scripts/sf/limpiar_sf.py
python scripts/sf/limpiar_sf.py --input data/raw/sf_html.csv
```

### Demo Etapa 1 (GSC + GA4 + CrUX + SF)

```bash
python scripts/demo_etapa1.py
```

### CrUX Enterprise

- `scripts/crux/crux_analyze_enterprise.py`
- Consulta API CrUX por origin.
- Analiza Core Web Vitals: LCP, INP, CLS (p75 y distribución).
- Evalúa pass/fail por umbrales oficiales.
- Salida: CSV + resumen ejecutivo en `reports/crux/`.

Ejemplo:

```bash
python scripts/crux/crux_analyze_enterprise.py --origin "https://your-domain.com"
```

## Cómo ejecutar rápido (copy/paste)

Se incluyen comandos preparados en:

- `reports/gsc/code/`
- `reports/ga4/code/`
- `reports/crux/code/`
- `reports/code/` (maestro)

Puedes ejecutar `*.ps1` o `*.bat` directamente desde PowerShell.

## Dónde ver resultados

Cada ejecución genera archivos con timestamp en:

- `reports/gsc/` → `gsc_report_*.xlsx` (5 hojas) + resumen `.md`
- `reports/ga4/` → `ga4_report_*.xlsx` (9 hojas: fecha + origen → destino) + resumen `.md`
- `reports/crux/` → CSV + resumen `.md`
- `data/processed/` → `sf_audit.csv` (auditoría técnica) + `sf_limpio.csv` (on-page)

Los informes generados y los CSV de datos **no van a GitHub** (ver `.gitignore`).

## Configuración local del sitio

Los scripts GSC/CrUX leen tu dominio desde un archivo **local** (no va a GitHub):

```powershell
copy config\site.local.yaml.example config\site.local.yaml
```

Edita `config/site.local.yaml` con tu `origin`, `gsc_site_url` y `sitemap_url`.

## Seguridad y buenas prácticas

- Secretos y configuración de cliente excluidos por `.gitignore`:
  - `config/site.local.yaml`
  - `content/`
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

## Repositorio relacionado

- Capa de decision: **AI-SEO-Toolkit** (analisis AI SEO de 10 modulos y plan de accion priorizado)
- Capa de datos: **SEO-as-Code-Toolkit** (este repositorio)

## Autor

Proyecto desarrollado por **Emanuel / SEO as Code** para operación SEO data-driven a nivel empresa.
