@echo off
echo Sprawdzanie portu 8008...
echo.

REM Sprawdź co używa portu 8008
netstat -ano | findstr :8008

echo.
echo Jeśli widzisz wyniki powyżej, port jest zajęty.
echo Ostatnia kolumna to PID procesu.
echo.

REM Pokaż szczegóły procesu
echo Szczegóły procesów używających port 8008:
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8008') do (
    echo PID: %%a
    tasklist /fi "PID eq %%a" /fo table
    echo.
)

pause