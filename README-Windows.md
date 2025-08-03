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
