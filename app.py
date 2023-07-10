from PIL import Image, ImageDraw
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

    response = requests.get(url)
    data = response.json()
    print(data)  # Print the data for debugging purposes

    results = data.get('results')
    if results:
        latitude = results[0]['location']['lat']
        longitude = results[0]['location']['lng']
        return latitude, longitude
    else:
        return None, None


# Function to generate the markers script for the HTML
def generateMarkersScript(locations):
    script = ''
    for i, location in enumerate(locations):
        lat = location['lat']
        lng = location['lng']
        script += f"var marker{i+1} = new google.maps.Marker({{position: {{ lat: {lat}, lng: {lng} }}, map: map}});\n"
    return script


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
        locations.append({'lat': latitude, 'lng': longitude})

# Save the final image
image.save('output.png')

# Generate the HTML file
html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Geocoded Addresses</title>
    <style>
        #map {{
            height: 600px;
            width: 800px;
        }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        function initMap() {{
            var map = new google.maps.Map(document.getElementById('map'), {{
                center: {{ lat: {locations[0]['lat']}, lng: {locations[0]['lng']} }},
                zoom: 8
            }});

            {generateMarkersScript(locations)}
        }}
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap" async defer></script>
</body>
</html>
'''

# Replace 'YOUR_API_KEY' with your actual Google Maps API key in the HTML code
html = html.replace('YOUR_API_KEY', os.getenv("GOOGLE_MAPS_API_KEY"))

# Save the HTML file
with open('map.html', 'w') as f:
    f.write(html)
