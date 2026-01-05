# IMPORTS
import subprocess
import time
from textual.app import App
from textual import on
from textual.containers import ScrollableContainer, Container
from textual.widgets import Header, Footer, Button, Input, Static
from textual.events import Focus
from music_services import get_trending_songs, search_song, get_suggestions
from mpv import MPV

# LOADING ASSETS

with open("assets/logo.txt") as f: logo = f.read()
with open("assets/trending.txt") as f: trending = f.read()
with open("assets/search.txt") as f: search = f.read()
with open("assets/queue.txt") as f: queue = f.read()

#MAIN APP
class VIBEtui(App):

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

    def __init__(self):
        super().__init__()
        self.theme = "gruvbox"
        self.mpv = MPV()
        self.current_view = "none"
        self.current_song = []
        self.current_song_idx = -1
        self.queue = []
        self.is_paused = False

    def compose(self):
        yield Footer()
        with Container(id="main_container"):

            # Home Page
            with Container(id="home_page"):
                yield Static(content=logo, classes="title")
                yield Button("dummy_home", classes="hidden") 

            # Search Page
            with Container(id="search_page", classes="hidden"):
                yield Static(content=search, classes="title")
                yield Input(placeholder="Start typing...", type="text", id="search_box")
                yield ScrollableContainer(id="suggestions", classes="container hidden")
                yield ScrollableContainer(id="search_results", classes="container")
                yield Button("dummy_search", classes="hidden") 

            # Queue Page
            with Container(id="queue_page", classes="hidden"):
                yield Static(content=queue, classes="title")
                yield Static("Itna sannata kyun hai bhai??", id="silence", classes="dialog")
                yield Static(content="Currently Playing:", id="currently_playing_text", classes="dialog")
                with Container(id="currently_playing_box", classes="hidden"):
                    yield Button("<-", id="prev", classes="music_controls")
                    yield Button("", id="current", classes="music_controls")
                    yield Button("->", id="next", classes="music_controls")
                yield Static(content="Up Next:", id="up_next_text", classes="dialog")
                yield ScrollableContainer(id="up_next_box", classes="hidden")
                yield Button("dummy_queue", classes="hidden")  

            # Trending Page
            with Container(id="trending_page", classes="hidden"):
                yield Static(content=trending, classes="title")
                yield ScrollableContainer(id="trending_songs")
                yield Button("dummy_trending", classes="hidden") 

    def on_mount(self):
        self.show_page("home_page") 
        self.set_focus(self.query_one("#home_page"))
        self.set_interval(1/60, self.play_from_queue,pause=False)

    def show_page(self, id: str):
        """Show one page, hide all others"""
        for page_idx in ["home_page","search_page","queue_page","trending_page"]:
            page = self.query_one(f"#{page_idx}")
            if page_idx== id:
                page.remove_class("hidden")
            else:
                page.add_class("hidden")
        self.current_view = id

    def action_navigate_home(self):
        self.show_page("home_page")
        self.set_focus(self.query_one("#home_page"))

    def action_navigate_search(self):
        self.show_page("search_page")
        self.set_focus(self.query_one("#search_box"))

    def action_navigate_queue(self):
        self.show_page("queue_page")
        self.update_queue_page()  # Always refresh on page switch

    def action_navigate_trending(self):
        self.show_page("trending_page")
        self.set_focus(self.query_one("#trending_page"))
        trending_songs = get_trending_songs()
        container = self.query_one("#trending_songs")
        for song in trending_songs:
            container.mount(Button(f'{song["title"]} | {song["duration"]}', name=song["videoId"], classes="listed_songs"))

    # Add this method in VIBEtui

    def update_queue_page(self):
        """Updates currently playing and up next sections dynamically."""
        page = self.query_one("#queue_page")
        currently_playing_box = self.query_one("#currently_playing_box")
        up_next_box = self.query_one("#up_next_box")
        silence_text = self.query_one("#silence")
        current_text = self.query_one("#currently_playing_text")
        up_next_text = self.query_one("#up_next_text")

        # No songs in queue
        if not self.queue:
            currently_playing_box.add_class("hidden")
            up_next_box.add_class("hidden")
            current_text.add_class("hidden")
            up_next_text.add_class("hidden")
            silence_text.remove_class("hidden")
            return

        # Songs exist
        silence_text.add_class("hidden")
        current_text.remove_class("hidden")
        currently_playing_box.remove_class("hidden")

        # Update currently playing song title
        current_button = self.query_one("#current", Button)
        if self.current_song:
            current_button.label = self.current_song["title"]
        else:
            current_button.label = "Nothing Playing"

        # Update Up Next
        up_next_box.remove_children()
        if self.current_song_idx + 1 < len(self.queue):
            up_next_box.remove_class("hidden")
            up_next_text.remove_class("hidden")
            for idx in range(self.current_song_idx + 1, len(self.queue)):
                up_next_box.mount(Button(self.queue[idx]["title"], classes="up_next_songs"))
        else:
            up_next_box.add_class("hidden")
            up_next_text.add_class("hidden")


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

    def play_song(self):
        self.current_song = self.queue[self.current_song_idx]
        song_url = f'https://www.youtube.com/watch?v={self.current_song["videoId"]}'
        self.mpv.play(song_url)
        self.update_queue_page()


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

    # EVENT HANDLERS

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
        self.set_focus(search_results_container)
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
        self.queue.append({
            "title": event.button.label.split("|")[0],
            "duration": event.button.label.split("|")[1],
            "videoId": event.button.name
        })
        self.update_queue_page()

    @on(Button.Pressed, "#next")
    def play_next_song(self):
        if self.current_song_idx + 1 < len(self.queue):
            self.current_song_idx += 1
            self.play_song()

    @on(Button.Pressed, "#prev")
    def play_previous_song(self):
        if self.current_song_idx - 1 >= 0:
            self.current_song_idx -= 1
            self.play_song()

    

if __name__ == "__main__":
    # Launch mpv socket
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
    # Run the app
    VIBEtui().run()
