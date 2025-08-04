# ChatGPT Bot - Docker for Windows

## 🚀 Quick Start

### Requirements
- Windows 10/11
- Docker Desktop for Windows
- Git (optional)

### Installing Docker Desktop
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop/
2. Install and run Docker Desktop
3. Make sure Docker is running (the whale icon in the system tray)

## 📁 Windows Files

The project contains the following Windows files:

### Basic Scripts
- `start-docker.bat` - Quick Start (basic configuration)
- `stop-docker.bat` - Stop all services
- `build-docker.bat` - Build Docker images
- `docker-manager.bat` - Full Docker Manager (all options)

## 🎯 Usage

### Option 1: Quick Starting
```batch
REM Start the project
start-docker.bat

REM Stop the project
stop-docker.bat
```

### Option 2: Docker Manager
```batch
REM Start the interactive manager
docker-manager.bat
```

### Option 3: Manually via PowerShell/CMD
```batch
REM Basic start
docker-compose up -d

REM Start with monitoring
docker-compose --profile monitoring up -d

REM Stopping
docker-compose down
```

## 🌐 Accessing services

After starting, the following are available:

| Service | URL | Description |
|--------|------|------|
| **API** | http://localhost:8000 | ChatGPT Bot Main API |
| **Documentation** | http://localhost:8000/docs | Swagger UI |
| **VNC** | localhost:5900 | GUI Access (Passwordless) |
| **Health Check** | http://localhost:8000/ | API Status |

### Additional Services (with Profiles)
| Service | URL | Profile |
|--------|--------|--------|
| **Nginx** | http://localhost:80 | `--profile nginx` |
| **Redis** | localhost:6379 | `--profile redis` |
| **PostgreSQL** | localhost:5432 | `--profile database` |
| **Prometheus** | http://localhost:9090 | `--profile monitoring` |
| **Grafana** | http://localhost:3000 | `--profile monitoring` |

## 🖥️ VNC - GUI Access

### VNC Clients for Windows
1. **TightVNC Viewer** (free)
- Download: https://www.tightvnc.com/download.php

2. **RealVNC Viewer** (free for personal use)
- Download: https://www.realvnc.com/download/viewer/

3. **UltraVNC** (free, open source)
- Download: https://www.uvnc.com/downloads/ultravnc.html

### VNC Connection
1. Launch the VNC client
2. Connect to: `localhost:5900`
3. Password: none (leave blank)
4. You should see Chrome in the GUI environment.

## 🔧 Docker Compose Profiles

### Basic Profiles
```batch
REM Only API
docker-compose up -d

REM API + Redis
docker-compose --profile redis up -d

REM API + Nginx (reverse proxy)
docker-compose --profile nginx up -d

REM API + PostgreSQL
docker-compose --profile database up -d

REM Monitoring (Prometheus + Grafana)
docker-compose --profile monitoring up -d
```

### Profile combinations
```batch
REM Full stack
docker-compose --profile redis --profile nginx --profile monitoring up -d

REM Development with everything
docker-compose --profile dev --profile redis --profile monitoring up -d
```

## 🛠️ Development Mode

```batch
REM Starting in development mode
docker-compose --profile dev up -d
```

Available in dev mode:
- API: http://localhost:8001
- VNC: localhost:5901
- Jupyter Notebook: http://localhost:8888
- Hot reload (code changes are immediately visible)

## 📊 Docker Manager (docker-manager.bat)

The interactive manager offers:

### 📦 Basic operations
1. Launching production
2. Launching development
3. Stopping all services
4. Restarting services
5. Service status

### 🏗️ Advanced operations
6. Full stack (API + Redis + Nginx)
7. With monitoring (+ Prometheus + Grafana)
8. With database (+ PostgreSQL)
9. Full development mode

### 🛠️ Maintenance
10. Building images
11. Cleaning (removing containers, volumes)
12. Viewing logs
13. Shell in container
14. Resource usage

### 🌐 Access information
15. All URLs
16. VNC instructions

## 🐛 Troubleshooting

### Docker not running
```batch
REM Check Docker status
docker version

REM Start Docker Desktop if not running
```

### Port busy
```batch
REM Check what's using port 8000
netstat -ano | findstr :8000

REM Terminate the process using the port (PID from the previous command)
taskkill /PID <PID> /F
```

### VNC Problems
1. Check if port 5900 is available
2. Try a different VNC client
3. Check the container logs:
```batch
docker-compose logs chatgpt-api
```

### Slow performance
```batch
REM Check resource usage
docker stats

REM Increase allocated resources in Docker Desktop:
REM Settings > Resources > Advanced
```

## 📝 Logs

### Viewing logs
```batch
REM All logs
docker-compose logs

REM Specific service logs
docker-compose logs chatgpt-api

REM Live logs
docker-compose logs -f

REM Last 100 lines
docker-compose logs --tail=100
```

## 🧹 Cleaning

### Stop and remove
```batch
REM Stop and remove containers
docker-compose down

REM Stop and remove containers + volumes
docker-compose down -v

REM Full Docker system prune
docker system prune
