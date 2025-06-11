@echo off
setlocal

REM --- Sprawdź, czy Python jest zainstalowany ---
python --version >nul 2>&1
if ERRORLEVEL 1 (
    echo Python nie jest zainstalowany. Pobieram instalator...

    set "PYTHON_INSTALLER=python-3.11.4-amd64.exe"
    if not exist "%PYTHON_INSTALLER%" (
        echo Pobieranie %PYTHON_INSTALLER% ...
        powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.4/%PYTHON_INSTALLER% -OutFile %PYTHON_INSTALLER%"
    ) else (
        echo Instalator Pythona juz jest lokalnie.
    )

    echo Instalacja Pythona...
    start /wait "" "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

    python --version >nul 2>&1
    if ERRORLEVEL 1 (
        echo Nie udało się zainstalować Pythona, przerwanie.
        pause
        exit /b 1
    )
) else (
    echo Python jest zainstalowany.
)

REM --- Zainstaluj potrzebne pakiety Python ---
echo Instalacja wymaganych pakietow Python...
python -m pip install --upgrade pip
python -m pip install yt-dlp spotdl questionary rich

REM --- Pobierz ffmpeg (wersja Windows) jeśli brak ---
if not exist ffmpeg\bin\ffmpeg.exe (
    echo Pobieram ffmpeg...
    powershell -Command "Invoke-WebRequest -Uri https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip -OutFile ffmpeg.zip"

    echo Rozpakowywanie ffmpeg...
    powershell -Command "Expand-Archive -Path ffmpeg.zip -DestinationPath ffmpeg"

    del ffmpeg.zip

    REM Przenies pliki bin do ffmpeg\
    for /d %%d in (ffmpeg\ffmpeg-*) do (
        move /y "%%d\bin\*" ffmpeg\
        rmdir /s /q "%%d"
    )
) else (
    echo ffmpeg juz jest pobrany.
)

REM --- Dodaj lokalny ffmpeg do PATH tymczasowo ---
set "PATH=%CD%\ffmpeg;%PATH%"

REM --- Uruchom skrypt Python ---
echo Uruchamiam program Python...
python "assets\konwerter.py"

pause
endlocal
