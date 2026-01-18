FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    binutils libproj-dev gdal-bin libgdal-dev python3-gdal \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .