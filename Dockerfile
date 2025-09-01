# Use a Python 3.9.6 slim buster base image
FROM python:3.10.13-slim

# Update and install dependencies using apt
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        gcc \
        libffi-dev \
        musl-dev \
        ffmpeg \
        aria2 \
        make \
        g++ \
        cmake \
        wget \
        unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy all files into the container
COPY . /app/
WORKDIR /app/

# Python dependencies install
RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir --upgrade --requirement requirements.txt \
    && python3 -m pip install -U yt-dlp \
    && pip3 install pytube

# Set the command to run the application
CMD gunicorn app:app & python3 main.py
