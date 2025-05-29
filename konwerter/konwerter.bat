@echo off
setlocal

REM Sprawdzenie Pythona
python --version >nul 2>&1
if errorlevel 1 (
    echo Python nie jest zainstalowany lub nie jest w PATH.
    echo Pobierz i zainstaluj Python 3.6 lub wyzszy z: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Sprawdzenie wersji Pythona
for /f "tokens=2 delims= " %%a in ('python --version') do set PYVER=%%a
for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (
    set PYMAJOR=%%a
    set PYMINOR=%%b
)

if %PYMAJOR% LSS 3 (
    echo Wymagana jest wersja Pythona 3.6 lub wyzsza.
    pause
    exit /b 1
) else if %PYMAJOR%==3 if %PYMINOR% LSS 6 (
    echo Wymagana jest wersja Pythona 3.6 lub wyzsza.
    pause
    exit /b 1
)

REM Sprawdzenie yt-dlp
python -m yt_dlp --version >nul 2>&1
if errorlevel 1 (
    echo Pakiet yt-dlp nie jest zainstalowany. Instalowanie...
    python -m pip install --upgrade yt-dlp
    if errorlevel 1 (
        echo Nie udalo sie zainstalowac yt-dlp. Sprawdz polaczenie internetowe i sprobuj ponownie.
        pause
        exit /b 1
    )
)

REM Uruchomienie skryptu
python assets\konwerter.py

endlocal
