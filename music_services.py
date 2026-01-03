from ytmusicapi import YTMusic
ytmusic = YTMusic()

def get_trending_songs():

    results = ytmusic.search("India Trending Songs", filter="songs", limit=20)

    songs = []

    for r in results:
        songs.append({
            "title": r["title"],
            "videoId": r["videoId"],
            "duration": r["duration"]
        })

    return songs

def search_song(query):

    results = ytmusic.search(query=query, filter="songs", limit=10)

    songs = []

    for r in results:
        songs.append({
            "title": r["title"],
            "videoId": r["videoId"],
            "duration": r["duration"]
        })

    return songs

