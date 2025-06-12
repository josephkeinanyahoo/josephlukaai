# Use a lightweight Alpine-based image
FROM alpine:3.14

# Set the working directory
WORKDIR /app

# Install required packages including pip and pymysql dependencies
RUN apk add --no-cache \
    python3 py3-pip bash curl \
    gcc python3-dev musl-dev \
    mariadb-connector-c-dev \
    libffi-dev

# Upgrade pip and install Python packages
RUN pip3 install --upgrade pip
RUN pip3 install pymysql cryptography==3.4.8

# Create a test HTML file
RUN echo '<html><body><h1>Hello Keren tsdokk  2RBC-AI- SingleRepo you have subscribe to PLAN A - Container 2 from CSO +2</h1></body></html>' > /app/index.html

# Create a health check endpoint
RUN mkdir -p /app/health
RUN echo "OK" > /app/health/index.html

# Copy the test script
COPY test_vault_db.py /app/
RUN chmod +x /app/test_vault_db.py

# Copy a simple startup script
COPY start.sh /app/
RUN chmod +x /app/start.sh

# Copy everything else
COPY . .

EXPOSE 6007

# Set the startup command
CMD ["/app/start.sh"]
