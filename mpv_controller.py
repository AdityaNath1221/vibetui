import threading
import time
from mpv import MPV

class MPVController:
    def __init__(self, on_song_end=None):
        self.mpv = MPV(
            ytdl=True,
            idle=True,
            vid="no",
            terminal="no",
            msg_level="all=no",
        )

        self.on_song_end = on_song_end
        self._running = True
        self._was_playing = False

        self._watcher = threading.Thread(
            target=self._watch_playback,
            daemon=True
        )
        self._watcher.start()

    def _watch_playback(self):
        while self._running:
            time.sleep(0.5)

            try:
                time_pos = self.mpv.time_pos
                idle = self.mpv.idle_active
            except Exception:
                continue

            # Song is playing
            if time_pos is not None:
                self._was_playing = True
                continue

            # Song just ended
            if self._was_playing and idle:
                self._was_playing = False
                if self.on_song_end:
                    self.on_song_end()

    def play(self, url):
        self.mpv.command("loadfile", url, "replace")

    def toggle_pause(self):
        self.mpv.pause = not self.mpv.pause

    def seek(self, seconds):
        self.mpv.command("seek", seconds, "relative")

    def quit(self):
        self._running = False
        try:
            self.mpv.terminate()
        except Exception:
            pass
