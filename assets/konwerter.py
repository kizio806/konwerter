import os
import subprocess
import questionary
from rich.console import Console
from rich.panel import Panel
from pathlib import Path

console = Console()


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def load_links(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            links = [line.strip() for line in file if line.strip()]
            if not links:
                console.print("[bold red]Plik jest pusty lub nie zawiera linków![/bold red]")
            return links
    except FileNotFoundError:
        console.print("[bold red]Nie znaleziono pliku![/bold red]")
        return []


def get_output_path():
    folder = questionary.path("Podaj ścieżkę folderu do zapisu:").ask()
    if not folder:
        folder = os.getcwd()
    if not os.path.isdir(folder):
        try:
            os.makedirs(folder)
            console.print(f"[green]Utworzono folder: {folder}[/green]")
        except Exception as e:
            console.print(f"[red]Błąd tworzenia folderu: {e}[/red]")
            folder = os.getcwd()
    return folder


def convert_to_mp3(file_path):
    mp3_path = file_path.with_suffix(".mp3")
    command = [
        "ffmpeg", "-y",
        "-i", str(file_path),
        "-codec:a", "libmp3lame",
        "-b:a", "192k",
        str(mp3_path)
    ]
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        file_path.unlink()  # usuń oryginalny .m4a po konwersji
        return mp3_path
    else:
        console.print(f"[red]❌ Błąd konwersji: {file_path}[/red]")
        return file_path


def download_youtube(links, count, audio_only, output_path):
    yt_format = "bestaudio[ext=m4a]" if audio_only else "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"
    output_template = os.path.join(output_path, "%(title)s.%(ext)s")

    for i, link in enumerate(links[:count]):
        console.print(f"\n[cyan][{i+1}/{count}] Pobieranie:[/cyan] {link}")
        command = [
            "yt-dlp",
            "-f", yt_format,
            "-o", output_template,
            link
        ]
        subprocess.run(command)

        # Konwersja do MP3 jeśli tylko audio
        if audio_only:
            try:
                result = subprocess.run(
                    ["yt-dlp", "--get-filename", "-o", output_template, link],
                    capture_output=True, text=True
                )
                downloaded_file = Path(result.stdout.strip())
                if downloaded_file.exists() and downloaded_file.suffix.lower() == ".m4a":
                    convert_to_mp3(downloaded_file)
            except Exception as e:
                console.print(f"[red]Błąd przy konwersji pliku: {e}[/red]")


def download_spotify(links, output_path):
    os.chdir(output_path)
    for link in links:
        console.print(f"\n[cyan]Pobieranie ze Spotify:[/cyan] {link}")
        command = [
            "spotdl", link
        ]
        subprocess.run(command)


def get_links_manual_or_file(source_name):
    mode = questionary.select(
        f"Jak chcesz wprowadzić link(i) z {source_name}?",
        choices=[
            "📄 Z pliku tekstowego",
            "🔗 Wpisz pojedynczy link"
        ]
    ).ask()

    if mode.startswith("📄"):
        file_path = questionary.path("Podaj ścieżkę do pliku z linkami:").ask()
        links = load_links(file_path)
    else:
        single_link = questionary.text("Wklej link:").ask()
        links = [single_link.strip()] if single_link else []

    if not links:
        console.print("[bold red]Brak poprawnych linków![/bold red]")
    return links


def main():
    clear_console()
    console.print(Panel.fit("[bold cyan]🎵 Downloader: YouTube & Spotify[/bold cyan]"))

    # Weryfikacja obecności narzędzi
    for cmd in ["yt-dlp", "ffmpeg"]:
        if not shutil.which(cmd):
            console.print(f"[bold red]❌ Nie znaleziono: {cmd}. Zainstaluj i dodaj do PATH.[/bold red]")
            return

    source = questionary.select(
        "Z jakiego źródła chcesz pobierać?",
        choices=["YouTube", "Spotify"]
    ).ask()

    links = get_links_manual_or_file(source)
    if not links:
        return

    output_path = get_output_path()

    if source == "YouTube":
        count = 1
        if len(links) > 1:
            count = questionary.text(
                f"Ile filmów chcesz pobrać? (max {len(links)}):", default=str(len(links))
            ).ask()
            count = int(count) if count.isdigit() and 0 < int(count) <= len(links) else len(links)

        quality = questionary.select(
            "Wybierz jakość:",
            choices=[
                ("🎵 Tylko dźwięk (MP3)", True),
                ("📺 Wideo (najlepsza jakość)", False)
            ]
        ).ask()

        download_youtube(links, count, audio_only=quality, output_path=output_path)

    else:  # Spotify
        download_spotify(links, output_path)

    console.print("\n[bold green]✅ Pobieranie zakończone![/bold green]")


if __name__ == "__main__":
    import shutil
    main()
