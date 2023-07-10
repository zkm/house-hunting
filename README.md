# House Hunting App

The House Hunting App is a Python application that allows you to geocode a list of addresses and display them on a map using the Geocodio API and Google Maps API.

## Prerequisites

Before running the app, make sure you have the following:

- Python 3.6 or higher installed
- API keys for Geocodio and Google Maps

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>

2. Install the required packages using pip:
   ```bash
   pip install -r requirements.txt

3. Replace the placeholders in the .env file with your actual API keys:
   ```bash
    GEOCODING_API_KEY=<your_geocodio_api_key>
    GOOGLE_MAPS_API_KEY=<your_google_maps_api_key>

## Usage
1. Add the addresses you want to geocode to the address.json file. The file should contain an array of address strings.

2. Run the app:
   ```bash
   python app.py

3. The geocoded addresses will be displayed in the terminal, and a map with markers will be saved as output.html.

## File Structure
The file structure of the project should look like this:
   ```bash
   .
   ├── app.py
   ├── address.json
   ├── marker.png
   ├── output.html
   ├── requirements.txt
   └── .env
   
   * app.py: The main Python script that geocodes the addresses and generates the map.
   * address.json: JSON file containing the list of addresses to geocode.
   * marker.png: Image file of the marker to be placed on the map.
   * output.html: The generated HTML file displaying the map with markers.
   * requirements.txt: Text file specifying the required Python packages.
   * .env: Environment file containing the API keys.
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
Feel free to modify the file as needed and include any additional information you want to provide to users.

