# from mpv import MPV as _MPV

# class MPVController:
#     def __init__(self, on_song_end=None):
#         self.mpv = _MPV(
#             input_ipc_server="/tmp/mpvsocket",
#             idle=True,
#         )
#         self.mpv["vid"] = "no"         
#         self.mpv["terminal"] = "no"    
#         self.mpv["msg-level"] = "all=no"
#         self.on_song_end = on_song_end

#         @self.mpv.event_callback("end-file")
#         def _(event):
#             if self.on_song_end:
#                 self.on_song_end()

#     def play(self, url: str):
#         self.mpv.command("loadfile", url, "replace")

#     def toggle_pause(self):
#         self.mpv.command("cycle", "pause")

#     def seek(self, seconds: int):
#         self.mpv.command("seek", seconds)

#     def quit(self):
#         self.mpv.terminate()

#     def shutdown(self):
#         try:
#             self.mpv.command("quit")
#         except Exception:
#             pass

#         try:
#             self.mpv.terminate()
#         except Exception:
#             pass

#     def is_playing(self):
#         # True only when actively playing audio
#         return self.mpv.core_idle is False and self.mpv.pause is False

#     def time_pos(self):
#         try:
#             return self.mpv.time_pos
#         except Exception:
#             return None

#     def duration(self):
#         try:
#             return self.player.duration
#         except Exception:
#             return None

# mpv_controller.py
from mpv import MPV

class MPVController:
    # def __init__(self, on_eof=None):
    #     self.on_eof = on_eof

    #     self.mpv = MPV(
    #         ytdl=True,
    #         input_default_bindings=True,
    #         input_vo_keyboard=True,
    #         terminal=False,
    #         log_handler=self._log_handler,
    #     )

    #     # mpv event hook
    #     @self.mpv.event_callback("end-file")
    #     def _on_end_file(event):
    #         reason = event.get("reason")
    #         if reason == "eof" and self.on_eof:
    #             self.on_eof()

    def __init__(self):
        # FIXED: Added ytdl=True to enable yt-dlp integration
        # This is required for MPV to stream YouTube URLs via yt-dlp
        # Without this, MPV cannot play YouTube videos
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

    # def play(self, url: str):
    #     # replace ensures previous file is killed properly
    #     self.mpv.command("loadfile", url, "replace")

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