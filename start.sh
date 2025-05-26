#!/bin/sh

echo "Starting Python HTTP server on port 6007..."
exec python3 -m http.server 6007 --directory /app

