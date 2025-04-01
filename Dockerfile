#### Use a lightweight Alpine-based image
FROM alpine:3.14

# Set the working directory
WORKDIR /app

# Install required packages (Python for web server, Bash for debugging, Curl for health checks)
RUN apk add --no-cache python3 bash curl

# Create a test HTML file
RUN echo '<html><body><h1>Hello from 2RBC-AI Container 2 from CSO</h1></body></html>' > /app/index.html

# Create a health check endpoint
RUN mkdir -p /app/health
RUN echo "OK" > /app/health/index.html

# Copy a simple startup script
COPY start.sh /app/
RUN chmod +x /app/start.sh
COPY . . 
# Expose port 8000
EXPOSE 8000

# Add HEALTHCHECK (Kubernetes Liveness and Readiness)
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5040/health/index.html || exit 1

# Start web server and keep the container running
CMD ["/app/start.sh"]

