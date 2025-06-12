#!/bin/bash

# Run the Vault database test
echo "Running Vault database test..."
python3 /app/test_vault_db.py

# Start the web server
echo "Starting web server on port 6007..."
cd /app && python3 -m http.server 6007
