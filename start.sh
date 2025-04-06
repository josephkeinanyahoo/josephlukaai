#!/bin/sh

echo "Starting Python HTTP server on port 6005..."
exec python3 -m http.server 6005 --directory /app

