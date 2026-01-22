#  _    __________  ________        _ 
# | |  / /  _/ __ )/ ____/ /___  __(_)
# | | / // // __  / __/ / __/ / / / / 
# | |/ // // /_/ / /___/ /_/ /_/ / /  
# |___/___/_____/_____/\__/\__,_/_/   
                                                                                                            


# =========================
# IMPORTS
# =========================

# Core Textual app class
from textual.app import App
from textual import on

from textual.screen import Screen

# Containers for layout
from textual.containers import ScrollableContainer, Container

# UI widgets
from textual.widgets import Footer, Button, Input, Static

# Custom modules for music handling
from music_services import get_trending_songs, search_song, get_suggestions
from mpv_controller import MPVController
from playlists.playlist_manager import PlaylistManager


# =========================
# LOADING ASCII / TEXT ASSETS
# =========================
# These are just text banners shown on different pages

with open("assets/logo.txt") as f:
    logo = f.read()

with open("assets/trending.txt") as f:
    trending = f.read()

with open("assets/search.txt") as f:
    search = f.read()

with open("assets/queue.txt") as f:
    queue = f.read()

with open("assets/playlists.txt") as f:
    playlists = f.read()

# Defining a custom song button to hold the metadata of songs.

class Song(Button):
    def __init__(self, song, **kwargs):
        super().__init__(**kwargs)
        self.song = song

class CreatePlaylistScreen(Screen):

    def on_mount(self):
        self.playlist_name: str | None = None
        self.songs: list[dict] = []

    def compose(self):
        yield Static("Create Playlist", classes="title")
        yield Input(placeholder="Playlist name", id="name")
        yield Input(placeholder="Search songs...", id="search")
        yield ScrollableContainer(id="results")
        yield Button("Save Playlist", id="save")
        yield Button("Cancel", id="cancel")

    @on(Input.Submitted, "#name")
    def set_name(self, event: Input.Submitted):
        self.playlist_name = event.value.strip()

    @on(Input.Changed, "#search")
    def search(self, event: Input.Changed):
        query = event.value.strip()

        if not query:
            return
        
        results = search_song(query)
        container = self.query_one("#results")
        container.remove_children()

        for song in results:
            container.mount(
                Song(
                    label=f"{song['title']}\n{song['artists']}",
                    song=song,
                    classes="listed_songs"
                )
            )
    
    @on(Button.Pressed, ".listed_songs")
    def add_song(self, event: Song.Pressed):
        song_button: Song = event.button
        self.songs.append(song_button.song)

    @on(Button.Pressed, "#save")
    def save(self):
        if not self.playlist_name:
            return

        pm = self.app.playlistManager
        pm.create(self.playlist_name)

        for song in self.songs:
            pm.add_song(self.playlist_name, song)

        pm.save()
        self.app.pop_screen()

    @on(Button.Pressed, "#cancel")
    def cancel(self):
        self.app.pop_screen()

class LoadPlaylistScreen(Screen):

    def compose(self):
        yield Static("Load Playlist", classes="title")
        yield ScrollableContainer(id="playlists")
        yield Button("Back", id="back")

    def on_mount(self):
        container = self.query_one("#playlists")
        for name in self.app.playlistManager.names():
            container.mount(Button(name, name=name))

    @on(Button.Pressed)
    def load(self, event: Button.Pressed):
        songs = self.app.playlistManager.get(event.button.name)
        self.app.queue.extend(songs)

        if self.app.current_song_idx == -1 and self.app.queue:
            self.app.current_song_idx = 0
            self.app.play_current()

        self.app.pop_screen()

class PlaylistScreen(Screen):

    def compose(self):
        yield Static(content=playlists, classes="title")
        yield Button("Create Playlist", id="create")
        yield Button("Load Playlist", id="load")
        yield Button("Back", id="back")

    @on(Button.Pressed, "#create")
    def create(self):
        self.app.push_screen(CreatePlaylistScreen())

    @on(Button.Pressed, "#load")
    def load(self):
        self.app.push_screen(LoadPlaylistScreen())

    @on(Button.Pressed, "#back")
    def go_back(self):
        self.app.pop_screen()

# =========================
# MAIN APP CLASS
# =========================
class VIBEtui(App):

    # Load CSS file for styling
    CSS_PATH = "style.css"

    # Global key bindings
    # ("key", "action_name", "Label shown in footer")
    BINDINGS = [
        ("h", "navigate_home", "Home"),
        ("escape", "navigate_home"),
        ("q", "navigate_queue", "Queue"),
        ("p", "navigate_playlists", "Playlists"),
        ("/", "navigate_search", "Search"),
        ("t", "navigate_trending", "Trending"),
        ("<", "seek_backward", "Backward 5s"),
        ("space", "toggle_pause", "Play/Pause"),
        (">", "seek_forward", "Forward 5s"),
        ("^q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()

        # UI related state
        self.theme = "gruvbox"
        self.current_view = "none"

        # MPV controller with callback when song ends
        self.mpv = MPVController(on_song_end=self.on_song_finished)

        # Flag to differentiate manual vs automatic song changes
        self.manual_change = False

        # Index of currently playing song in queue
        self.current_song_idx = -1

        # Queue holds song dictionaries
        self.queue = []

        # Playback state
        self.is_paused = False

        self.playlistManager = PlaylistManager()


    # =========================
    # UI LAYOUT
    # =========================
    def compose(self):
        # Footer shows keybindings
        yield Footer()

        # -------- HOME PAGE --------
        with Container(id="home_page"):
            yield Static(content=logo, classes="title")
            # Dummy button used only for focus handling
            yield Button("dummy_home", classes="hidden")

        # -------- SEARCH PAGE --------
        with Container(id="search_page", classes="hidden"):
            yield Static(content=search, classes="title")
            yield Input(placeholder="Start typing...", type="text", id="search_box")
            yield ScrollableContainer(id="suggestions", classes="container hidden")
            yield ScrollableContainer(id="search_results", classes="container")
            yield Button("dummy_search", classes="hidden")

        # -------- QUEUE PAGE --------
        with Container(id="queue_page", classes="hidden"):
            yield Static(content=queue, classes="title")

            # Shown when queue is empty
            yield Static("Itna sannata kyun hai bhai??", id="silence", classes="dialog")

            yield Static(content="Currently Playing:", id="currently_playing_text", classes="dialog")

            # Music control buttons
            with Container(id="currently_playing_box", classes="hidden"):
                yield Button("<-", id="prev", classes="music_controls")
                yield Button("", id="current", classes="music_controls")
                yield Button("->", id="next", classes="music_controls")

            yield Static(content="Up Next:", id="up_next_text", classes="dialog")
            yield ScrollableContainer(id="up_next_box", classes="hidden")

            yield Button("dummy_queue", classes="hidden")

        # -------- TRENDING PAGE --------
        with Container(id="trending_page", classes="hidden"):
            yield Static(content=trending, classes="title")
            yield ScrollableContainer(id="trending_songs")
            yield Button("dummy_trending", classes="hidden")


    # =========================
    # APP LIFECYCLE
    # =========================
    def on_mount(self):
        # Start on home page
        self.install_screen(PlaylistScreen(), name="playlists")
        self.show_page("home_page")
        self.set_focus(self.query_one("#home_page"))


    # =========================
    # SONG PLAYBACK HANDLING
    # =========================
    def on_song_finished(self):
        """
        Called automatically by MPV when a song ends.
        """
        if self.manual_change:
            # Ignore end events caused by manual next/prev
            return

        # Play next song if exists
        if self.current_song_idx + 1 < len(self.queue):
            self.current_song_idx += 1
            # Thread-safe UI call
            self.call_from_thread(self._play_next_from_end)

    def _play_next_from_end(self):
        self.play_current()


    # =========================
    # PAGE NAVIGATION
    # =========================
    def show_page(self, id: str):
        """
        Shows the selected page and hides all others.
        """
        for page_idx in ["home_page", "search_page", "queue_page", "trending_page"]:
            page = self.query_one(f"#{page_idx}")
            if page_idx == id:
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
        # Always refresh queue UI
        self.update_queue_page()

    def action_navigate_trending(self):
        self.show_page("trending_page")
        self.set_focus(self.query_one("#trending_page"))

        # Load trending songs dynamically
        trending_songs = get_trending_songs()
        container = self.query_one("#trending_songs")

        for song in trending_songs:
            container.mount(
                Song(label=f'{song["title"]} \n {song["artists"]} \n {song["duration"]}',song=song, classes="listed_songs")
            )

    def action_navigate_playlists(self):
        self.push_screen("playlists")


    # =========================
    # QUEUE UI UPDATE
    # =========================
    def update_queue_page(self):
        """
        Updates 'Currently Playing' and 'Up Next' sections.
        """
        currently_playing_box = self.query_one("#currently_playing_box")
        up_next_box = self.query_one("#up_next_box")
        silence_text = self.query_one("#silence")
        current_text = self.query_one("#currently_playing_text")
        up_next_text = self.query_one("#up_next_text")

        # No songs → show silence text
        if not self.queue:
            currently_playing_box.add_class("hidden")
            up_next_box.add_class("hidden")
            current_text.add_class("hidden")
            up_next_text.add_class("hidden")
            silence_text.remove_class("hidden")
            return

        # Songs exist → show player UI
        silence_text.add_class("hidden")
        current_text.remove_class("hidden")
        currently_playing_box.remove_class("hidden")

        # Update current song title
        current_button = self.query_one("#current", Button)
        if 0 <= self.current_song_idx < len(self.queue):
            current_button.label = f'{self.queue[self.current_song_idx]["title"]}\n{self.queue[self.current_song_idx]["artists"]}'
        else:
            current_button.label = "Nothing Playing"

        # Update "Up Next"
        up_next_box.remove_children()
        if self.current_song_idx + 1 < len(self.queue):
            up_next_box.remove_class("hidden")
            up_next_text.remove_class("hidden")

            for idx in range(self.current_song_idx + 1, len(self.queue)):
                up_next_box.mount(
                    Button(f'{self.queue[idx]["title"]}\n{self.queue[idx]["artists"]}', classes="up_next_songs")
                )
        else:
            up_next_box.add_class("hidden")
            up_next_text.add_class("hidden")


    # =========================
    # PLAYBACK CONTROLS
    # =========================
    def play_current(self):
        """
        Plays the song at current_song_idx.
        """
        if not (0 <= self.current_song_idx < len(self.queue)):
            return

        song = self.queue[self.current_song_idx]
        url = f"https://www.youtube.com/watch?v={song['videoId']}"

        self.is_paused = False
        self.mpv.play(url)

        self.update_queue_page()

    def action_toggle_pause(self):
        self.is_paused = not self.is_paused
        self.mpv.toggle_pause()

    def action_seek_forward(self):
        self.mpv.seek(5)

    def action_seek_backward(self):
        self.mpv.seek(-5)

    def action_quit(self):
        self.mpv.quit()
        self.exit()


    # =========================
    # EVENT HANDLERS
    # =========================
    @on(Input.Changed, "#search_box")
    def get_search_suggestions(self, event: Input.Changed):
        """
        Fetch live suggestions while typing.
        """
        search_results = self.query_one("#search_results")
        search_results.add_class("hidden")

        container = self.query_one("#suggestions")
        container.remove_children()
        container.remove_class("hidden")

        suggestions = get_suggestions(event.input.value)
        if suggestions:
            for suggestion in suggestions:
                container.mount(
                    Button(suggestion, name=suggestion, classes="listed_suggestions")
                )

    @on(Input.Submitted, "#search_box")
    def search(self, event: Input.Submitted):
        """
        Perform search on Enter key.
        """
        suggestions = self.query_one("#suggestions")
        suggestions.add_class("hidden")

        search_results_container = self.query_one("#search_results")
        search_results_container.remove_children()
        search_results_container.remove_class("hidden")

        self.set_focus(search_results_container)

        results = search_song(event.input.value)
        for song in results:
            search_results_container.mount(
                Song(
                    label = f"{song['title']} \n {song['artists']} \n {song['duration']}",
                    song=song,
                    classes="listed_songs"
                )
            )

    @on(Button.Pressed, ".listed_suggestions")
    def search_from_suggestion(self, event: Button.Pressed):
        """
        Search using clicked suggestion.
        """
        suggestion = self.query_one("#suggestions")
        suggestion.add_class("hidden")

        search_results_container = self.query_one("#search_results")
        search_results_container.remove_children()
        search_results_container.remove_class("hidden")

        results = search_song(event.button.name)
        for song in results:
            search_results_container.mount(
                Song(
                    label = f"{song['title']} \n {song['artists']} \n {song['duration']}",
                    song=song,
                    classes="listed_songs"
                )
            )

    @on(Button.Pressed, ".listed_songs")
    def add_to_queue(self, event: Song.Pressed):
        """
        Add selected song to queue.
        """
        song_button: Song = event.button
        self.queue.append(song_button.song)

        # Auto-play if queue was empty
        if self.current_song_idx == -1:
            self.current_song_idx = 0
            self.play_current()

        self.update_queue_page()

    @on(Button.Pressed, "#next")
    def next_song(self):
        if self.current_song_idx + 1 < len(self.queue):
            self.manual_change = True
            self.current_song_idx += 1
            self.play_current()
            self.manual_change = False

    @on(Button.Pressed, "#current")
    def pause_song(self):
        self.mpv.toggle_pause()

    @on(Button.Pressed, "#prev")
    def prev_song(self):
        if self.current_song_idx - 1 >= 0:
            self.manual_change = True
            self.current_song_idx -= 1
            self.play_current()
            self.manual_change = False
        else:
            # Restart current song
            self.play_current()


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    VIBEtui().run()
