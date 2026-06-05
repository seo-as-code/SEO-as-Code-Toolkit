# SEO as Code Toolkit

> **Languages:** [English](README.md) | [Español](README.es.md)

Automated SEO system to extract, analyze, and report data from:

- Google Search Console (GSC)
- Google Analytics 4 (GA4)
- Chrome UX Report (CrUX)
- (Screaming Frog integration foundation)

This repository implements an **SEO-as-Code** approach: repeatable processes, Git-tracked workflows, and production-ready execution for teams.

## What we built

- Clear project structure by data source (`scripts/gsc`, `scripts/ga4`, `scripts/crux`).
- Enterprise-grade analyzers per channel.
- Master script for end-to-end analysis.
- Organized `reports` folder by source.
- Ready-to-run terminal commands (`reports/**/code`).
- Version control with Git + GitHub.
- Secret protection via `.gitignore`.

## Terminal commands (cheatsheet)

Ordered table with **all pipeline commands** (data extraction, enterprise analysis, AI modules 01–12):

→ **[comandos/COMANDOS_TERMINAL.md](comandos/COMANDOS_TERMINAL.md)**

## Project architecture

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

## Key scripts

### Master (all-in-one)

- `scripts/maestro_analisis_enterprise.py`
- Runs in sequence: GSC + GA4 + CrUX.
- Centralizes business parameters (thresholds and origin).

Example:

```bash
python scripts/maestro_analisis_enterprise.py --origin "https://your-domain.com"
```

### GSC Enterprise

- `scripts/gsc/gsc_analyze_enterprise.py`
- KPIs: clicks, impressions, weighted CTR, weighted position.
- Analysis: top queries, top pages, SEO opportunities, cannibalization.
- Output: Excel (`gsc_report_*.xlsx`, 5 sheets) + summary `.md` in `reports/gsc/`.

Example:

```bash
python scripts/gsc/gsc_analyze_enterprise.py --min-impressions 500 --low-ctr-threshold 0.02 --position-floor 4
```

### GA4 Enterprise

- `scripts/ga4/ga4_extract.py` for extraction (includes `page_path` and `page_title`).
- `scripts/ga4/ga4_analyze_enterprise.py` for analysis.
- KPIs: sessions, users, pageviews, unique landing pages, date range.
- Analysis: **dated traffic flow** (source/medium → destination URL), landing pages, channels and sources by day.
- Output: **single Excel** (`ga4_report_*.xlsx`, 9 sheets) + summary `.md` in `reports/ga4/`.

Key Excel sheets:

| Sheet | Content |
|-------|---------|
| Origen y destino | Date + source + destination URL + sessions |
| Landing pages por dia | Date + page + source |
| Resumen periodo | 30-day totals without daily breakdown |
| Canales / Fuentes por dia | Daily evolution by channel and source/medium |

Example:

```bash
python scripts/ga4/ga4_analyze_enterprise.py --input "C:\Users\emami\proyecto_seo\data\raw\ga4_last30days.csv"
```

### Screaming Frog

- Export crawl to `data/raw/sf_html.csv` (also accepts `internos_html.csv`).
- `scripts/sf/sf_utils.py` — shared Tier 1/2 column maps and filters.
- `scripts/sf/limpiar_sf.py` writes two files to `data/processed/`:

| File | Purpose | Filters |
|------|---------|---------|
| `sf_audit.csv` | Technical audit (404, noindex, redirects…) | HTML only |
| `sf_limpio.csv` | On-page + GSC cross-check / AI module 07 | HTML + 200 + indexable |

Example:

```bash
python scripts/sf/limpiar_sf.py
python scripts/sf/limpiar_sf.py --input data/raw/sf_html.csv
```

### Stage 1 demo (GSC + GA4 + CrUX + SF)

```bash
python scripts/demo_etapa1.py
```

### CrUX Enterprise

- `scripts/crux/crux_analyze_enterprise.py`
- Queries CrUX API by origin.
- Analyzes Core Web Vitals: LCP, INP, CLS (p75 and distribution).
- Evaluates pass/fail against official thresholds.
- Output: CSV + executive summary in `reports/crux/`.

Example:

```bash
python scripts/crux/crux_analyze_enterprise.py --origin "https://your-domain.com"
```

## Quick run (copy/paste)

Prebuilt commands are available in:

- `reports/gsc/code/`
- `reports/ga4/code/`
- `reports/crux/code/`
- `reports/code/` (master)

You can run `*.ps1` or `*.bat` directly from PowerShell.

## Where to find results

Each run generates timestamped files in:

- `reports/gsc/`
- `reports/ga4/`
- `reports/crux/`

Deliverables:

- `*_executive_summary_*.md` (executive summary)
- `*.csv` (detailed analytics for BI/Excel/QA)

## Local site configuration

GSC/CrUX scripts read your domain from a **local** file (not committed to GitHub):

```powershell
copy config\site.local.yaml.example config\site.local.yaml
```

Edit `config/site.local.yaml` with your `origin`, `gsc_site_url`, and `sitemap_url`.

## Security and best practices

- Secrets and client configuration excluded by `.gitignore`:
  - `config/site.local.yaml`
  - `content/`
  - `Credentials/`
  - `*.pickle`
  - `scripts/**/ga_credentials.json`
  - `scripts/**/service_account.json`
  - `scripts/**/crux_key.txt`
  - `.env*`
- Recommended workflow:
  1. Extract data.
  2. Analyze by source or with master script.
  3. Review reports.
  4. Commit code changes (never secrets).

## Roadmap (next iteration)

- Integrate Screaming Frog enterprise analysis.
- Generate unified scorecards (SEO visibility + CWV + traffic quality).
- Automate daily/weekly execution (scheduler).
- Publish outputs to an executive dashboard.

## Related repository

- Decision layer: **AI-SEO-Toolkit** (10-module AI SEO analysis and prioritized action plans)
- Data layer: **SEO-as-Code-Toolkit** (this repository)

## Author

Built by **Emanuel / SEO as Code** for enterprise-grade, data-driven SEO operations.
