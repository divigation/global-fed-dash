# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Single-file React dashboard (`global_economics_dashboard.html`) that visualizes macroeconomic data for the US, Argentina, and China. Built for an EMBA Global Economics course (BA 6239, Spring 2026).

## How to Run

```
python3 serve.py
```

Then open http://localhost:8000/global_economics_dashboard.html. The server proxies FRED API requests to avoid CORS restrictions (FRED doesn't send CORS headers, so direct browser fetch from any origin is blocked). The app prompts for a FRED API key on launch (free from fred.stlouisfed.org).

## Architecture

Everything lives in one HTML file (~718 lines) with inline CSS, inline JSX (transpiled by Babel standalone), and no external build tooling.

**Stack:** React 18 (UMD), Recharts (UMD), Babel standalone (in-browser JSX transform). All loaded via unpkg CDN.

**Key sections in the file (marked by comment banners):**
- **Configuration** (~line 68): `US_FRED`, `ARG_FRED`, `CHN_FRED` define FRED series IDs; `WB_INDICATORS` defines World Bank indicator codes; `COUNTRY_META` maps country keys to display metadata.
- **API Functions** (~line 122): `fetchFRED()` and `fetchWorldBank()` fetch from the FRED and World Bank REST APIs. `computeYoY()` and `computeQoQAnn()` are data transforms.
- **Dashboard Metrics** (~line 180): `DASHBOARD_METRICS` array defines the 10 metrics displayed per country (GDP growth, inflation, policy rate, unemployment, exchange rate, current account, debt/GDP, M2 growth, real rate, stock index).
- **React Components** (~line 196): `Sparkline`, `ComparisonChart`, `MetricCard`, `CountryPanel`, `ApiKeyScreen`, `App`.
- **App component** (~line 425): Orchestrates data loading, navigation (overview / country / compare views), and state management.

**Data flow:** User enters FRED API key → `loadData()` fetches all FRED series sequentially per country → computes derived metrics (YoY inflation, real rate via Fisher equation) → fetches World Bank annual data as supplement → renders.

**Views:** Overview (summary table), per-country deep dive (metric cards with sparklines), and cross-country comparison (overlay line chart with metric selector).

## Design Decisions

- FRED data is preferred over World Bank when both are available (higher frequency). World Bank serves as annual fallback.
- Real interest rate is computed client-side as policy rate minus CPI YoY (Fisher equation), not fetched directly.
- The US "exchange rate" metric uses the broad USD index (DTWEXBGS), not a bilateral rate.
- All styling uses CSS custom properties defined in `:root` (dark theme, DM Sans + JetBrains Mono fonts).
