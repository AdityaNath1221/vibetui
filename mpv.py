import socket
import json 

class MPV:
    def __init__(self, socket_path="/tmp/mpvsocket"):
        self.sock = socket.socket(socket.AF_UNIX)
        self.sock.connect(socket_path)

    def cmd(self, *args):
        self.sock.send(
            json.dumps({"command": list(args)}).encode() + b"\n"
        )

    def play(self, url):
        self.cmd("loadfile", url, "replace")

    def pause(self):
        self.cmd("set_property", "pause", True)

    def resume(self):
        self.cmd("set_property", "pause", False)

    def stop(self):
        self.cmd("stop")

    def toggle_pause(self):
        self.cmd("cycle", "pause")

    def seek_forward(self):
        self.cmd("seek", 5, "relative")

    def seek_backward(self):
        self.cmd("seek", -5, "relative")

    def quit(self):
        self.cmd("quit")