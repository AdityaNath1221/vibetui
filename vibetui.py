import subprocess
from textual.app import App
from textual import on
from textual.containers import ScrollableContainer, Container
from textual.widgets import Header, Footer, Button, Input, Static
from music_services import get_trending_songs, search_song
# from player import play_song, stop_all_songs
from mpv import MPV

with open("/home/aditya/Projects/vibetui/banner.txt") as f:
    banner = f.read()

class Player(Static):
    pass

class VIBEtui(App):
    """Main landing"""
    def on_mount(self):
        self.theme = "gruvbox"
        self.mpv = MPV()

    CSS_PATH = "style.css"

    BINDINGS = [
        ("h", "navigate_home", "Home"),
        ("/", "search_song", "Search"),
        ("t", "get_trending", "Trending"),
        ("h", "seek_backward", "Backward 5s"),
        ("space", "toggle_pause", "Play/Pause"),
        ("l", "seek_forward", "Forward 5s"),
        ("^q", "quit", "Quit"),
    ]

    @on(Button.Pressed)
    def play(self, event: Button.Pressed):
        song_url = f"https://www.youtube.com/watch?v={event.button.name}"
        self.mpv.play(song_url)

    @on(Input.Submitted, "#search")
    def search(self, event: Input.Submitted):
        results = search_song(event.input.value)
        text_area = self.query("#search")
        text_area.remove()
        container = self.query_one("#main_container")
        for x in results:
            container.mount(Button(f"{x['title']} | {x['duration']}", name=x["videoId"]))


    def action_navigate_home(self):
        container = self.query_one("#main_container")
        container.remove_children()
        container.mount(Static(content=banner, id="banner"))

    def action_search_song(self):
        container = self.query_one("#main_container")
        container.remove_children()
        input_area = Input(placeholder="Enter song name", type="text", id="search")
        container.mount(input_area)
        input_area.focus()

    def action_get_trending(self):
        container = self.query_one("#main_container")
        container.remove_children()
        songs = get_trending_songs()
        for song in songs:
            container.mount(
                Button(f'{song["title"]} | {song.get("duration","--:--")}', name=song["videoId"])
            )

    def action_toggle_pause(self):
        self.mpv.toggle_pause()

    def action_seek_forward(self):
        self.mpv.seek_forward()

    def action_seek_backward(self):
        self.mpv.seek_backward()

    def stop_music(self):
        try:
            self.mpv.quit()
        except Exception:
            pass

    def action_quit(self):
        self.stop_music()
        self.exit()

    def compose(self):
        """Creating/rendering widgets"""
        yield Header(show_clock=True)
        yield Footer()
        with ScrollableContainer(id="main_container"):
            yield Static(content=banner, id="banner")
            

if __name__ == "__main__":
    cmd = [
        "mpv",
        "--no-video",
        "--idle=yes",
        "--input-ipc-server=/tmp/mpvsocket",
        "--input-terminal=no",
        "--no-input-default-bindings",
        "--really-quiet",
        "--cache=no",
    ]

    subprocess.Popen(cmd)

    VIBEtui().run()
