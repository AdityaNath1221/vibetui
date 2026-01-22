# =========================
# YTMUSIC API SETUP
# =========================

# Import the unofficial YouTube Music API wrapper
from ytmusicapi import YTMusic

# Create a YTMusic client instance
# This handles all communication with YouTube Music
ytmusic = YTMusic()


# =========================
# TRENDING SONGS
# =========================
def get_trending_songs():
    """
    Fetches a list of trending songs in India.

    Returns:
        List[dict]: Each dict contains:
            - category
            - title
            - videoId
            - duration
            - artists
    """

    # Search YouTube Music using a trending-related query
    # filter="songs" ensures we only get songs (not playlists/videos)
    results = ytmusic.search(
        "India Trending Songs",
        filter="songs",
    )

    songs = []

    # Extract only the fields we actually need
    for x in results:
        artist_names = ", ".join(
            artist["name"] for artist in x.get("artists", [])
        )

        songs.append({
            "category": x["category"],
            "title": x["title"],
            "videoId": x["videoId"],
            "duration": x["duration"] if x["duration"] else "",
            "artists": artist_names,
            })

    return songs


# =========================
# SEARCH SONGS
# =========================
def search_song(query):
    """
    Searches YouTube Music for songs/videos based on user input.

    Args:
        query (str): Search keyword entered by the user

    Returns:
        List[dict]: Search results with:
            - category
            - title
            - videoId
            - duration
            - artists
    """

    # filter="videos" is used instead of "songs"
    # because some songs are only available as videos and not labelled as songs
    results = ytmusic.search(
        query=query,
        filter="videos",
    )

    songs = []

    # Normalize API response into a clean structure
    for x in results:
        artist_names = ", ".join(
            artist["name"] for artist in x.get("artists", [])
        )

        songs.append({
            "category": x["category"],
            "title": x["title"],
            "videoId": x["videoId"],
            "duration": x["duration"] if x["duration"] else "",
            "artists": artist_names,
            })

    return songs


# =========================
# SEARCH SUGGESTIONS
# =========================
def get_suggestions(text):
    """
    Fetches live search suggestions while the user types.

    Args:
        text (str): Current input in the search box

    Returns:
        List[str]: Suggested search queries
    """

    # YouTube Music provides autocomplete-style suggestions
    results = ytmusic.get_search_suggestions(text)

    return results