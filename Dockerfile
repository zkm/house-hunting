FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Pillow and a web server
RUN apt-get update && apt-get install -y \
    zlib1g-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY address.json .
COPY marker.png .
COPY map.html .

# Create .env file (users should override with their own)
RUN echo "GEOCODING_API_KEY=" > .env && \
    echo "GOOGLE_MAPS_API_KEY=" >> .env

# Run the app (optional geocoding) and start a web server
CMD sh -c "python app.py || true && python3 -m http.server 8000 --directory /app/output"
