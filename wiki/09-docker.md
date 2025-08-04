# 🐳 Docker

## 🎯 Przegląd

Docker umożliwia uruchomienie ChatGPT Bot w kontenerze, zapewniając izolację, przenośność i łatwość wdrażania. Projekt obsługuje zarówno pojedyncze kontenery, jak i orkiestrację z docker-compose.

## 📦 Dockerfile

### API Server Dockerfile
```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 chatgpt && chown -R chatgpt:chatgpt /app
USER chatgpt

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "chatgpt_api_server.py"]
```

### Multi-stage Dockerfile (Optimized)
```dockerfile
# Build stage
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# Copy Python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 chatgpt && chown -R chatgpt:chatgpt /app
USER chatgpt

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "chatgpt_api_server.py"]
```

## 🐙 Docker Compose

### Basic docker-compose.yml
```yaml
version: '3.8'

services:
  chatgpt-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - DEBUG=false
    volumes:
      - ./data:/app/data
      - /dev/shm:/dev/shm
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Production docker-compose.yml
```yaml
version: '3.8'

services:
  chatgpt-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - DEBUG=false
      - MAX_SESSIONS=20
      - SESSION_TIMEOUT=7200
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - /dev/shm:/dev/shm
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - chatgpt-api
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

### Development docker-compose.yml
```yaml
version: '3.8'

services:
  chatgpt-api-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - DEBUG=true
      - RELOAD=true
    volumes:
      - .:/app
      - /dev/shm:/dev/shm
    restart: unless-stopped
    command: ["uvicorn", "chatgpt_api_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

## 🚀 Uruchomienie

### Podstawowe komendy

#### Build i uruchomienie
```bash
# Build image
docker build -t chatgpt-bot-api .

# Run container
docker run -d \
  --name chatgpt-bot \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  --shm-size=2g \
  chatgpt-bot-api
```

#### Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Skrypty uruchomieniowe

#### start-docker.sh (Linux/macOS)
```bash
#!/bin/bash

echo "🐳 Starting ChatGPT Bot with Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose."
    exit 1
fi

# Create data directory if it doesn't exist
mkdir -p data logs

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ ChatGPT Bot API is running!"
    echo "📖 API Documentation: http://localhost:8000/docs"
    echo "🔍 Health Check: http://localhost:8000/health"
else
    echo "❌ Service failed to start. Check logs:"
    docker-compose logs
fi
```

#### start-docker.bat (Windows)
```batch
@echo off
echo 🐳 Starting ChatGPT Bot with Docker...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Create data directory
if not exist "data" mkdir data
if not exist "logs" mkdir logs

REM Start services
echo 🚀 Starting services...
docker-compose up -d

REM Wait for services
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check health
curl -f http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Service failed to start. Check logs:
    docker-compose logs
) else (
    echo ✅ ChatGPT Bot API is running!
    echo 📖 API Documentation: http://localhost:8000/docs
    echo 🔍 Health Check: http://localhost:8000/health
)

pause
```

## 🔧 Konfiguracja

### Environment Variables
```bash
# .env file
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
MAX_SESSIONS=10
SESSION_TIMEOUT=3600
HEADLESS_DEFAULT=true
BROWSER_TIMEOUT=30

# Chrome options
CHROME_NO_SANDBOX=true
CHROME_DISABLE_DEV_SHM=true
CHROME_DISABLE_GPU=true
```

### Volume Mounts
```yaml
volumes:
  # Application data
  - ./data:/app/data
  
  # Logs
  - ./logs:/app/logs
  
  # Shared memory for Chrome
  - /dev/shm:/dev/shm
  
  # Configuration
  - ./config:/app/config
  
  # SSL certificates (if needed)
  - ./ssl:/app/ssl
```

## 🛡️ Security

### Non-root User
```dockerfile
# Create non-root user
RUN useradd -m -u 1000 chatgpt && chown -R chatgpt:chatgpt /app
USER chatgpt
```

### Security Options
```yaml
services:
  chatgpt-api:
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - SYS_ADMIN  # Required for Chrome
    read_only: true
    tmpfs:
      - /tmp
      - /var/tmp
```

### Secrets Management
```yaml
services:
  chatgpt-api:
    secrets:
      - api_key
      - ssl_cert
      - ssl_key

secrets:
  api_key:
    file: ./secrets/api_key.txt
  ssl_cert:
    file: ./secrets/ssl_cert.pem
  ssl_key:
    file: ./secrets/ssl_key.pem
```

## 📊 Monitoring

### Health Checks
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Logging
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### Metrics Collection
```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

## 🔄 CI/CD Integration

### GitHub Actions
```yaml
name: Docker Build and Deploy

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: docker build -t chatgpt-bot-api .
    
    - name: Test Docker image
      run: |
        docker run -d --name test-container -p 8000:8000 chatgpt-bot-api
        sleep 30
        curl -f http://localhost:8000/health
        docker stop test-container
    
    - name: Push to registry
      if: github.ref == 'refs/heads/main'
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker tag chatgpt-bot-api ${{ secrets.DOCKER_USERNAME }}/chatgpt-bot-api:latest
        docker push ${{ secrets.DOCKER_USERNAME }}/chatgpt-bot-api:latest
```

## 🚀 Production Deployment

### Docker Swarm
```yaml
version: '3.8'

services:
  chatgpt-api:
    image: chatgpt-bot-api:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    ports:
      - "8000:8000"
    networks:
      - chatgpt-network

networks:
  chatgpt-network:
    driver: overlay
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chatgpt-bot-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: chatgpt-bot-api
  template:
    metadata:
      labels:
        app: chatgpt-bot-api
    spec:
      containers:
      - name: chatgpt-bot-api
        image: chatgpt-bot-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: API_HOST
          value: "0.0.0.0"
        - name: API_PORT
          value: "8000"
        resources:
          limits:
            memory: "2Gi"
            cpu: "1000m"
          requests:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: chatgpt-bot-api-service
spec:
  selector:
    app: chatgpt-bot-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## 🧹 Maintenance

### Cleanup Scripts
```bash
#!/bin/bash
# cleanup-docker.sh

echo "🧹 Cleaning up Docker resources..."

# Stop and remove containers
docker-compose down

# Remove unused images
docker image prune -f

# Remove unused volumes
docker volume prune -f

# Remove unused networks
docker network prune -f

echo "✅ Cleanup completed!"
```

### Backup Scripts
```bash
#!/bin/bash
# backup-data.sh

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📦 Creating backup..."

# Backup data directory
tar -czf "$BACKUP_DIR/data.tar.gz" ./data

# Backup logs
tar -czf "$BACKUP_DIR/logs.tar.gz" ./logs

# Backup configuration
cp docker-compose.yml "$BACKUP_DIR/"
cp .env "$BACKUP_DIR/"

echo "✅ Backup created in $BACKUP_DIR"
```