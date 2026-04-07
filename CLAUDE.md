# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Single-file React dashboard (`index.html`) that compares macroeconomic data for the US, Argentina, and China. Built for an EMBA Global Economics course (BA 6239, Spring 2026). Deployed at pages.macdav.com via GitHub Pages.

## How to Run

Open `index.html` directly in a browser. No server, build step, or API key required — all data is static.

## Architecture

Everything lives in one HTML file with inline CSS, inline JSX (transpiled by Babel standalone), and no external build tooling.

**Stack:** React 18 (UMD), Recharts (UMD), prop-types (UMD), Babel standalone (in-browser JSX transform). All loaded via unpkg CDN.

**Key sections in the file (marked by comment banners):**
- **Static Data** (~line 68): `STATIC_DATA` object contains all economic data points for all 3 countries, organized by country then metric. Each metric is an array of `{date, value}` objects. Data sourced from BEA, BLS, FRED, INDEC, NBS China, IMF, and World Bank.
- **Country Metadata**: `COUNTRY_META` maps country keys (US, ARG, CHN) to display names, flags, and accent colors.
- **Dashboard Metrics**: `DASHBOARD_METRICS` array defines the 5 metrics displayed: GDP growth, CPI inflation, unemployment, exchange rate, and interest rate.
- **React Components**: `Sparkline`, `ComparisonChart`, `MetricCard`, `CountryPanel`, `App`.

**Views:** Overview (summary table), per-country deep dive (metric cards with sparklines), cross-country comparison (overlay line chart with metric selector), and Sources (linked references for all data).

## Design Decisions

- All data is hardcoded as static values (as of March 2026) rather than fetched from live APIs, ensuring consistent and comparable data across all 3 countries.
- The US "exchange rate" metric uses the broad USD trade-weighted index, not a bilateral rate.
- Argentina interest rate is the BCRA overnight repo rate; China uses the 1-Year Loan Prime Rate (LPR).
- Visual design is FRED-inspired: light theme, white cards on a light gray page, FRED dark blue (`#0a3052`) brand bar with a `#2272b9` accent. Country series colors are FRED-style (US blue, Argentina red, China green).
- Typography: Source Serif 4 for titles, Source Sans 3 for body, JetBrains Mono for numerics. All styling lives in CSS custom properties on `:root` plus a small set of `.fred-*` utility classes in the `<style>` block.
