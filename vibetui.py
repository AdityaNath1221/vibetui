from textual.app import App
from textual.widgets import Header, Footer

class vibetui(App):
    """Main landing"""

    BINDINGS = [
        ("D", "toggle_dark", "Toggle Dark Mode")
    ]

    def compose(self):
        """Creating/rendering widgets"""
        yield Header(show_clock=True)
        yield Footer()

if __name__ == "__main__":
    vibetui().run()
