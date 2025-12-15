from PIL import Image, ImageDraw
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# Load the list of addresses from address.json
with open('address.json') as f:
    addresses = json.load(f)

# Create a blank image
image = Image.new('RGB', (800, 600), (255, 255, 255))
draw = ImageDraw.Draw(image)

# Load the map marker image
marker_image = Image.open('marker.png')

# Geocode function to get latitude and longitude
def geocode(address):
    api_key = os.getenv("GEOCODING_API_KEY")
    url = f'https://api.geocod.io/v1.7/geocode?q={address}&api_key={api_key}'

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


# Function to generate the markers script for the HTML
def generateMarkersScript(locations):
    script = ''
    for i, location in enumerate(locations):
        lat = location['lat']
        lng = location['lng']
        script += f"var marker{i+1} = new google.maps.Marker({{position: {{ lat: {lat}, lng: {lng} }}, map: map}});\n"
    return script


# Function to generate the sidebar HTML with Zillow links
def generateSidebar(locations):
    sidebar = ''
    for i, location in enumerate(locations):
        address = location['address']
        zillow_link = f'https://www.zillow.com/homes/{address}'
        sidebar += f"<div class='address'><a href='{zillow_link}' target='_blank'>{address}</a></div>\n"
    return sidebar


# Iterate over the addresses and place a marker on the image
locations = []
for address in addresses:
    latitude, longitude = geocode(address)
    if latitude is not None and longitude is not None:
        # Calculate the marker position on the image
        x = int((longitude + 180) * (image.width / 360))
        y = int((90 - latitude) * (image.height / 180))

        # Paste the marker image onto the image
        marker_width, marker_height = marker_image.size
        x -= marker_width // 2
        y -= marker_height // 2
        image.paste(marker_image, (x, y), marker_image)

        # Draw a circle around the marker
        draw.ellipse([(x - 5, y - 5), (x + 5, y + 5)], outline=(255, 0, 0))

        # Store the location data
        locations.append({'lat': latitude, 'lng': longitude, 'address': address})

# Save the final image
image.save('output/output.png')
print(f"Image saved with {len(locations)} locations")

# Generate the HTML file
if locations:
    center_lat = locations[0]['lat']
    center_lng = locations[0]['lng']
else:
    # Default to center of US
    center_lat = 39.8283
    center_lng = -98.5795

html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Geocoded Addresses</title>
    <style>
        body {{
            display: flex;
            flex-direction: row;
            font-family: Lucida Console,Lucida Sans Typewriter,monaco,Bitstream Vera Sans Mono,monospace; 
            font-size: .75rem;
            margin: 0;
            padding: 0;
        }}

        a {{
            color: #337ab7;
            text-decoration: none;
        }}

        a:hover {{
            color: #337ab7;
            font-weight: bold;
            font-size: 1em;
        }}

        #map {{
            flex: 1;
            height: 600px;
            width: 800px;
        }}

        #sidebar {{
            width: 200px;
            height: 600px;
            overflow-y: scroll;
            padding: 0;
            box-sizing: border-box;
        }}

        .address {{
            padding: 1em;
        }}
        .address:nth-child(even) {{
            background-color: #fcfcfc;
        }}

        .address:nth-child(odd) {{
            background-color: #ccc;
        }}
    </style>
</head>
<body>
    <div id="map"></div>
    <div id="sidebar">
        {generateSidebar(locations)}
    </div>
    <script>
        function initMap() {{
            var map = new google.maps.Map(document.getElementById('map'), {{
                center: {{ lat: {center_lat}, lng: {center_lng} }},
                zoom: 8
            }});

            {generateMarkersScript(locations)}
        }}
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key={os.getenv("GOOGLE_MAPS_API_KEY")}&callback=initMap" async defer></script>
</body>
</html>
'''

# Save the HTML file
with open('output/map.html', 'w') as f:
    f.write(html)
print("HTML map saved")
