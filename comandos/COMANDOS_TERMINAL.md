# Chuleta de comandos

Copia y pega en la terminal (**Ctrl + `**). No escribes código: solo ejecutas scripts.

---

## Mapa del proyecto (3 etapas)

```text
ETAPA 1 — DATOS              ETAPA 2 — ENTERPRISE         ETAPA 3 — AI
(proyecto_seo)               (proyecto_seo, opcional)     (ai-seo-toolkit)
─────────────────            ─────────────────────        ─────────────────
GSC, GA4, SF, CrUX    →      Informes CSV clásicos   →    Módulos 01–12
CSV en data\raw\              reports\gsc, ga4, crux        Informes .md cliente
```

| Etapa | Carpeta | Para qué |
|-------|---------|----------|
| **1** | `C:\Users\emami\proyecto_seo` | Sacar datos a CSV |
| **2** | `C:\Users\emami\proyecto_seo` | Analizar esos CSV (sin IA) |
| **3** | `C:\Users\emami\proyecto_seo\ai-seo-toolkit` | Análisis AI + informe ejecutivo |

**Orden habitual:** 1 → 3. La etapa 2 es opcional.

**Siempre primero:**

```powershell
cd C:\Users\emami\proyecto_seo
```

---

## Índice

1. [Etapa 1 — Sacar datos](#etapa-1--sacar-datos)
2. [Etapa 2 — Análisis enterprise](#etapa-2--análisis-enterprise-opcional)
3. [Etapa 3 — Módulos AI](#etapa-3--módulos-ai)
4. [Flujo completo A → Z](#flujo-completo-a--z)
5. [Demo rápida](#demo-rápida)
6. [Ayuda](#ayuda)

---

# Etapa 1 — Sacar datos

**Objetivo:** crear CSV en `data\raw\`.  
**Carpeta:** `C:\Users\emami\proyecto_seo`

## Qué puedes hacer aquí

| Acción | Obligatorio para AI | Salida |
|--------|---------------------|--------|
| Exportar GSC | **Sí** | `data\raw\gsc_oauth_*.csv` |
| Exportar GA4 | No (solo etapa 2) | `data\raw\ga4_last30days.csv` |
| Subir crawl Screaming Frog | Recomendable (módulo 07) | `data\raw\internos_todo.csv` |
| Test CrUX | No | pantalla |

---

## Opción A — Menú con números (`maestro_seo.py`)

Mismo resultado que los comandos sueltos, pero eliges con números.

```powershell
cd C:\Users\emami\proyecto_seo
py .\maestro_seo.py
```

### Menú principal

| Eliges | Fuente |
|--------|--------|
| **1** | Google Search Console |
| **2** | Google Analytics 4 |
| **3** | Core Web Vitals (CrUX) |
| **4** | Screaming Frog |
| **0** | Salir |

### Dentro de GSC (opción 1)

| Eliges | Qué hace | Equivalente comando |
|--------|----------|---------------------|
| **1** | Exportar GSC (OAuth) | `py .\scripts\gsc\gsc_oauth.py` |
| **2** | Extraer GSC (alternativo) | `py .\scripts\gsc\gsc_fetch.py` |
| **3** | Análisis básico | `py .\scripts\gsc\analisis_gsc.py` |
| **4** | Análisis avanzado | Pide ruta del CSV → ver [Ayuda](#si-el-menú-pide-ruta-de-csv) |
| **5** | Enviar sitemap | `py .\scripts\gsc\enviar_sitemap.py` |

### Dentro de GA4 (opción 2)

| Eliges | Qué hace |
|--------|----------|
| **1** | Login Google (1ª vez) |
| **2** | Exportar tráfico 30 días |

### Dentro de SF (opción 4)

| Eliges | Qué hace |
|--------|----------|
| **1** | Leer CSV del crawl |
| **2** | Limpiar CSV |

**Para módulos AI necesitas como mínimo:** menú **1 → 1** (GSC).

---

## Opción B — Comandos directos

### GSC (imprescindible)

```powershell
cd C:\Users\emami\proyecto_seo
py .\scripts\gsc\gsc_oauth.py
```

**OK:** `Exportado: ...\data\raw\gsc_oauth_FECHA_FECHA.csv`

### GA4

```powershell
py .\scripts\ga4\ga4_oauth.py
py .\scripts\ga4\ga4_extract.py
```

### Screaming Frog

1. Exporta el crawl en la app Screaming Frog.
2. Guarda el `.csv` en `C:\Users\emami\proyecto_seo\data\raw\`

```powershell
py .\scripts\sf\leer_sf.py
py .\scripts\sf\limpiar_sf.py
```

### Comprobar que los datos existen

```powershell
Get-ChildItem .\data\raw
```

---

# Etapa 2 — Análisis enterprise (opcional)

**Objetivo:** informes enterprise (GSC Excel + GA4/CrUX CSV).  
**Carpeta:** `C:\Users\emami\proyecto_seo`  
**No usa módulos AI.** No es obligatoria para la etapa 3.

## Qué puedes hacer

| Acción | Comando | Salida |
|--------|---------|--------|
| Análisis GSC | `py .\scripts\gsc\gsc_analyze_enterprise.py` | `reports\gsc\` → `gsc_report_*.xlsx` (5 hojas) + `.md` |
| Análisis GA4 | `py .\scripts\ga4\ga4_analyze_enterprise.py` | `reports\ga4\` |
| Análisis CrUX | `py .\scripts\crux\crux_analyze_enterprise.py --origin "https://TU-DOMINIO.com"` | `reports\crux\` |
| Los tres juntos | `py .\scripts\maestro_analisis_enterprise.py --origin "https://TU-DOMINIO.com"` | las 3 carpetas |

### Atajos `.bat`

```powershell
.\reports\gsc\code\run_gsc_analysis.bat
.\reports\ga4\code\run_ga4_analysis.bat
.\reports\crux\code\run_crux_analysis.bat
.\reports\code\run_full_enterprise_analysis.bat
```

---

# Etapa 3 — Módulos AI

**Objetivo:** análisis inteligente + informes `.md` para cliente.  
**Carpeta:** `C:\Users\emami\proyecto_seo\ai-seo-toolkit`  
**Necesita:** CSV de GSC en `proyecto_seo\data\raw\` (etapa 1).

## Entrar al toolkit

```powershell
cd C:\Users\emami\proyecto_seo\ai-seo-toolkit
```

**OK:** `PS ...\ai-seo-toolkit>`

---

## Instalar librerías (solo 1ª vez)

`pip` ya viene con Python. Esto instala pandas y demás del proyecto:

```powershell
pip install -r requirements.txt
```

Si ya corriste módulos AI antes → **salta este paso**.

---

## Pipeline completo (recomendado)

Un solo comando lanza módulos **01 → 10 → 12 → 11**.

### Comando (copia entero — sin Tab)

```powershell
py .\scripts\orchestrator\ai_seo_master.py --gsc C:\Users\emami\proyecto_seo\data\raw\gsc_oauth_2026-05-02_2026-06-01.csv
```

Cambia la fecha del CSV por el tuyo, o usa el truco del CSV más reciente:

```powershell
py .\scripts\orchestrator\ai_seo_master.py --gsc (Get-ChildItem ..\data\raw\gsc_oauth*.csv | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
```

**OK al terminar:** `AI SEO full pipeline completed.`

**Dónde mirar:**

| Carpeta | Qué hay |
|---------|---------|
| `reports\ai\` | Detalle por módulo (CSV) |
| `reports\executive\` | Informes `.md` (módulos 11 y 12) |

**Abrir informe:** **Ctrl + P** → `ai-seo-toolkit/reports/executive/` → `.md` más reciente.

### Orden de ejecución (por qué 12 antes que 11)

| Paso | Módulo | Qué hace |
|------|--------|----------|
| 1–10 | 01 … 10 | Mapa, intención, gaps, técnico, plan… |
| 11º | **12** | Estrategia de blog |
| 12º | **11** | Informe ejecutivo final (resume todo) |

El módulo **11 siempre va al final**.

---

## Módulos uno a uno

Solo si quieres lanzar uno concreto o continuar tras un error.

| Módulo | Comando | Necesita GSC |
|--------|---------|--------------|
| 01 Mapa semántico | `py .\scripts\modules\01_semantic_map.py` | No |
| 02 Entidades | `py .\scripts\modules\02_entity_extraction.py` | No |
| 03 Intención | `py .\scripts\modules\03_intent_classifier.py --gsc RUTA_CSV` | Sí |
| 04 Tono y estilo | `py .\scripts\modules\04_tone_style.py` | No |
| 05 Huecos | `py .\scripts\modules\05_content_gaps.py --gsc RUTA_CSV` | Sí |
| 06 Reescritura | `py .\scripts\modules\06_ai_rewrite.py` | No |
| 07 Técnico | `py .\scripts\modules\07_technical_audit.py` | No (SF en data\raw) |
| 08 UX/CRO | `py .\scripts\modules\08_ux_cro.py` | No |
| 09 Competencia | `py .\scripts\modules\09_competitor_gap.py` | No |
| 10 Plan acción | `py .\scripts\modules\10_action_plan.py` | No |
| 12 Blog | `py .\scripts\modules\12_blog_strategy.py --gsc RUTA_CSV` | Sí |
| 11 Informe ES | `py .\scripts\modules\11_executive_report.py` | No (lee reports\ai\) |

**Atajos:** `.\reports\code\run_module_01.ps1` … `run_module_12.ps1`

**Si falló en el 05** (GSC mal puesto): continúa desde el 05 con la ruta correcta.

---

# Flujo completo A → Z

Copia bloque a bloque, en orden.

```powershell
# ── ETAPA 1: datos ──
cd C:\Users\emami\proyecto_seo
py .\scripts\gsc\gsc_oauth.py
Get-ChildItem .\data\raw\gsc_oauth*.csv

# ── ETAPA 2: opcional (puedes saltar) ──
# py .\scripts\maestro_analisis_enterprise.py --origin "https://TU-DOMINIO.com"

# ── ETAPA 3: AI ──
cd C:\Users\emami\proyecto_seo\ai-seo-toolkit
py .\scripts\orchestrator\ai_seo_master.py --gsc (Get-ChildItem ..\data\raw\gsc_oauth*.csv | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
```

Abre el informe en `reports\executive\`.

---

# Demo rápida

```powershell
cd C:\Users\emami\proyecto_seo
py .\scripts\gsc\gsc_oauth.py

cd C:\Users\emami\proyecto_seo\ai-seo-toolkit
py .\scripts\modules\11_executive_report.py
```

*(El 11 solo funciona bien si ya corriste el pipeline completo al menos una vez.)*

**Con menú en la etapa 1:**

```powershell
cd C:\Users\emami\proyecto_seo
py .\maestro_seo.py
```

Elige **1 → 1**, luego **0** para salir, y continúa con etapa 3.

---

# Ayuda

## Rutas: `.\` vs `..\`

| Estás en | Quieres | Escribes |
|----------|---------|----------|
| `proyecto_seo` | algo dentro | `.\data\raw\` |
| `ai-seo-toolkit` | CSV del padre | `..\data\raw\` |

**Error típico:** `--gsc .\data\raw\` desde `ai-seo-toolkit` → carpeta vacía, falla el módulo 05.

**Solución fácil:** usa ruta completa:

```text
C:\Users\emami\proyecto_seo\data\raw\gsc_oauth_FECHA_FECHA.csv
```

## Si el menú pide ruta de CSV

(GSC → opción 4). Pega la ruta completa:

```text
C:\Users\emami\proyecto_seo\data\raw\gsc_oauth_2026-05-02_2026-06-01.csv
```

## Errores frecuentes

| Qué ves | Qué hacer |
|---------|-----------|
| `FileNotFoundError: GSC CSV not found` | Ruta mal: usa `..\data\raw\` o ruta completa |
| Módulo 01 tarda sin escribir nada | Normal: está rastreando la web (1–5 min) |
| `python` no reconocido | Usa `py` |
| `llclear` no existe | Usa `cls` |
| CSV no visible en Cursor | **Ctrl+P** y pega la ruta |
| Tab no muestra CSV tras `--gsc ..` | Sigue escribiendo `..\data\raw\gsc_oauth_` y Tab, o usa ruta completa |

## Reglas de terminal

- Siempre `cd` antes de la carpeta.
- Usa `.\` (punto + barra), nunca `-\`.
- `maestro_seo.py` = etapa 1. No lanza módulos AI.
- `ai_seo_master.py` = etapa 3. No saca datos de Google.

---

*Proyecto: `C:\Users\emami\proyecto_seo`*
