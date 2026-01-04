import subprocess
import time
from textual.app import App
from textual import on
from textual.containers import ScrollableContainer, Container
from textual.widgets import Header, Footer, Button, Input, Static
from textual.events import Focus
from music_services import get_trending_songs, search_song, get_suggestions
from mpv import MPV

with open("assets/logo.txt") as f:
    logo = f.read()
with open("assets/trending.txt") as f:
    trending = f.read()
with open("assets/queue.txt") as f:
    queue = f.read()
with open("assets/search.txt") as f:
    search = f.read()
with open("assets/player.txt") as f:
    player = f.read()

class Music_Player(Static):

    @on(Button.Pressed, "#current_song_name")
    def toggle_song(self):
        self.app.mpv.toggle_pause()

    def compose(self):
        with Container(id="player_controller"):
            yield Button("Kal Ho Naa Ho", id="current_song_name")
            yield Button("<-", id="previous" ,classes="player_controls")
            yield Button("->", id="next", classes="player_controls")

class Home(Static):
    
    def compose(self):
        with Container(id="home_box"):
            yield Static(content=logo, classes="title", id="vibetui")
            yield Music_Player()

class Trending(Static):

    def __init__(self):
        super().__init__()
        self.trending_songs = get_trending_songs()

    @on(Button.Pressed, ".listed_songs")
    def play_song(self, event: Button.Pressed):                            # directly play song for now, add to queue later
        song_url = f"https://www.youtube.com/watch?v={event.button.name}"
        self.app.mpv.play(song_url)

    def compose(self):
        with Container(id="trending_box"):
            yield Static(content=trending, id="trending_title", classes="title")
            with ScrollableContainer(id="trending_songs"):
                for song in self.trending_songs:
                    yield Button(f'{song["title"]} | {song["duration"]}', name=song["videoId"], classes="listed_songs")

class Search(Static):

    def on_mount(self):
        self.set_interval(1/2, self.get_search_suggestions, pause=False)

    def get_search_suggestions(self):
        input = self.query_one("#search_box")
        container = self.query_one("#suggestions")
        container.remove_children()
        suggestions = get_suggestions(input.value)
        if suggestions:
            for suggestion in suggestions:
                container.mount(Button(suggestion, classes="listed_suggestions"))


    @on(Input.Submitted, "#search_box")
    def search(self, event: Input.Submitted):
        search_results_container = self.query_one("#search_results")
        search_results_container.remove_class("hidden")
        suggestions = self.query_one("#suggestions")
        suggestions.add_class("hidden")
        results = search_song(event.input.value)
        for x in results:
            search_results_container.mount(Button(f"{x['title']} | {x['duration']}", name=x["videoId"], classes="listed_songs"))

    @on(Button.Pressed, ".listed_songs")
    def play(self, event: Button.Pressed):
        song_url = f"https://www.youtube.com/watch?v={event.button.name}"
        # self.queue.append({
        #     "title": event.button.label.split("|")[0],
        #     "duration": event.button.label.split("|")[1],
        #     "videoId": event.button.name
        # })
        self.app.mpv.play(song_url)


    def compose(self):
        with Container(id="search_box_container"):
            yield Static(content=search, id="search_title", classes="title")  
            yield Input(placeholder="Start typing...", type="text", id="search_box")
            yield ScrollableContainer(id="suggestions")
            yield ScrollableContainer(id="search_results")


class VIBEtui(App):
    """Main landing"""
    def on_mount(self):
        self.queue = []
        self.theme = "gruvbox"
        self.mpv = MPV()
        self.set_interval(1/60, self.play_from_queue,pause=False)
        self.current_view = "none"
        self.current_song=[]
        self.action_navigate_home()

    CSS_PATH = "style.tcss"

    BINDINGS = [
        ("h", "navigate_home", "Home"),
        ("q", "navigate_queue", "Queue"),
        ("/", "navigate_search", "Search"),
        ("t", "navigate_trending", "Trending"),
        ("<", "seek_backward", "Backward 5s"),
        ("space", "toggle_pause", "Play/Pause"),
        (">", "seek_forward", "Forward 5s"),
        ("^q", "quit", "Quit"),
    ]

    @on(Button.Pressed, ".songs")
    def play(self, event: Button.Pressed):
        song_url = f"https://www.youtube.com/watch?v={event.button.name}"
        self.queue.append({
            "title": event.button.label.split("|")[0],
            "duration": event.button.label.split("|")[1],
            "videoId": event.button.name
        })
        # self.mpv.play(song_url)

    def play_from_queue(self):
        if not self.queue:
            self.current_song=[]
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
            container.mount(Home())


    def action_navigate_queue(self):
        if self.current_view=="queue":
            return
        else:
            self.current_view = "queue"
            container = self.query_one("#main_container")
            container.remove_children()
            container.mount(Static(content=queue, id="queue"))
            if not self.current_song:
                container.mount(Static(content="Itna sannata kyun hai bhai?", id="queue_empty", classes="queue_dialog"))
            else:
                container.mount(Static(content="Currently Playing:", id="current"))
                container.mount(Button(self.current_song["title"]))
                if not self.queue:
                    return
                else:
                    container.mount(Static(content="Up Next", id="up_next"))
                    for song in self.queue:
                        container.mount(Button(song["title"]))

    def action_navigate_search(self):
        if self.current_view=="search":
            return
        else:
            self.current_view="search"
            container = self.query_one("#main_container")
            container.remove_children()
            container.mount(Search())
            input_area = container.query_one("#search_box")
            input_area.focus()

    def action_navigate_trending(self):
        if self.current_view=="trending":
            return
        else:
            self.current_view = "trending"
            container = self.query_one("#main_container")
            container.remove_children()
            container.mount(Trending())

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
        yield Container(id="main_container")
        # yield Search()


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
    time.sleep(0.001) 

    VIBEtui().run()
