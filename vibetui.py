from textual.app import App
from textual import on
from textual.containers import ScrollableContainer
from textual.widgets import Header, Footer, Button, Input, Static
from ytdlp import get_trending_songs, play_song, search_song

INDIA_TOP_100_TRENDING_SONGS = "https://youtube.com/playlist?list=PL4fGSI1pDJn4pTWyM3t61lOyZ6_4jcNOw&si=-XQqHOyVg7bSor0P"

songs = get_trending_songs(INDIA_TOP_100_TRENDING_SONGS)

class Player(Static):
    pass

class VIBEtui(App):
    """Main landing"""

    CSS_PATH = "style.css"

    BINDINGS = [
        ("/", "search", "Search")

    ]

    @on(Button.Pressed)
    def play(self, event: Button.Pressed):
        play_song(event.button.name)

    @on(Input.Submitted, "#search")
    def search(self, event: Input.Submitted):
        results = search_song(event.input.value)
        text_area = self.query("#search")
        text_area.remove()
        container = self.query_one("#songs")
        for x in results:
            container.mount(Button(x["title"], name=x["url"]))

    def on_mount(self):
        self.theme = "nord"

    def action_search(self):
        container = self.query_one("#songs")
        container.remove_children()
        input_area = Input(placeholder="Enter song name", type="text", id="search")
        container.mount(input_area)
        input_area.focus()

    def compose(self):
        """Creating/rendering widgets"""
        yield Header(show_clock=True)
        yield Footer()
        with ScrollableContainer(id="songs"):
            for x in songs:
                yield Button(x["title"], name=x["url"])

if __name__ == "__main__":
    VIBEtui().run()
