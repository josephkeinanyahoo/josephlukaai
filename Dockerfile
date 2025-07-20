# Use a more recent Python slim image for smaller footprint and security
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for mysql-connector-python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .


# Expose port for FastAPI
EXPOSE 6007

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6007"]
