import subprocess
from textual.app import App
from textual import on
from textual.containers import ScrollableContainer
from textual.widgets import Header, Footer, Button, Input, Static
from music_services import get_trending_songs, search_song
from mpv import MPV

with open("assets/logo.txt") as f:
    logo = f.read()
with open("assets/trending.txt") as f:
    trending = f.read()
with open("assets/queue.txt") as f:
    queue = f.read()
with open("assets/search.txt") as f:
    search = f.read()

class Player(Static):
    pass

class VIBEtui(App):
    """Main landing"""
    def on_mount(self):
        self.queue = []
        self.theme = "gruvbox"
        self.mpv = MPV()
        self.set_interval(0.1, self.play_from_queue,pause=False)
        self.current_view = "none"
        self.current_song=[]
        self.action_navigate_home()

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

    @on(Input.Submitted, "#search_box")
    def search(self, event: Input.Submitted):
        results = search_song(event.input.value)
        text_area = self.query("#search_box")
        text_area.remove()
        container = self.query_one("#main_container")
        for x in results:
            container.mount(Button(f"{x['title']} | {x['duration']}", name=x["videoId"]))

    def play_from_queue(self):
        if not self.queue:
            return
        if not self.mpv.is_playing():
            self.current_song = self.queue.pop(0)
            song_url = f"https://www.youtube.com/watch?v={self.current_song['videoId']}"
            self.mpv.play(song_url)

    def action_navigate_home(self):
        if self.current_view=="home":
            return
        else:
            self.current_view="home"
            container = self.query_one("#main_container")
            container.remove_children()
            container.mount(Static(content=logo, id="logo"))
            # container.mount(Static(content=self.queue[0].get("videoId")))

    def action_navigate_queue(self):
        if self.current_view=="queue":
            return
        else:
            self.current_view = "queue"
            container = self.query_one("#main_container")
            container.remove_children()
            container.mount(Static(content=queue, id="queue"))
            if not self.current_song:
                container.mount(Static(content="Itna sannata kyun hai bhai?", id="queue_empty"))
            else:
                container.mount(Static(content="Currently Playing:", id="current"))
                container.mount(Button(self.current_song["title"]))
                if not self.queue:
                    return
                else:
                    container.mount(Static(content="Up Next", id="up_next"))
                    for song in self.queue:
                        container.mount(Button(song["title"]))

    def action_search_song(self):
        if self.current_view=="search":
            return
        else:
            self.current_view="search"
            container = self.query_one("#main_container")
            container.remove_children()
            container.mount(Static(content=search, id="search"))
            input_area = Input(placeholder="Start typing...", type="text", id="search_box")
            container.mount(input_area)
            input_area.focus()

    def action_get_trending(self):
        if self.current_view=="trending":
            return
        else:
            self.current_view = "trending"
            container = self.query_one("#main_container")
            container.remove_children()
            container.mount(Static(content=trending, id="trending"))
            songs = get_trending_songs()
            for song in songs:
                container.mount(
                    Button(f'{song["title"]} | {song.get("duration")}', name=song["videoId"], classes="songs")
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
        # yield Header(show_clock=True)
        yield Footer()
        yield ScrollableContainer(id="main_container")
            

if __name__ == "__main__":

    VIBEtui().run()
