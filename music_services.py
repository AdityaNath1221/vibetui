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
            - title (str)
            - videoId (str)
            - duration (str)
    """

    # Search YouTube Music using a trending-related query
    # filter="songs" ensures we only get songs (not playlists/videos)
    results = ytmusic.search(
        "India Trending Songs",
        filter="songs",
        limit=20
    )

    songs = []

    # Extract only the fields we actually need
    for r in results:
        songs.append({
            "title": r["title"],
            "videoId": r["videoId"],
            "duration": r["duration"]
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
            - title
            - videoId
            - duration
    """

    # filter="videos" is used instead of "songs"
    # because video results are more reliable for playback via mpv
    results = ytmusic.search(
        query=query,
        filter="videos",
        limit=10
    )

    songs = []

    # Normalize API response into a clean structure
    for r in results:
        songs.append({
            "title": r["title"],
            "videoId": r["videoId"],
            "duration": r["duration"]
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
