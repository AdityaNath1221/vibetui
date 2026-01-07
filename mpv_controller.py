# =========================
# IMPORTS
# =========================

# Used to run mpv playback monitoring in background
import threading

# Used for polling intervals
import time

# Python bindings for mpv media player
from mpv import MPV


# =========================
# MPV CONTROLLER CLASS
# =========================
class MPVController:
    """
    A thin wrapper around mpv that:
    - Plays audio streams (YouTube URLs)
    - Exposes simple controls (play / pause / seek)
    - Detects when a song ends using a background watcher thread
    """

    def __init__(self, on_song_end=None):
        # Initialize mpv with minimal UI and audio-only setup
        self.mpv = MPV(
            ytdl=True,          # Enable youtube-dl / yt-dlp support
            idle=True,          # Keep mpv running even when nothing is playing
            vid="no",           # Disable video output (audio-only mode)
            terminal="no",      # Disable mpv terminal UI
            msg_level="all=no", # Silence mpv logs
        )

        # Callback function to be called when song finishes
        self.on_song_end = on_song_end

        # Controls the lifetime of the watcher thread
        self._running = True

        # Tracks whether something was playing previously
        # Used to detect "play → end" transitions
        self._was_playing = False

        # Background thread that watches playback state
        self._watcher = threading.Thread(
            target=self._watch_playback,
            daemon=True  # Daemon thread dies when main app exits
        )
        self._watcher.start()


    # =========================
    # PLAYBACK MONITOR THREAD
    # =========================
    def _watch_playback(self):
        """
        Continuously checks mpv playback state.

        Logic:
        - If time_pos exists → song is playing
        - If time_pos becomes None while mpv is idle → song ended
        """
        while self._running:
            # Poll every 500ms (cheap + responsive enough)
            time.sleep(0.5)

            try:
                # time_pos = current playback time in seconds
                time_pos = self.mpv.time_pos

                # idle_active = True when mpv is idle (nothing playing)
                idle = self.mpv.idle_active
            except Exception:
                # mpv might be in a transient state, ignore and retry
                continue

            # Song is currently playing
            if time_pos is not None:
                self._was_playing = True
                continue

            # Song just ended:
            # - Was playing before
            # - Now mpv is idle
            if self._was_playing and idle:
                self._was_playing = False

                # Notify the app that playback finished
                if self.on_song_end:
                    self.on_song_end()


    # =========================
    # PUBLIC CONTROL METHODS
    # =========================
    def play(self, url):
        """
        Load and immediately play a media URL.
        'replace' ensures the current track is stopped.
        """
        self.mpv.command("loadfile", url, "replace")

    def toggle_pause(self):
        """
        Toggles pause/play state.
        """
        self.mpv.pause = not self.mpv.pause

    def seek(self, seconds):
        """
        Seek forward/backward relative to current position.

        Args:
            seconds (int): Positive → forward, Negative → backward
        """
        self.mpv.command("seek", seconds, "relative")

    def quit(self):
        """
        Gracefully shut down mpv and stop watcher thread.
        """
        self._running = False
        try:
            self.mpv.terminate()
        except Exception:
            # Ignore shutdown errors
            pass
