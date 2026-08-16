# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A small Python script (`app.py`) that geocodes a list of home addresses (`address.json`), then generates a static site in `output/`: a landing page (`index.html`), an interactive map with a sidebar of clickable Zillow links (`map.html`), and a shared stylesheet (`styles.css`).

Both the geocoder and the map provider are optional — the script works with zero API keys, falling back to free services, and upgrades automatically when keys are present.

## Commands

Setup:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optionally create a `.env` file (not committed) to use paid providers instead of the free fallbacks:
```
GEOCODING_API_KEY=<geocodio_api_key>
GOOGLE_MAPS_API_KEY=<google_maps_js_api_key>
```
`env.txt` is a placeholder template for this — copy it to `.env` and fill in real keys. Without it, geocoding uses Nominatim (OpenStreetMap) and the map uses Leaflet (OpenStreetMap tiles) — see Architecture below.

Run the app (reads `address.json`, writes to `output/`):
```bash
python app.py
```

Lint (as run in CI):
```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

CI (`.github/workflows/ci.yml`) runs this lint plus `pytest` on Python 3.9/3.10/3.11 for every push/PR to `main`/`develop`. There are no test files in this repo yet, and pytest runs with `continue-on-error: true`, so the test step currently passes vacuously.

Run via Docker:
```bash
docker compose up --build
```
This builds the image, runs `app.py` once (`|| true` swallows any failure, e.g. missing `address.json`), then serves `output/` over `python3 -m http.server 8000`. Visit `http://localhost:8000/` for the landing page, or go straight to `http://localhost:8000/map.html`.

## Architecture

Everything lives in the single `app.py` script, run top-to-bottom (no functions besides a few small helpers: `geocode_geocodio`, `geocode_nominatim`, `geocode`, `generateMarkersScript`, `generateSidebar`).

1. Load `address.json` (a flat JSON array of address strings).
2. For each address, call `geocode()` to get lat/lng. This dispatches to `geocode_geocodio()` if `GEOCODING_API_KEY` is set, otherwise to `geocode_nominatim()` (free, no key, but rate-limited to 1 request/sec per Nominatim's usage policy — enforced with a `time.sleep(1)`).
3. Build `output/map.html`: an HTML page with a sidebar `<div>` linking each geocoded address to a Zillow search URL, plus a map. If `GOOGLE_MAPS_API_KEY` is set, it embeds the Google Maps JavaScript API with one `google.maps.Marker` per address; otherwise it embeds Leaflet against OpenStreetMap tiles with `L.marker(...)`. `generateMarkersScript()` emits whichever marker code matches the active provider.
4. Write `output/styles.css`, a shared stylesheet used by both generated pages.
5. Build `output/index.html`, a landing page showing how many addresses geocoded successfully and which geocoder/map provider was used, linking to `map.html`.

There is no longer any static-image rendering step (no `marker.png` overlay, no `output.png`) — that was removed; the map is HTML-only now.

Two `map.html`-named files exist and are easy to confuse:
- `./map.html` (repo root) is a static, committed **example template** showing the expected structure/styling with placeholder markers and a hardcoded Google Maps script tag — it is not read or written by `app.py`.
- `output/map.html` is the actual generated map from the last `app.py` run; the `output/` directory is gitignored.

The Dockerfile bakes an empty `.env` into the image (both keys blank), so a container run with no mounted `.env`/env vars uses the free Nominatim + Leaflet path by default.
