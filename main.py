import subprocess
import json

def search_song(query, items=10):
    cmd = [
        "yt-dlp",
        "-j",
        "-s",
        f"ytsearch{items}:{query}"
    ]

    results = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    videos = []

    for line in results.stdout.splitlines():
        data = json.loads(line)
        videos.append({
            "title": data["title"],
            "url": data["webpage_url"],
            "duration": data["duration"]
        })


    return videos

def get_song_url(url):
    cmd=[
        "yt-dlp",
        "-f",
        "bestaudio",
        "-g",
        f"{url}"
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    return result.stdout

def play_song(url):
    cmd = [
        "mpv",
        "--no-video",
        f"{url}"
    ]

    result = subprocess.run(
        cmd
    )

    return result

song = input("Enter the name of song: ")

song_metadata = search_song(song, 1)

# print(type(song[0].get("url")))

# print(get_song_url("https://www.youtube.com/watch?v=DZ4BtMpaJaU"))
# print(get_song_url(song[0].get("url")))

song_url = get_song_url(song_metadata[0].get("url"))

play_song(song_url)

