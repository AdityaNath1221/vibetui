from mpv import MPV

class MPVController:

    def __init__(self):
        self.mpv = MPV(
            ytdl=True,
            input_ipc_server="/tmp/mpvsocket",
            idle=True,
        )
        self.mpv["vid"] = "no"         
        self.mpv["terminal"] = "no"    
        self.mpv["msg-level"] = "all=no"
        self._on_end = None

        @self.mpv.event_callback("end-file")
        def _(event):
            if event.reason == "eof" and self._on_end:
                self._on_end()

    def play(self, url):
        self.mpv.command("stop")
        self.mpv.command("loadfile", url, "replace")

    def toggle_pause(self):
        self.mpv.pause = not self.mpv.pause

    def on_end(self, callback):
        self._on_end = callback


    def seek(self, seconds: int):
        self.mpv.command("seek", seconds, "relative")

    def stop(self):
        try:
            self.mpv.command("stop")
        except Exception:
            pass

    def quit(self):
        try:
            self.mpv.terminate()
        except Exception:
            pass