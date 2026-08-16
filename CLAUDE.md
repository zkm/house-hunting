# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A small Python script (`app.py`) that geocodes a list of home addresses (`address.json`) via the Geocodio API, plots them as markers on a static image (`marker.png` overlaid on a blank canvas), and generates an interactive Google Maps HTML page with a sidebar of clickable Zillow links for each address.

## Commands

Setup:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Requires a `.env` file (not committed) with:
```
GEOCODING_API_KEY=<geocodio_api_key>
GOOGLE_MAPS_API_KEY=<google_maps_js_api_key>
```
`env.txt` is a placeholder template for this — copy it to `.env` and fill in real keys.

Run the app (reads `address.json`, writes to `output/`):
```bash
python app.py
```

Lint (as run in CI):
```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

There are no test files in this repo yet; CI runs `pytest` with `continue-on-error: true`, so it currently passes vacuously.

Run via Docker:
```bash
docker compose up --build
```
This builds the image, runs `app.py` once (geocoding failures are swallowed via `|| true`), then serves `output/` over `python3 -m http.server 8000`. View the generated map at `http://localhost:8000/map.html`.

## Architecture

Everything lives in the single `app.py` script, run top-to-bottom (no functions besides the small `geocode`, `generateMarkersScript`, and `generateSidebar` helpers):

1. Load `address.json` (a flat JSON array of address strings).
2. For each address, call the Geocodio API (`geocode()`) to get lat/lng.
3. Convert each lat/lng to x/y pixel coordinates on an 800x600 blank canvas using an equirectangular projection, and paste `marker.png` at that position — written to `output/output.png`.
4. Build an HTML page embedding the Google Maps JavaScript API, with one `google.maps.Marker` per geocoded address and a sidebar `<div>` linking each address to a Zillow search URL — written to `output/map.html`.

Two `map.html`-named files exist and are easy to confuse:
- `./map.html` (repo root) is a static, committed **example template** showing the expected structure/styling with placeholder markers — it is not read or written by `app.py`.
- `output/map.html` is the actual generated map from the last `app.py` run; the `output/` directory is gitignored.

`docker-compose.yml` mounts `./address.json` and `./output` into the container, and (separately) `./map.html` — but since `app.py` only ever writes to `output/map.html`, the mounted root `map.html` is not what gets served.

The Geocodio API key and Google Maps API key are both required — the former to resolve addresses server-side, the latter is embedded directly into the generated HTML's `<script src>` tag to render the interactive map client-side.
