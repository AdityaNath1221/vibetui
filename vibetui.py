import subprocess
from textual.app import App
from textual import on
from textual.containers import ScrollableContainer
from textual.widgets import Header, Footer, Button, Input, Static
from music_services import get_trending_songs, search_song
from mpv import MPV

with open("/home/aditya/Projects/vibetui/banner.txt") as f:
    banner = f.read()

class Player(Static):
    pass

class VIBEtui(App):
    """Main landing"""
    def on_mount(self):
        self.queue = []
        self.theme = "gruvbox"
        self.mpv = MPV()
        self.set_interval(0.1, self.play_from_queue,pause=False)

    CSS_PATH = "style.css"

    BINDINGS = [
        ("h", "navigate_home", "Home"),
        ("q", "navigate_queue", "Queue"),
        ("/", "search_song", "Search"),
        ("t", "get_trending", "Trending"),
        ("<", "seek_backward", "Backward 5s"),
        ("space", "toggle_pause", "Play/Pause"),
        (">", "seek_forward", "Forward 5s"),
        ("^q", "quit", "Quit"),
    ]

    @on(Button.Pressed)
    def play(self, event: Button.Pressed):
        song_url = f"https://www.youtube.com/watch?v={event.button.name}"
        self.queue.append({
            "title": event.button.label.split("|")[0],
            "duration": event.button.label.split("|")[1],
            "videoId": event.button.name
        })
        # self.mpv.play(song_url)

    @on(Input.Submitted, "#search")
    def search(self, event: Input.Submitted):
        results = search_song(event.input.value)
        text_area = self.query("#search")
        text_area.remove()
        container = self.query_one("#main_container")
        for x in results:
            container.mount(Button(f"{x['title']} | {x['duration']}", name=x["videoId"]))

    def play_from_queue(self):
        if not self.queue:
            return
        if not self.mpv.is_playing():
            song = self.queue.pop(0)
            song_url = f"https://www.youtube.com/watch?v={song['videoId']}"
            self.mpv.play(song_url)

    def action_navigate_home(self):
        container = self.query_one("#main_container")
        container.remove_children()
        container.mount(Static(content=banner, id="banner"))
        # container.mount(Static(content=self.queue[0].get("videoId")))

    def action_navigate_queue(self):
        container = self.query_one("#main_container")
        container.remove_children()
        container.mount(Static(content=banner, id="banner"))
        if not self.queue:
            container.mount(Static(content="Your queue is empty!!!", id="queue_empty"))
        else:
            for song in self.queue:
                container.mount(Button(song["title"]))
        # container.mount(Static(content=self.queue[0].get("videoId")))

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

    VIBEtui().run()
