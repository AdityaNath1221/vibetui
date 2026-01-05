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
with open("assets/search.txt") as f:
    search = f.read()
with open("assets/queue.txt") as f:
    queue = f.read()

class Trending(Static):

    def __init__(self):
        super().__init__()
        self.trending_songs = get_trending_songs()

    @on(Button.Pressed, ".listed_songs")
    def play_song(self, event: Button.Pressed):                            # directly play song for now, add to queue later
        self.app.queue.append({
            "title": event.button.label.split("|")[0],
            "duration": event.button.label.split("|")[1],
            "videoId": event.button.name
        })

    def compose(self):
        with Container(id="trending_box"):
            yield Static(content=trending, id="trending_title", classes="title")
            with ScrollableContainer(id="trending_songs"):
                for song in self.trending_songs:
                    yield Button(f'{song["title"]} | {song["duration"]}', name=song["videoId"], classes="listed_songs")

class Search(Static):

    @on(Input.Changed, '#search_box')
    def get_search_suggestions(self, event: Input.Changed):
        search_results = self.query_one("#search_results")
        search_results.add_class("hidden")
        container = self.query_one("#suggestions")
        container.remove_children()
        container.remove_class("hidden")
        suggestions = get_suggestions(event.input.value)
        if suggestions:
            for suggestion in suggestions:
                container.mount(Button(suggestion,name=suggestion, classes="listed_suggestions"))


    @on(Input.Submitted, "#search_box")
    def search(self, event: Input.Submitted):
        suggestions = self.query_one("#suggestions")
        suggestions.add_class("hidden")
        search_results_container = self.query_one("#search_results")
        search_results_container.remove_children()
        search_results_container.remove_class("hidden")
        results = search_song(event.input.value)
        for x in results:
            search_results_container.mount(Button(f"{x['title']} | {x['duration']}", name=x["videoId"], classes="listed_songs"))

    @on(Button.Pressed, ".listed_suggestions")
    def search_from_suggestion(self, event: Button.Pressed):
        suggestion = self.query_one("#suggestions")
        suggestion.add_class("hidden")
        search_results_container = self.query_one("#search_results")
        search_results_container.remove_children()
        search_results_container.remove_class("hidden")
        results = search_song(event.button.name)
        for x in results:
            search_results_container.mount(Button(f"{x['title']} | {x['duration']}", name=x["videoId"], classes="listed_songs"))

    @on(Button.Pressed, ".listed_songs")
    def play(self, event: Button.Pressed):
        self.app.queue.append({
            "title": event.button.label.split("|")[0],
            "duration": event.button.label.split("|")[1],
            "videoId": event.button.name
        })


    def compose(self):
        with Container(id="search_box_container"):
            yield Static(content=search, id="search_title", classes="title")  
            yield Input(placeholder="Start typing...", type="text", id="search_box")
            yield ScrollableContainer(id="suggestions", classes="container")
            yield ScrollableContainer(id="search_results", classes="container")


class VIBEtui(App):
    """Main landing"""

    def __init__(self):
        super().__init__()
        self.theme = "gruvbox"
        self.is_paused = False
        self.mpv = MPV()

    def on_mount(self):
        self.queue = []
        self.set_interval(1/60, self.play_from_queue,pause=False)
        self.current_view = "none"
        self.current_song = []
        self.current_song_idx = -1
        self.action_navigate_home()

    CSS_PATH = "style.css"

    BINDINGS = [
        ("h", "navigate_home", "Home"),
        ("escape", "navigate_home"),
        ("q", "navigate_queue", "Queue"),
        ("/", "navigate_search", "Search"),
        ("t", "navigate_trending", "Trending"),
        ("<", "seek_backward", "Backward 5s"),
        ("space", "toggle_pause", "Play/Pause"),
        (">", "seek_forward", "Forward 5s"),
        ("^q", "quit", "Quit"),
    ]

    def play_from_queue(self):          # Recursive function that checks if any songs in queue and plays it. Runs 60 times per sec
        if not self.queue:
            return
        if self.is_paused:
            return
        if not self.mpv.is_playing():
            if self.current_song_idx+1==len(self.queue):
                return                
            self.current_song_idx+=1
            self.current_song = self.queue[self.current_song_idx]
            self.play_song()

    def get_current_song(self):
        if not self.current_song:
            return False
        return self.current_song
        

    def play_song(self):
        self.current_song = self.queue[self.current_song_idx]
        song_url = f'https://www.youtube.com/watch?v={self.current_song["videoId"]}'
        self.mpv.play(song_url)

    @on(Button.Pressed, "#next")
    def play_next_song(self):           # increment current song index and then play it
        if self.current_song_idx+1 != len(self.queue):
            self.current_song_idx+=1
            self.current_song = self.queue[self.current_song_idx]
            self.play_song()
        else:
            return

    @on(Button.Pressed, "#prev")
    def play_previous_song(self):       # decrement current song index and then play it
        if self.current_song_idx-1 != -1:
            self.current_song_idx-=1
            self.current_song = self.queue[self.current_song_idx]
            self.play_song()
        else:
            self.play_song()

    @on(Button.Pressed, "#current")
    def toggle_song(self):
        self.is_paused = not self.is_paused
        self.mpv.toggle_pause()

    def action_navigate_home(self):
        if self.current_view=="home":
            return
        else:
            self.current_view="home"
            container = self.query_one("#main_container")
            container.remove_children()
            container.mount(Static(content=logo, classes="title"))

    def action_navigate_queue(self):
        if self.current_view=="queue":
            return
        else:
            self.current_view="queue"
            container = self.query_one("#main_container")
            container.remove_children()
            container.mount(Static(content=queue, classes="title"))
            if not self.queue:
                container.mount(Static("Itna sannata kyun hai bhai??", id="silence"))
            else:
                container.mount(Static(content="Currently Playing:", id="currently_playing_text"))

                currently_playing_container = Container(id="currently_playing_box")
                container.mount(currently_playing_container)

                currently_playing_container.mount(Button("<-", id="prev", classes="music_controls"))
                currently_playing_container.mount(Button(self.current_song["title"], id="current", classes="music_controls"))
                currently_playing_container.mount(Button("->", id="next", classes="music_controls"))

                if len(self.queue)>1 and self.current_song_idx!=len(self.queue)-1:
                    container.mount(Static(content="Up Next:", id="up_next_text"))

                    up_next_container = ScrollableContainer(id="up_next_box")
                    container.mount(up_next_container)

                    for idx in range(self.current_song_idx+1, len(self.queue)):
                        up_next_container.mount(Button(self.queue[idx]["title"], classes="up_next_songs"))


 

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
        self.is_paused = not self.is_paused
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
    time.sleep(0.5) 

    VIBEtui().run()




        #    if not self.current_song:
        #         container.mount(Static(content="Itna sannata kyun hai bhai?", id="queue_empty", classes="queue_dialog"))
        #     else:
        #         container.mount(Static(content="Currently Playing:", classes="queue_dialog"))
        #         container.mount(Button(self.current_song["title"], id="current", classes="queue_current"))
        #         if not self.queue:
        #             return
        #         else:
        #             container.mount(Static(content="Up Next"))
        #             for idx in range(self.current_song_idx+1, len(self.queue)):
        #                 container.mount(Button(self.queue[idx]["title"]), classes="queue_songs")