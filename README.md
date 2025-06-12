# 🎵 YouTube & Spotify Downloader

Interaktywny skrypt terminalowy do pobierania muzyki i wideo z **YouTube** i **Spotify**. Obsługuje pojedyncze linki oraz pliki z wieloma adresami. Idealny do lokalnego backupu ulubionych utworów, z pełną obsługą audio MP3 i wysokiej jakości wideo MP4.

---

## 📦 Wymagania

Przed uruchomieniem upewnij się, że posiadasz:

- Python **3.7** lub wyższy
- Narzędzia CLI:
  - [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
  - [`ffmpeg`](https://ffmpeg.org/)
  - [`spotDL`](https://github.com/spotDL/spotify-downloader)

> 📌 Upewnij się, że wszystkie powyższe narzędzia są zainstalowane i dodane do `PATH`.

**Instalacja zależności Pythona:**

```bash
pip install questionary rich
```

---

## 🚀 Jak używać

1. Uruchom skrypt:

```bash
python konwerter.py
```

2. Wybierz źródło (YouTube / Spotify)  
3. Podaj link lub plik z linkami  
4. Wybierz format (MP3/Wideo)  
5. Podaj folder docelowy  
6. Gotowe — pliki zostaną pobrane i zapisane lokalnie!

---

## 🧠 Funkcje

- 🎧 Pobieranie audio z YouTube (MP3)
- 📺 Pobieranie wideo z YouTube (MP4)
- 🎶 Pobieranie z Spotify przy użyciu `spotDL`
- 📂 Obsługa wielu linków z pliku `.txt`
- 🧼 Automatyczne czyszczenie konsoli
- 💡 Dynamiczne pytania w CLI (`questionary`)
- 🎨 Kolorowe logi z `rich`

---

## 📄 Przykład pliku z linkami

```
https://www.youtube.com/watch?v=xxxx
https://open.spotify.com/track/yyyy
```

---

## 🧑‍💻 Autor

**Nick:** kizio806  
**Discord:** `_kizio_`
**GitHub:** [https://github.com/kizio806](https://github.com/kizio806)


Jeśli masz pytania, propozycje zmian lub chcesz współtworzyć projekt — śmiało się odezwij!

---

## 📜 Licencja

Ten projekt dostępny jest na licencji **MIT** — możesz go dowolnie używać, kopiować i modyfikować. Wymagana jest jedynie informacja o autorze w przypadku dalszej dystrybucji.

Pełna treść licencji znajduje się w pliku [LICENSE](LICENSE).

---

## ❤️ Wsparcie projektu

Jeśli ten skrypt Ci pomógł, zostaw ⭐ na GitHubie lub przekaż opinię. Możesz też:

- Zgłosić problem (Issue)
- Zaproponować nową funkcję (Pull Request)
- Udostępnić znajomym

---

## 📬 Kontakt i społeczność

💬 Dołącz do mojego **serwera Discord**:  
[discord.gg/blintzstore](https://discord.com/invite/M9thr49cFY)
