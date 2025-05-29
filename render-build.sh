#!/usr/bin/env bash

# Step 1: Install Python packages
pip install -r requirements.txt

# Step 2: Download ffmpeg from evermeet.cx
mkdir -p Bin/ffmpeg
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJ --strip-components=1 -C Bin/ffmpeg

# Optional: show ffmpeg version to verify
Bin/ffmpeg/ffmpeg -version
