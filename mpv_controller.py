from mpv import MPV

class MPVController:

    def __init__(self, on_song_end=None):
        self.mpv = MPV(
            ytdl=True,
            input_ipc_server="/tmp/mpvsocket",
            idle=True,
        )
        self.mpv["vid"] = "no"         
        self.mpv["terminal"] = "no"    
        self.mpv["msg-level"] = "all=no"
        self.on_song_end = on_song_end
        self.shutting_down = False

        @self.mpv.event_callback("end-file")
        def _(event):
            if self._shutting_down:
                return

            reason = event.get("reason")
            if reason != "eof":
                return  # 🔥 ignore manual skips

            if self.on_song_end:
                self.on_song_end()

    def play(self, url):
        self.mpv.command("stop")
        self.mpv.command("loadfile", url, "replace")

    def toggle_pause(self):
        self.mpv.pause = not self.mpv.pause



    def seek(self, seconds: int):
        self.mpv.command("seek", seconds, "relative")

    def quit(self):
        self.shutting_down = True
        try:
            self.mpv.terminate()
        except Exception:
            pass