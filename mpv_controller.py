from mpv import MPV as _MPV

class MPVController:
    def __init__(self, on_song_end=None):
        self.mpv = _MPV(
            input_ipc_server="/tmp/mpvsocket",
            idle=True,
        )
        self.mpv["vid"] = "no"         
        self.mpv["terminal"] = "no"    
        self.mpv["msg-level"] = "all=no"
        self.on_song_end = on_song_end

        @self.mpv.event_callback("end-file")
        def _(event):
            if self.on_song_end:
                self.on_song_end()

    def play(self, url: str):
        self.mpv.command("loadfile", url, "replace")

    def toggle_pause(self):
        self.mpv.command("cycle", "pause")

    def seek(self, seconds: int):
        self.mpv.command("seek", seconds)

    def quit(self):
        self.mpv.terminate()

    def shutdown(self):
        try:
            self.mpv.command("quit")
        except Exception:
            pass

        try:
            self.mpv.terminate()
        except Exception:
            pass

    def is_playing(self):
        # True only when actively playing audio
        return self.mpv.core_idle is False and self.mpv.pause is False

    def time_pos(self):
        try:
            return self.mpv.time_pos
        except Exception:
            return None

    def duration(self):
        try:
            return self.player.duration
        except Exception:
            return None

