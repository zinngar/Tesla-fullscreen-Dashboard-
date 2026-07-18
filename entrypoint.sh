#!/bin/sh

# Ensure the destination directory exists
mkdir -p /config/plugins/TeslaFullscreen

# Copy the build artifacts from the staging area to the plugins folder
cp -f /app/plugins/TeslaFullscreen/* /config/plugins/TeslaFullscreen/

# Ensure correct file permissions so Jellyfin can load them without permissions errors
chmod 644 /config/plugins/TeslaFullscreen/* 2>/dev/null || true
chmod 755 /config/plugins/TeslaFullscreen 2>/dev/null || true

# Hand over to the standard Jellyfin executable
exec /jellyfin/jellyfin "$@"
