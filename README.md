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

## Key scripts

### Master (all-in-one)

- `scripts/maestro_analisis_enterprise.py`
- Runs in sequence: GSC + GA4 + CrUX.
- Centralizes business parameters (thresholds and origin).

Example:

```bash
python scripts/maestro_analisis_enterprise.py --origin "https://studiorethinkibiza.com"
```

### GSC Enterprise

- `scripts/gsc/gsc_analyze_enterprise.py`
- KPIs: clicks, impressions, weighted CTR, weighted position.
- Analysis: top queries, top pages, SEO opportunities, cannibalization.
- Output: CSV + executive summary in `reports/gsc/`.

Example:

```bash
python scripts/gsc/gsc_analyze_enterprise.py --min-impressions 500 --low-ctr-threshold 0.02 --position-floor 4
```

### GA4 Enterprise

- `scripts/ga4/ga4_extract.py` for extraction.
- `scripts/ga4/ga4_analyze_enterprise.py` for analysis.
- KPIs: sessions, users, pageviews, pages/session.
- Analysis: channel performance, top source/medium, daily trend.
- Output: CSV + executive summary in `reports/ga4/`.

Example:

```bash
python scripts/ga4/ga4_analyze_enterprise.py --input "C:\Users\emami\proyecto_seo\data\raw\ga4_traffic_last30days.csv"
```

### CrUX Enterprise

- `scripts/crux/crux_analyze_enterprise.py`
- Queries CrUX API by origin.
- Analyzes Core Web Vitals: LCP, INP, CLS (p75 and distribution).
- Evaluates pass/fail against official thresholds.
- Output: CSV + executive summary in `reports/crux/`.

Example:

```bash
python scripts/crux/crux_analyze_enterprise.py --origin "https://studiorethinkibiza.com"
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

## Security and best practices

- Secrets and credentials excluded by `.gitignore`:
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
