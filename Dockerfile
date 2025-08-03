# ChatGPT Bot - Docker Container
# Multi-stage build for optimized image size
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DISPLAY=:99 \
    DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg2 \
    unzip \
    curl \
    xvfb \
    x11vnc \
    fluxbox \
    supervisor \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome - updated method
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/* \
    && rm /etc/apt/sources.list.d/google.list

# Production stage
FROM base as production

# Copy requirements first for better Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directories for data persistence
RUN mkdir -p /app/data /app/logs /app/sessions

# Make scripts executable
RUN chmod +x *.sh 2>/dev/null || true

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash chatgpt && \
    chown -R chatgpt:chatgpt /app && \
    mkdir -p /home/chatgpt/.cache && \
    chown -R chatgpt:chatgpt /home/chatgpt

# Copy supervisor configuration
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Switch to non-root user
USER chatgpt

# Create Chrome user data directory
RUN mkdir -p /home/chatgpt/.config/google-chrome

# Expose ports
EXPOSE 8000 5900

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Use supervisor to manage multiple processes
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

# Development stage
FROM base as development

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies including dev tools
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pytest black flake8 ipython jupyter

# Copy application files
COPY . .

# Make scripts executable
RUN chmod +x *.sh 2>/dev/null || true

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash chatgpt && \
    chown -R chatgpt:chatgpt /app

USER chatgpt

# Development command
CMD ["python", "chatgpt_api_server.py"]
