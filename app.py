import requests
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEOCODIO_API_KEY = os.getenv("GEOCODING_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# Load the list of addresses from address.json
with open('address.json') as f:
    addresses = json.load(f)


def geocode_geocodio(address):
    url = f'https://api.geocod.io/v1.7/geocode?q={address}&api_key={GEOCODIO_API_KEY}'
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        print(data)  # Print the data for debugging purposes

        results = data.get('results')
        if results:
            latitude = results[0]['location']['lat']
            longitude = results[0]['location']['lng']
            return latitude, longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return None, None


def geocode_nominatim(address):
    # Free fallback used when GEOCODING_API_KEY isn't set. No key required, but
    # usage policy caps requests at 1/sec and requires an identifying User-Agent:
    # https://operations.osmfoundation.org/policies/nominatim/
    url = 'https://nominatim.openstreetmap.org/search'
    headers = {'User-Agent': 'house-hunting-app (https://github.com/zkm/house-hunting)'}
    params = {'q': address, 'format': 'json', 'limit': 1}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        results = response.json()
        print(results)  # Print the data for debugging purposes

        if results:
            return float(results[0]['lat']), float(results[0]['lon'])
        else:
            return None, None
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return None, None
    finally:
        time.sleep(1)


# Geocode function to get latitude and longitude
def geocode(address):
    if GEOCODIO_API_KEY:
        return geocode_geocodio(address)
    return geocode_nominatim(address)


# Function to generate the markers script for the HTML
def generateMarkersScript(locations):
    script = ''
    for i, location in enumerate(locations):
        lat = location['lat']
        lng = location['lng']
        if GOOGLE_MAPS_API_KEY:
            script += f"var marker{i+1} = new google.maps.Marker({{position: {{ lat: {lat}, lng: {lng} }}, map: map}});\n"
        else:
            script += f"L.marker([{lat}, {lng}]).addTo(map);\n"
    return script


# Function to generate the sidebar HTML with Zillow links
def generateSidebar(locations):
    sidebar = ''
    for i, location in enumerate(locations):
        address = location['address']
        zillow_link = f'https://www.zillow.com/homes/{address}'
        sidebar += (
            f"<a class='address-card' href='{zillow_link}' target='_blank'>"
            f"<span class='index'>{i + 1}</span><span>{address}</span></a>\n"
        )
    return sidebar


if GEOCODIO_API_KEY:
    print("Using Geocodio for geocoding")
else:
    print("GEOCODING_API_KEY not set - falling back to free Nominatim (OpenStreetMap) geocoding")

if GOOGLE_MAPS_API_KEY:
    print("Using Google Maps for the interactive map")
else:
    print("GOOGLE_MAPS_API_KEY not set - falling back to free Leaflet/OpenStreetMap map")

# Geocode every address
locations = []
for address in addresses:
    latitude, longitude = geocode(address)
    if latitude is not None and longitude is not None:
        locations.append({'lat': latitude, 'lng': longitude, 'address': address})

print(f"Geocoded {len(locations)} of {len(addresses)} addresses")

# Shared stylesheet for the generated pages
styles_css = '''
:root {
    --color-bg: #f8fafc;
    --color-surface: #ffffff;
    --color-border: #e2e8f0;
    --color-text: #1e293b;
    --color-text-muted: #64748b;
    --color-primary: #2563eb;
    --color-primary-hover: #1d4ed8;
    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --radius: 8px;
    --shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: var(--font-sans);
    color: var(--color-text);
    background: var(--color-bg);
}

a {
    color: var(--color-primary);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 1rem 1.5rem;
    background: var(--color-surface);
    border-bottom: 1px solid var(--color-border);
}

.header h1 {
    font-size: 1.125rem;
    margin: 0;
}

.badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    background: #eff6ff;
    color: var(--color-primary);
    font-size: 0.8125rem;
    font-weight: 600;
    white-space: nowrap;
}

.layout {
    display: flex;
    height: calc(100vh - 57px);
}

#map {
    flex: 1;
}

#sidebar {
    width: 320px;
    overflow-y: auto;
    background: var(--color-surface);
    border-left: 1px solid var(--color-border);
}

.address-card {
    display: flex;
    gap: 0.75rem;
    align-items: baseline;
    padding: 0.875rem 1.25rem;
    border-bottom: 1px solid var(--color-border);
    font-size: 0.875rem;
    color: var(--color-text);
}

.address-card:hover {
    background: var(--color-bg);
    text-decoration: none;
}

.address-card .index {
    color: var(--color-text-muted);
    font-variant-numeric: tabular-nums;
    flex-shrink: 0;
}

body.landing-body {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
    background: radial-gradient(circle at 50% 0%, #eaf0ff 0%, var(--color-bg) 55%);
}

.landing {
    width: 100%;
    max-width: 440px;
    margin: 0;
    padding: 2.75rem 2.25rem;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: 20px;
    box-shadow: 0 20px 40px -20px rgba(15, 23, 42, 0.25);
    text-align: center;
}

.landing .icon {
    width: 56px;
    height: 56px;
    margin: 0 auto 1.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #eff6ff;
    font-size: 1.75rem;
}

.landing h1 {
    margin: 0 0 0.5rem;
    font-size: 1.75rem;
    letter-spacing: -0.02em;
}

.landing .subtitle {
    margin: 0 0 1.75rem;
    color: var(--color-text-muted);
    font-size: 0.9375rem;
    line-height: 1.5;
}

.stats {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
    margin: 0 0 2rem;
}

.button {
    display: inline-block;
    padding: 0.75rem 1.75rem;
    border-radius: var(--radius);
    background: var(--color-primary);
    color: #fff;
    font-weight: 600;
    font-size: 0.9375rem;
    box-shadow: 0 1px 2px rgba(37, 99, 235, 0.35);
    transition: background 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
}

.button:hover {
    background: var(--color-primary-hover);
    box-shadow: 0 8px 16px -4px rgba(37, 99, 235, 0.45);
    transform: translateY(-1px);
    text-decoration: none;
}
'''

with open('output/styles.css', 'w', encoding='utf-8') as f:
    f.write(styles_css)

# Generate the interactive map HTML
if locations:
    center_lat = locations[0]['lat']
    center_lng = locations[0]['lng']
else:
    # Default to center of US
    center_lat = 39.8283
    center_lng = -98.5795

if GOOGLE_MAPS_API_KEY:
    map_head = ''
    map_body_script = f'''
    <script>
        function initMap() {{
            var map = new google.maps.Map(document.getElementById('map'), {{
                center: {{ lat: {center_lat}, lng: {center_lng} }},
                zoom: 8
            }});

            {generateMarkersScript(locations)}
        }}
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&callback=initMap" async defer></script>'''
else:
    map_head = '''<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'''
    map_body_script = f'''
    <script>
        var map = L.map('map').setView([{center_lat}, {center_lng}], 8);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; OpenStreetMap contributors',
            maxZoom: 19
        }}).addTo(map);

        {generateMarkersScript(locations)}
    </script>'''

html = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>Geocoded Addresses</title>
    <link rel="stylesheet" href="styles.css" />
    {map_head}
</head>
<body>
    <header class="header">
        <h1>House Hunting</h1>
        <span class="badge">{len(locations)} locations</span>
    </header>
    <div class="layout">
        <div id="map"></div>
        <aside id="sidebar">
            {generateSidebar(locations)}
        </aside>
    </div>
    {map_body_script}
</body>
</html>
'''

# Save the HTML file
with open('output/map.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML map saved")

# Landing page served by default at http://host:8000/, linking to the interactive map
geocoder_name = "Geocodio" if GEOCODIO_API_KEY else "Nominatim (OpenStreetMap)"
map_provider_name = "Google Maps" if GOOGLE_MAPS_API_KEY else "Leaflet (OpenStreetMap)"

index_html = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>House Hunting</title>
    <link rel="stylesheet" href="styles.css" />
</head>
<body class="landing-body">
    <div class="landing">
        <div class="icon">📍</div>
        <h1>House Hunting</h1>
        <p class="subtitle">Addresses from address.json, geocoded and plotted on an interactive map.</p>
        <div class="stats">
            <span class="badge">{len(locations)} of {len(addresses)} geocoded</span>
            <span class="badge">{geocoder_name}</span>
            <span class="badge">{map_provider_name}</span>
        </div>
        <a class="button" href="map.html">Open interactive map &rarr;</a>
    </div>
</body>
</html>
'''

with open('output/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
print("Landing page saved")
