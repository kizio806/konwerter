#!/bin/bash

# Sprawdzenie czy jest python3
if ! command -v python3 &> /dev/null
then
    echo "Python3 nie jest zainstalowany lub nie jest w PATH."
    echo "Zainstaluj Python 3.6 lub wyzszy i uruchom ponownie."
    exit 1
fi

# Sprawdzenie wersji Pythona
PYVER=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYMAJOR=$(echo "$PYVER" | cut -d. -f1)
PYMINOR=$(echo "$PYVER" | cut -d. -f2)

if [ "$PYMAJOR" -lt 3 ] || { [ "$PYMAJOR" -eq 3 ] && [ "$PYMINOR" -lt 6 ]; }; then
    echo "Wymagana jest wersja Pythona 3.6 lub wyzsza."
    exit 1
fi

# Sprawdzenie yt-dlp
if ! python3 -m yt_dlp --version &> /dev/null; then
    echo "Pakiet yt-dlp nie jest zainstalowany. Instalowanie..."
    python3 -m pip install --upgrade yt-dlp
    if [ $? -ne 0 ]; then
        echo "Nie udało się zainstalować yt-dlp. Sprawdź połączenie internetowe i spróbuj ponownie."
        exit 1
    fi
fi

# Uruchomienie skryptu assets/konwerter.py
python3 assets/konwerter.py
