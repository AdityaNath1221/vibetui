import socket
import json 
import subprocess
import time

class MPV:
    def __init__(self, socket_url="/tmp/mpvsocket"):
        self.sock = socket.socket(socket.AF_UNIX)
        self.sock.connect(socket_url)

    # def cmd(self, *args):
    #     self.sock.send(
    #         json.dumps({"command": list(args)}).encode() + b"\n"
    #     )

    def cmd(self, *args):
        msg = {
            "command": list(args),
            "request_id": 1
        }
        self.sock.send(json.dumps(msg).encode() + b"\n")

        while True:
            line = self.sock.recv(4096).decode().splitlines()
            for l in line:
                data = json.loads(l)

                # Ignore async events
                if "event" in data:
                    continue

                # This is our reply
                return data

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

    # def get_property(self, prop):
    #     return self.cmd("get_property", prop)

    def get_property(self, prop):
        res = self.cmd("get_property", prop)
        return res.get("data")


    # def is_playing(self):
    #     paused = self.get_property("pause")
    #     idle = self.get_property("idle-active")
    #     return not paused and not idle
    
    def is_playing(self):
        idle = self.get_property("idle-active")
        paused = self.get_property("pause")
        return (not idle) and (not paused)


    def quit(self):
        self.cmd("quit")