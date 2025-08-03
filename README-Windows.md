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
⭐⭐⭐ A gift for ignoramuses who don't know English ;-) ⭐⭐⭐

# ChatGPT Bot - Docker dla Windows

## 🚀 Szybki Start

### Wymagania
- Windows 10/11
- Docker Desktop for Windows
- Git (opcjonalnie)

### Instalacja Docker Desktop
1. Pobierz Docker Desktop z https://www.docker.com/products/docker-desktop/
2. Zainstaluj i uruchom Docker Desktop
3. Upewnij się, że Docker działa (ikona wieloryba w tray)

## 📁 Pliki Windows

Projekt zawiera następujące pliki Windows:

### Podstawowe skrypty
- `start-docker.bat` - Szybkie uruchomienie (podstawowa konfiguracja)
- `stop-docker.bat` - Zatrzymanie wszystkich usług
- `build-docker.bat` - Zbudowanie obrazów Docker
- `docker-manager.bat` - Pełny menedżer Docker (wszystkie opcje)

## 🎯 Użycie

### Opcja 1: Szybkie uruchomienie
```batch
REM Uruchom projekt
start-docker.bat

REM Zatrzymaj projekt
stop-docker.bat
```

### Opcja 2: Menedżer Docker
```batch
REM Uruchom interaktywny menedżer
docker-manager.bat
```

### Opcja 3: Ręcznie przez PowerShell/CMD
```batch
REM Podstawowe uruchomienie
docker-compose up -d

REM Uruchomienie z monitoringiem
docker-compose --profile monitoring up -d

REM Zatrzymanie
docker-compose down
```

## 🌐 Dostęp do usług

Po uruchomieniu dostępne są:

| Usługa | URL | Opis |
|--------|-----|------|
| **API** | http://localhost:8000 | Główne API ChatGPT Bot |
| **Dokumentacja** | http://localhost:8000/docs | Swagger UI |
| **VNC** | localhost:5900 | Dostęp do GUI (bez hasła) |
| **Health Check** | http://localhost:8000/ | Status API |

### Usługi dodatkowe (z profilami)
| Usługa | URL | Profil |
|--------|-----|--------|
| **Nginx** | http://localhost:80 | `--profile nginx` |
| **Redis** | localhost:6379 | `--profile redis` |
| **PostgreSQL** | localhost:5432 | `--profile database` |
| **Prometheus** | http://localhost:9090 | `--profile monitoring` |
| **Grafana** | http://localhost:3000 | `--profile monitoring` |

## 🖥️ VNC - Dostęp do GUI

### Klienty VNC dla Windows
1. **TightVNC Viewer** (darmowy)
   - Pobierz: https://www.tightvnc.com/download.php
   
2. **RealVNC Viewer** (darmowy do użytku osobistego)
   - Pobierz: https://www.realvnc.com/download/viewer/
   
3. **UltraVNC** (darmowy, open source)
   - Pobierz: https://www.uvnc.com/downloads/ultravnc.html

### Połączenie VNC
1. Uruchom klienta VNC
2. Połącz się z: `localhost:5900`
3. Hasło: brak (pozostaw puste)
4. Powinieneś zobaczyć przeglądarkę Chrome w środowisku GUI

## 🔧 Profile Docker Compose

### Podstawowe profile
```batch
REM Tylko API
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

### Kombinacje profili
```batch
REM Pełny stack
docker-compose --profile redis --profile nginx --profile monitoring up -d

REM Development z wszystkim
docker-compose --profile dev --profile redis --profile monitoring up -d
```

## 🛠️ Tryb Development

```batch
REM Uruchomienie w trybie development
docker-compose --profile dev up -d
```

Dostępne w trybie dev:
- API: http://localhost:8001
- VNC: localhost:5901
- Jupyter Notebook: http://localhost:8888
- Hot reload (zmiany w kodzie od razu widoczne)

## 📊 Menedżer Docker (docker-manager.bat)

Interaktywny menedżer oferuje:

### 📦 Podstawowe operacje
1. Uruchomienie produkcyjne
2. Uruchomienie development
3. Zatrzymanie wszystkich usług
4. Restart usług
5. Status usług

### 🏗️ Zaawansowane operacje
6. Pełny stack (API + Redis + Nginx)
7. Z monitoringiem (+ Prometheus + Grafana)
8. Z bazą danych (+ PostgreSQL)
9. Pełny tryb development

### 🛠️ Konserwacja
10. Budowanie obrazów
11. Czyszczenie (usunięcie kontenerów, volumes)
12. Wyświetlanie logów
13. Shell w kontenerze
14. Użycie zasobów

### 🌐 Informacje o dostępie
15. Wszystkie URL-e
16. Instrukcje VNC

## 🐛 Rozwiązywanie problemów

### Docker nie działa
```batch
REM Sprawdź status Docker
docker version

REM Uruchom Docker Desktop jeśli nie działa
```

### Port zajęty
```batch
REM Sprawdź co używa portu 8000
netstat -ano | findstr :8000

REM Zakończ proces używający portu (PID z poprzedniej komendy)
taskkill /PID <PID> /F
```

### Problemy z VNC
1. Sprawdź czy port 5900 jest dostępny
2. Spróbuj innego klienta VNC
3. Sprawdź logi kontenera:
   ```batch
   docker-compose logs chatgpt-api
   ```

### Wolne działanie
```batch
REM Sprawdź użycie zasobów
docker stats

REM Zwiększ przydzielone zasoby w Docker Desktop:
REM Settings > Resources > Advanced
```

## 📝 Logi

### Wyświetlanie logów
```batch
REM Wszystkie logi
docker-compose logs

REM Logi konkretnej usługi
docker-compose logs chatgpt-api

REM Logi na żywo
docker-compose logs -f

REM Ostatnie 100 linii
docker-compose logs --tail=100
```

## 🧹 Czyszczenie

### Zatrzymanie i usunięcie
```batch
REM Zatrzymaj i usuń kontenery
docker-compose down

REM Zatrzymaj i usuń kontenery + volumes
docker-compose down -v

REM Pełne czyszczenie systemu Docker
docker system prune -a
```

## 🔐 Bezpieczeństwo

### Hasła domyślne
- VNC: brak hasła (tylko localhost)
- Grafana: admin/admin
- PostgreSQL: postgres/postgres
- Redis: bez uwierzytelniania

### Produkcja
Przed wdrożeniem na produkcji:
1. Zmień wszystkie hasła domyślne
2. Skonfiguruj HTTPS
3. Ogranicz dostęp do portów
4. Włącz uwierzytelnianie Redis

## 📞 Wsparcie

W przypadku problemów:
1. Sprawdź logi: `docker-compose logs`
2. Sprawdź status: `docker-compose ps`
3. Sprawdź zasoby: `docker stats`
4. Restart: `docker-compose restart`

## 🆕 Aktualizacje

```batch
REM Pobierz najnowszy kod
git pull

REM Przebuduj obrazy
docker-compose build --no-cache

REM Uruchom ponownie
docker-compose up -d
```
