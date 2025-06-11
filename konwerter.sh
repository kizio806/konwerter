#!/bin/bash
set -e

# --- Sprawdź, czy Python jest zainstalowany ---
if ! command -v python3 &> /dev/null; then
    echo "Python nie jest zainstalowany. Proszę zainstalować Pythona ręcznie."
    exit 1
else
    echo "Python jest zainstalowany."
fi

# --- Zainstaluj potrzebne pakiety Python ---
echo "Instalacja wymaganych pakietow Python..."
python3 -m pip install --upgrade pip
python3 -m pip install yt-dlp spotdl questionary rich

# --- Pobierz ffmpeg jeśli brak ---
if [ ! -x "./ffmpeg/ffmpeg" ]; then
    echo "Pobieram ffmpeg..."
    wget https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip -O ffmpeg.zip

    echo "Rozpakowywanie ffmpeg..."
    unzip -q ffmpeg.zip -d ffmpeg_temp

    rm ffmpeg.zip

    # Przeniesienie plików binarnych do ./ffmpeg
    mkdir -p ffmpeg
    mv ffmpeg_temp/ffmpeg-*/bin/* ffmpeg/
    rm -rf ffmpeg_temp
else
    echo "ffmpeg juz jest pobrany."
fi

# --- Dodaj lokalny ffmpeg do PATH tymczasowo ---
export PATH="$PWD/ffmpeg:$PATH"

# --- Uruchom skrypt Python ---
echo "Uruchamiam program Python..."
python3 "assets/konwerter.py"
