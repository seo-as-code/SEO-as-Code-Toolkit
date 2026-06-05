# Playbook completo — SEO-as-Code · AI-as-Code · GSC Index Monitor

Documento maestro: qué construimos, cómo encaja todo, paso a paso, qué va en Git y dónde está cada guía.

**Raíz del workspace:** `C:\Users\emami\proyecto_seo`

---

## 1. Visión en una frase

Tres capas del mismo enfoque **SEO-as-Code** (procesos repetibles, versionados, medibles):

```text
CAPA 1 — DATOS (SEO-as-Code)     →  Extraer GSC, GA4, CrUX, Screaming Frog a CSV
CAPA 2 — ENTERPRISE (opcional)   →  Informes KPI (Excel/MD) para stakeholders
CAPA 3 — DECISIÓN (AI-as-Code)   →  Módulos 01–12: intención, gaps, técnico, plan
PARALELO — INDEX MONITOR          →  URLs no indexadas: sync → audit → P1/P2/P3
```

**Flujo habitual:** Etapa 1 → Etapa 3 (+ Monitor semanal si hay problemas de indexación).

---

## 2. Qué está en GitHub y qué es solo local

| Qué | Repo / carpeta | GitHub | Notas |
|-----|----------------|--------|--------|
| **SEO-as-Code Toolkit** | `proyecto_seo/` (scripts, maestro, reports/code) | [github.com/seo-as-code](https://github.com/seo-as-code) — org **seo-as-code** | Código y comandos sí; datos y credenciales no |
| **AI-SEO-Toolkit** | `proyecto_seo/ai-seo-toolkit/` | Repo publicado aparte: **AI-SEO-Toolkit** | En `.gitignore` del repo padre → se versiona en su propio repo |
| **GSC Index Monitor** | `proyecto_seo/proyecto_seo-index/` | Dentro del monorepo `proyecto_seo` | Código sí; `credentials/`, `token.json`, `data/runs/*.csv` no |
| **Notas entrevista** | `proyecto_seo/private/` | **Nunca** (gitignored) | `INTERVIEW_PLAYBOOK.md` solo local |
| **Contenido publicado** | `proyecto_seo/content/` | Sí (artículos, schema, HTML) | Entregable SEO + schema |

### Qué NO subir a Git (`.gitignore`)

- `Credentials/`, `*.pickle`, `token.json`, `credentials/*.json`
- `data/raw/*.csv`, `reports/**/*.csv`, informes generados `*_summary_*.md`
- `seo-automation/venv/`, `proyecto_seo-index/venv/`
- Carpeta `private/`
- Repo hijo `ai-seo-toolkit/` (tiene su propio remoto)

### Qué SÍ subir a Git

- Scripts Python (`scripts/`, `proyecto_seo-index/src/`)
- README, `comandos/COMANDOS_TERMINAL.md`, playbooks en `docs/`
- `config.yaml`, `requirements.txt`, `.gitignore`
- Plantillas y código de módulos AI (en repo AI-SEO-Toolkit)
- Carpeta `content/` (artículo + `schema.jsonld` sin secretos)

---

## 3. Mapa de carpetas

```text
C:\Users\emami\proyecto_seo\
│
├── maestro_seo.py                 ← Menú Etapa 1 (GSC, GA4, CrUX, SF)
├── scripts/
│   ├── gsc/                       ← OAuth, fetch, analyze enterprise
│   ├── ga4/
│   ├── crux/
│   ├── sf/                        ← leer_sf.py, limpiar_sf.py
│   └── maestro_analisis_enterprise.py   ← Etapa 2 (los 3 canales)
│
├── data/raw/                      ← CSV crudos (NO en git)
├── reports/                       ← Informes generados (NO CSV en git)
│   ├── gsc/ code/
│   ├── ga4/ code/
│   ├── crux/ code/
│   └── code/                      ← .bat / .ps1 maestro enterprise
│
├── comandos/
│   └── COMANDOS_TERMINAL.md       ← Chuleta oficial (3 etapas)
│
├── ai-seo-toolkit/                ← AI-as-Code (repo GitHub separado)
│   ├── scripts/modules/01…12
│   ├── scripts/orchestrator/ai_seo_master.py
│   ├── config/project.yaml
│   └── reports/ai + reports/executive
│
├── proyecto_seo-index/            ← GSC Index Monitor
│   ├── src/                       ← sync, audit, report, classifier
│   ├── data/imports/              ← gsc_export.csv (entrada)
│   ├── data/runs/                 ← salidas (NO en git)
│   └── docs/                      ← guías operativas
│
├── content/                       ← Artículos + JSON-LD listos para WP
├── Credentials/                   ← OAuth (NO en git)
├── seo-automation/venv/           ← Python compartido
├── docs/PLAYBOOK-COMPLETO.md      ← Este archivo
└── private/                       ← Solo local
```

---

## 4. SEO-as-Code — Paso a paso (Etapa 1 + 2)

### 4.1 Objetivo

Sacar datos reales de Google y del crawl a **CSV versionados localmente**, luego (opcional) informes enterprise para cliente/jefe.

### 4.2 Etapa 1 — Sacar datos

**Carpeta:** `cd C:\Users\emami\proyecto_seo`

#### Opción A — Menú (recomendado la primera vez)

```powershell
cd C:\Users\emami\proyecto_seo
py .\maestro_seo.py
```

| Menú | Acción | Script | Salida |
|------|--------|--------|--------|
| **1 → 1** | Export GSC OAuth | `scripts/gsc/gsc_oauth.py` | `data/raw/gsc_oauth_FECHA_FECHA.csv` |
| **1 → 2** | Fetch GSC alternativo | `scripts/gsc/gsc_fetch.py` | CSV GSC |
| **2 → 1** | Login GA4 (1ª vez) | `scripts/ga4/ga4_oauth.py` | credenciales |
| **2 → 2** | Tráfico 30 días | `scripts/ga4/ga4_extract.py` | `data/raw/ga4_last30days.csv` |
| **3** | Test CrUX | `scripts/crux/crux_api_test.py` | pantalla |
| **4 → 1** | Leer crawl SF | `scripts/sf/leer_sf.py` | prepara rutas |
| **4 → 2** | Limpiar SF | `scripts/sf/limpiar_sf.py` | `data/raw/internos_todo.csv` |

**Mínimo para AI-as-Code:** menú **1 → 1** (GSC).  
**Recomendado:** GSC + `internos_todo.csv` (módulo 07 técnico).

#### Opción B — Comandos directos

```powershell
cd C:\Users\emami\proyecto_seo
py .\scripts\gsc\gsc_oauth.py
py .\scripts\sf\leer_sf.py
py .\scripts\sf\limpiar_sf.py
```

#### Primera vez — Credenciales GSC/GA4

- Carpeta: `Credentials/credentials.json` (OAuth client Google Cloud)
- Tras OAuth: `token.pickle` en raíz (no commitear)
- Guía monitor indexación: `proyecto_seo-index/docs/gsc-auth-setup.md`

### 4.3 Etapa 2 — Análisis enterprise (opcional)

No usa IA. Convierte CSV de Etapa 1 en informes legibles.

```powershell
cd C:\Users\emami\proyecto_seo
py .\scripts\maestro_analisis_enterprise.py --origin "https://TU-DOMINIO.com"
```

O por canal:

| Canal | Comando | Salida |
|-------|---------|--------|
| GSC | `py .\scripts\gsc\gsc_analyze_enterprise.py` | `reports/gsc/gsc_report_*.xlsx` (5 hojas) + `gsc_executive_summary_*.md` |
| GA4 | `py .\scripts\ga4\ga4_analyze_enterprise.py` | `reports/ga4/` |
| CrUX | `py .\scripts\crux\crux_analyze_enterprise.py --origin "https://..."` | `reports/crux/` |

**Atajos:** `reports\code\run_full_enterprise_analysis.bat`

**KPIs típicos del informe GSC:** clicks, impressions, CTR, posición media, top queries, oportunidades CTR, canibalización.

### 4.4 Documentación SEO-as-Code en Git

| Documento | Ruta |
|-----------|------|
| README ES/EN | `README.es.md`, `README.md` |
| Todos los comandos | `comandos/COMANDOS_TERMINAL.md` |
| Índice comandos | `comandos/README.md` |

---

## 5. AI-as-Code (AI-SEO-Toolkit) — Paso a paso (Etapa 3)

### 5.1 Objetivo

Convertir CSV de Etapa 1 (+ crawl) en **diagnóstico priorizado**: intención, gaps de contenido, auditoría técnica, plan de acción e informe ejecutivo.

### 5.2 Prerrequisitos

1. Etapa 1 hecha → al menos `data/raw/gsc_oauth_*.csv`
2. (Recomendado) `data/raw/internos_todo.csv` desde Screaming Frog
3. Copiar `ai-seo-toolkit/config/project.local.yaml.example` → `project.local.yaml` y rellenar tu sitio (no subir a GitHub)
4. Copiar `config/site.local.yaml.example` → `config/site.local.yaml` para scripts GSC del repo padre

### 5.3 Instalación (una vez)

```powershell
cd C:\Users\emami\proyecto_seo\ai-seo-toolkit
pip install -r requirements.txt
```

### 5.4 Pipeline completo (recomendado)

Ejecuta módulos **01 → 10 → 12 → 11** (el 11 siempre al final).

```powershell
cd C:\Users\emami\proyecto_seo\ai-seo-toolkit
py .\scripts\orchestrator\ai_seo_master.py --gsc (Get-ChildItem ..\data\raw\gsc_oauth*.csv | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
```

O atajo:

```powershell
.\reports\code\run_ai_seo_master.ps1
```

**OK:** mensaje `AI SEO full pipeline completed.`

### 5.5 Qué hace cada módulo

| # | Módulo | Script | Necesita GSC | Output principal |
|---|--------|--------|--------------|------------------|
| 01 | Mapa semántico | `01_semantic_map.py` | No | `reports/ai/01_semantic_map_*` |
| 02 | Entidades | `02_entity_extraction.py` | No | entidades por URL |
| 03 | Intención búsqueda | `03_intent_classifier.py` | Sí | matriz intención |
| 04 | Tono y estilo | `04_tone_style.py` | No | legibilidad / tono |
| 05 | Content gaps | `05_content_gaps.py` | Sí | queries con demanda sin cobertura |
| 06 | AI rewrite | `06_ai_rewrite.py` | No | sugerencias title/meta/H1 |
| 07 | Auditoría técnica | `07_technical_audit.py` | No (SF) | issues técnicos CSV |
| 08 | UX/CRO | `08_ux_cro.py` | No | checks conversión |
| 09 | Competencia | `09_competitor_gap.py` | No | gaps vs competidores |
| 10 | Plan de acción | `10_action_plan.py` | No | backlog priorizado |
| 12 | Estrategia blog | `12_blog_strategy.py` | Sí | calendario / temas |
| 11 | Informe ejecutivo | `11_executive_report.py` | No | resume todo en MD |

**Un módulo suelto:**

```powershell
py .\scripts\modules\05_content_gaps.py --gsc C:\Users\emami\proyecto_seo\data\raw\gsc_oauth_YYYY-MM-DD_YYYY-MM-DD.csv
```

Atajos: `reports\code\run_module_01.ps1` … `run_module_12.ps1`

### 5.6 Dónde leer resultados

| Carpeta | Para qué |
|---------|----------|
| `ai-seo-toolkit/reports/ai/` | Detalle CSV por módulo |
| `ai-seo-toolkit/reports/executive/` | Informe cliente: `11_informe_ejecutivo_*.md`, `10_action_plan_*.md` |

### 5.7 Publicar AI-as-Code en GitHub

Desde `ai-seo-toolkit/` (repo independiente):

```powershell
git add .
git commit -m "Update: modules and reports structure"
git push origin main
```

Remoto documentado: `https://github.com/seo-as-code/AI-SEO-Toolkit.git`

### 5.8 Documentación AI-as-Code

| Documento | Ruta |
|-----------|------|
| README toolkit | `ai-seo-toolkit/README.md` |
| Config proyecto | `ai-seo-toolkit/config/project.yaml` |
| Playbook entrevista (local) | `private/INTERVIEW_PLAYBOOK.md` |

---

## 6. GSC Index Monitor — Paso a paso

### 6.1 Objetivo

GSC dice *qué* URLs no están indexadas; el monitor comprueba **si el problema sigue hoy** y genera **cola P1/P2/P3** para WordPress/dev.

### 6.2 Pipeline interno (3 fases)

```text
SYNC  →  importar URLs + motivo GSC (CSV manual o API)
AUDIT →  visitar cada URL (status, redirect, noindex, canonical, sitemap)
REPORT→  CSV + summary.md con prioridad y acción recomendada
```

**Código:** `proyecto_seo-index/src/main.py`  
**Clasificador:** `src/classifier.py`  
**Auditor en vivo:** `src/live_auditor.py`  
**API GSC:** `src/gsc_client.py`, `src/auth.py`

### 6.3 Configuración

- `proyecto_seo-index/config.yaml` — URL sitio, sitemap, rutas credenciales
- Credenciales: reutiliza `../Credentials/` y `../token.pickle` o `credentials/gsccredentialindexing.json`
- Guía OAuth: `docs/gsc-auth-setup.md`

### 6.4 Entrada de datos

**Opción A — CSV manual (45 URLs del informe GSC)**

1. GSC → Indexing → Pages → Why pages aren't indexed  
2. Exportar por categoría (6 tipos)  
3. Unir en `data/imports/gsc_export.csv` con columnas `URL`, `Reason`  
4. Guía: `docs/exportar-gsc-paso-a-paso.md`

**Opción B — API automática (sitemap + URL Inspection)**

- Lee URLs del sitemap + analytics  
- Inspecciona con API (cuota: pausa entre llamadas)  
- Guarda no indexadas en `data/imports/gsc_export.csv`  
- Luego mismo pipeline audit + report

### 6.5 Comandos

```powershell
cd C:\Users\emami\proyecto_seo\proyecto_seo-index
```

| Acción | Comando |
|--------|---------|
| **Todo en uno** (CSV) | `.\scripts\run.bat --skip-api` |
| **Todo en uno** (API) | `.\scripts\run.bat` o `.\scripts\run.ps1` |
| Solo sync | `..\seo-automation\venv\Scripts\python.exe -m src.main sync --skip-api` |
| Solo audit | `python -m src.main audit` |
| Solo report | `python -m src.main report` |
| Export API | `python -m src.main export` |
| Salud sitio | `python scripts\check_site_health.py` |
| Checklist GSC | `python scripts\gsc_validate_checklist.py` |

**Salidas (local, no git):**

- `data/runs/snapshot_FECHA.json`
- `data/runs/audited_FECHA.json`
- `data/runs/report_FECHA.csv` ← tabla para Excel/dev
- `data/runs/summary_FECHA.md` ← empieza aquí

### 6.6 Prioridades P1 / P2 / P3

| Prioridad | Significado | Acción típica |
|-----------|-------------|---------------|
| **P1** | Bloqueo técnico | 404, sitemap caído, noindex accidental, redirect roto |
| **P2** | Descubrimiento | Discovered not indexed; falta sitemap/enlaces |
| **P3** | Calidad | Crawled not indexed; thin/duplicate |

### 6.7 Después del informe — WordPress / hosting

1. Arreglar **P1** primero → `docs/wp-fixes-playbook.md`  
2. GSC → **Validate fix** por categoría  
3. Semana siguiente → re-ejecutar `run.bat` y comparar `summary_*.md` (delta URLs)

**Resultados reales documentados:** de ~45 URLs reportadas → monitor refinó a ~20 activas → última corrida **4 URLs** (0 P1). Sitemap corregido de HTTP 500 a 200.

### 6.8 Documentación del Monitor

| Documento | Ruta |
|-----------|------|
| Guía maestra | `proyecto_seo-index/docs/GUIA-COMPLETA.md` |
| Export GSC paso a paso | `docs/exportar-gsc-paso-a-paso.md` |
| Playbook WordPress | `docs/wp-fixes-playbook.md` |
| Sync semanal | `docs/weekly-sync.md` |
| Estado / checklist | `proyecto_seo-index/ESTADO.md` |
| README rápido | `proyecto_seo-index/README.md` |

---

## 7. Entregable contenido (SEO + schema)

Carpeta: `content/eco-friendly-renovations-ibiza/`

| Archivo | Uso |
|---------|-----|
| `article.md` / `article-wordpress.html` | Copy del post |
| `schema.jsonld` | Article + FAQPage + LocalBusiness |
| `POST-copiar-en-elementor.md` | Publicación en WP |
| `README-publicacion.md` | Checklist |

**Origen:** gap detectado en pipeline AI-as-Code (query con impresiones en GSC) → contenido + schema alineados.

---

## 8. Flujo completo A → Z (primera vez)

```powershell
# ── 0. Siempre ──
cd C:\Users\emami\proyecto_seo

# ── ETAPA 1: datos ──
py .\maestro_seo.py
# Elegir: 1→1 (GSC), 4→2 (SF limpiar)

# ── ETAPA 2: opcional ──
py .\scripts\maestro_analisis_enterprise.py --origin "https://TU-DOMINIO.com"

# ── ETAPA 3: AI ──
cd .\ai-seo-toolkit
pip install -r requirements.txt
py .\scripts\orchestrator\ai_seo_master.py --gsc ..\data\raw\gsc_oauth_MAS_RECIENTE.csv
# Leer: reports\executive\11_informe_ejecutivo_*.md

# ── INDEX MONITOR (si hay URLs no indexadas) ──
cd ..\proyecto_seo-index
# Colocar o generar gsc_export.csv
.\scripts\run.bat --skip-api
# Leer: data\runs\summary_*.md
# Arreglar P1: docs\wp-fixes-playbook.md
```

---

## 9. Flujo semanal (operación)

| Día | Tarea |
|-----|--------|
| Lunes | `gsc_oauth.py` o menú 1→1 → actualizar CSV |
| Lunes | `proyecto_seo-index\scripts\run.bat` → revisar P1/P2 |
| Tras fixes WP | GSC Validate fix |
| Mensual | `maestro_analisis_enterprise.py` + `ai_seo_master.py` |
| Mensual | Comparar `summary_*.md` (delta URLs no indexadas) |

---

## 10. Cómo explicarlo (elevator pitch)

> "Tengo un stack SEO-as-Code en GitHub: primero extraigo datos reales (GSC, GA4, CrUX, crawl) a CSV; opcionalmente informes enterprise; luego AI-as-Code convierte eso en plan de acción priorizado; en paralelo un Index Monitor audita URLs no indexadas en vivo y saca backlog P1/P2/P3 para dev. Todo reproducible, sin commitear secretos ni exports."

---

## 11. Índice rápido de documentos

| Necesito… | Abrir |
|-----------|--------|
| Todos los comandos terminal | `comandos/COMANDOS_TERMINAL.md` |
| Playbook global | `docs/PLAYBOOK-COMPLETO.md` (este) |
| Monitor indexación completo | `proyecto_seo-index/docs/GUIA-COMPLETA.md` |
| Exportar 45 URLs GSC | `proyecto_seo-index/docs/exportar-gsc-paso-a-paso.md` |
| Arreglos WordPress | `proyecto_seo-index/docs/wp-fixes-playbook.md` |
| AI toolkit | `ai-seo-toolkit/README.md` |
| Entrevista (solo PC) | `private/INTERVIEW_PLAYBOOK.md` |

---

## 12. Git — qué commitear después de cambiar código

```powershell
cd C:\Users\emami\proyecto_seo
git status
git add scripts/ proyecto_seo-index/src/ docs/ content/ README.es.md comandos/
git commit -m "docs: playbook completo y ajustes monitor"
git push
```

Para **ai-seo-toolkit**, commit y push **desde esa carpeta** en su repo.

**Nunca:** `git add Credentials/ data/raw/ reports/*.csv token.json credentials/`

---

*Última actualización: junio 2026 — Emanuel / SEO as Code*
