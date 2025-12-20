import subprocess
import os

# CONFIG 
download_folder = "download"
os.makedirs(download_folder, exist_ok=True)

# FUNTIONS
def get_valid_url():
    while True:
        url = input("Paste your URL: ")
        if not url:
            print("URL cannot be empty: ")
            continue

        if not (url.startswith("http://") or url.startswith("https://")):
            print("Please enter a valid URL format: ")
            continue
        return url
    
def show_video_formats(url):
    print("\nFeatching available qualities...\n")
    result = subprocess.run(
        ["yt-dlp", "-F", url],
        capture_output = True,
        text = True
    )
    if result.returncode != 0:
        print("Failed to featch formats: ")
        return False
    print(result.stdout)
    return True

def show_audio_formats(url):
    print("\nFeatching available qualities...\n")
    result = subprocess.run(
        ["yt-dlp", "-F", url],
        capture_output = True,
        text = True
    )
    if result.returncode != 0:
        print("Failed to featch audio Formats.")
        return False
    
    for line in result.stdout.splitlines():
        if "audio only" in line:
            print(line)

    return True

def download_selected_video(url):
    success = show_video_formats(url)
    if not success:
        return
    while True:
        format_id = input("Enter 'Format ID' you want to download.").strip()
        if not format_id:
            print("Format ID can't be empty.")
            continue
        break
    print("\nDownloarding Selected video quality...\n")

    subprocess.run(
        ["yt-dlp", "-f", format_id, "-o", f"{download_folder}/%(title)s.%(ext)s", url]
    )
    print("Downloard completed:")

def download_selected_audio(url):
    if not show_audio_formats(url):
        return
    
    while True:
        format_id = input("Enter Audio Format you want.").strip()
        if not format_id:
            print("Format ID cannot be empty.\n")
            continue
        break
    print("\nDownloading selected audio quality...\n")

    subprocess.run([
        "yt-dlp",
        "-f", format_id,
        "-x", 
        "--audio-format", "mp3",
        "-o", f"{download_folder}/%(title)s.%(ext)s",
        url
    ])

print("** Simple Media Downloader **")
url = get_valid_url()
while True:
    print("1. Video:")
    print("2. Audio:")
    choice = input("Enter a format that you want to download ( 1 / 2 )").strip().lower()
    if choice == "1":
        download_selected_video(url)
    elif choice == "2":
        download_selected_audio(url)
    elif choice == "exit":
        print("Exiting the program...")
        break