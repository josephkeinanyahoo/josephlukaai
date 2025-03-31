#!/bin/sh

echo "Starting Python HTTP server on port 5003..."
exec python3 -m http.server 5003 --directory /app

