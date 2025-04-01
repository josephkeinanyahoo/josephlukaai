#!/bin/sh

echo "Starting Python HTTP server on port 6001..."
exec python3 -m http.server 6002 --directory /app

