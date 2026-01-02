from ytmusicapi import YTMusic
from time import monotonic
import json
import subprocess
from ytdlp import play_song

starting_time = monotonic()
ytmusic = YTMusic()
results = ytmusic.search("jhim jhim aaune aankha", filter="songs")

songs=[]

for r in results:
    songs.append({
        "title": r["title"],
        "videoId": r["videoId"],
        "duration": r.get("duration")
    })

url = f"https://youtu.be/{songs[0].get("videoId")}"

print("Elapsed Time = ", monotonic()-starting_time)

subprocess.Popen([
    "mpv",
    "--no-video",
    "--ytdl-format=bestaudio[ext=m4a]",
    url
])



