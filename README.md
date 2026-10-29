
# House Hunting App

[![CI](https://github.com/zkm/house-hunting/actions/workflows/ci.yml/badge.svg)](https://github.com/zkm/house-hunting/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

![Python 3.10–3.11](https://img.shields.io/badge/Python-3.10%E2%80%933.11-3776AB?logo=python&logoColor=white)
![Geocodio](https://img.shields.io/badge/Geocodio-5A5A5A)
![Google Maps](https://img.shields.io/badge/Google%20Maps-4285F4?logo=googlemaps&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

The House Hunting App is a Python application that geocodes a list of addresses and displays them on both a static image and an interactive Google Map. It uses the **Geocodio API** for geocoding and the **Google Maps JavaScript API** for interactive visualization.

---

## 🚀 Features

- Converts addresses to geographic coordinates using Geocodio  
- Overlays custom markers on a static image map  
- Generates a styled interactive map with clickable Zillow links  
- Outputs both a `.png` image and an `.html` map

---

## 📦 Prerequisites

Before running the app, make sure you have:

- Python 3.6 or higher
- API keys for:
  - [Geocodio](https://www.geocod.io/)
  - [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/get-api-key)

---

## 🔧 Installation

1. **Clone the repository**

   ```bash
   git clone <repository_url>
   cd house-hunting
   ```

2. **(Optional) Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   pip install python-dotenv
   ```

4. **Set your API keys in a `.env` file**

   Create a file called `.env` and add the following:

   ```env
   GEOCODING_API_KEY=your_geocodio_api_key
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   ```

---

## ▶️ Usage

1. **Edit `address.json`**

   Add the addresses you want to geocode. Example:

   ```json
   [
     "1600 Pennsylvania Ave NW, Washington, DC 20500",
     "1 Infinite Loop, Cupertino, CA 95014"
   ]
   ```

2. **Run the application**

   ```bash
   python app.py
   ```

3. **View the outputs**

   - A static image map will be saved as `output.png`
   - An interactive map will be saved as `map.html` — open it in a browser

4. **Open the map**

   After running the script, open `map.html` in your web browser to view the interactive map:

   ```bash
   xdg-open map.html    # Linux
   open map.html        # macOS
   start map.html       # Windows

---

## 📁 File Structure

```bash
.
├── address.json         # List of input addresses
├── app.py               # Main Python script
├── env.txt              # (optional) Environment variable placeholder
├── LICENSE              # MIT license
├── map.html             # Generated interactive map with markers
├── marker.png           # Custom marker image for plotting
├── output.png           # Generated static image with plotted markers
├── README.md            # You're reading it!
├── requirements.txt     # Python dependencies
└── .env                 # API keys (not committed to Git)
```

## 📝 License

This project is licensed under the MIT License. See the [MIT License](https://github.com/zkm/house-hunting?tab=MIT-1-ov-file) file for details.
