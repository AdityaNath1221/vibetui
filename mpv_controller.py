# from mpv import MPV

# # class MPVController:

# #     def __init__(self, on_song_end=None):
# #         self.mpv = MPV(
# #             ytdl=True,
# #             input_ipc_server="/tmp/mpvsocket",
# #             idle=True,
# #         )
# #         self.mpv["vid"] = "no"         
# #         self.mpv["terminal"] = "no"    
# #         self.mpv["msg-level"] = "all=no"
# #         self.on_song_end = on_song_end
# #         self.shutting_down = False

# #         # @self.mpv.event_callback("end-file")
# #         # def _(event):
# #         #     if self.shutting_down:
# #         #         return

# #         #     reason = event.get("reason")
# #         #     if reason != "eof":
# #         #         return  # 🔥 ignore manual skips

# #         #     if self.on_song_end:
# #         #         self.on_song_end()

# #         @self.mpv.event_callback("end-file")
# #         def _(event):
# #             if self.shutting_down:
# #                 return

# #             reason = event.reason  # <-- enum, not string

# #             # Only advance queue on natural ending
# #             if reason == EndFileReason.EOF:
# #                 if self.on_song_end:
# #                     self.on_song_end()

# class MPVController:
#     def __init__(self, on_song_end=None):
#         self.mpv = MPV(
#             ytdl=True,
#             input_ipc_server="/tmp/mpvsocket",
#             idle=True,
#         )

#         self.mpv["vid"] = "no"
#         self.mpv["terminal"] = "no"
#         self.mpv["msg-level"] = "all=no"

#         self.on_song_end = on_song_end
#         self.shutting_down = False

#         @self.mpv.event_callback("end-file")
#         def _(event):
#             if self.shutting_down:
#                 return

#             # event.reason is an INT in python-mpv
#             # 0 = EOF (natural end)
#             if event.reason == 0:
#                 if self.on_song_end:
#                     self.on_song_end()

#     def play(self, url):
#         self.mpv.command("stop")
#         self.mpv.command("loadfile", url, "replace")

#     def toggle_pause(self):
#         self.mpv.pause = not self.mpv.pause



#     def seek(self, seconds: int):
#         self.mpv.command("seek", seconds, "relative")

#     def quit(self):
#         self.shutting_down = True
#         try:
#             self.mpv.terminate()
#         except Exception:
#             pass

# NEW CODE

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
