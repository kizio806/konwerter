# yt_downloader.py
import os
import subprocess
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

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

def validate_int_input(prompt, min_val, max_val, default):
    while True:
        val = Prompt.ask(prompt, default=str(default))
        if val.isdigit():
            val_int = int(val)
            if min_val <= val_int <= max_val:
                return val_int
        console.print(f"[yellow]Podaj liczbę od {min_val} do {max_val} lub ENTER dla domyślnej ({default})[/yellow]")

def validate_choice_input(prompt, choices):
    while True:
        val = Prompt.ask(prompt)
        if val in choices:
            return val
        console.print(f"[yellow]Wybierz jedną z opcji: {', '.join(choices)}[/yellow]")

def get_valid_file_path(prompt):
    while True:
        path = Prompt.ask(prompt)
        if os.path.isfile(path):
            return path
        console.print("[red]Nie znaleziono pliku pod podaną ścieżką.[/red]")

def download_videos(links, max_count, yt_format, output_path):
    for i, link in enumerate(links[:max_count]):
        console.print(f"\n[cyan][{i+1}/{max_count}] Pobieranie:[/cyan] {link}")
        output_template = os.path.join(output_path, "%(title)s.%(ext)s")
        command = [
            "python", "-m", "yt_dlp",
            "-f", yt_format,
            "-o", output_template,
            link
        ]
        subprocess.run(command)

def main():
    clear_console()
    console.print(Panel.fit("[bold magenta]YouTube Video Downloader (yt-dlp)[/bold magenta]"))

    file_path = get_valid_file_path("Podaj ścieżkę do pliku z linkami (np. C:\\linki.txt):")
    links = load_links(file_path)
    if not links:
        return

    max_count = validate_int_input(f"Ile filmów chcesz pobrać? (1–{len(links)}):", 1, len(links), len(links))

    console.print("\nWybierz jakość:")
    console.print("1. Najlepsza dostępna MP4\n2. Tylko dźwięk (MP3)")
    choice = validate_choice_input("Wybór (1/2):", ["1", "2"])

    if choice == "2":
        yt_format = "bestaudio"
    else:
        yt_format = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"

    output_path = Prompt.ask("\nPodaj ścieżkę folderu do zapisu (ENTER = bieżący folder)", default=os.getcwd())
    if not os.path.isdir(output_path):
        try:
            os.makedirs(output_path)
            console.print(f"[green]Utworzono folder: {output_path}[/green]")
        except Exception as e:
            console.print(f"[red]Błąd tworzenia folderu: {e}[/red]")
            output_path = os.getcwd()

    console.print("\n[bold green]Rozpoczynam pobieranie...[/bold green]")
    download_videos(links, max_count, yt_format, output_path)

if __name__ == "__main__":
    main()
