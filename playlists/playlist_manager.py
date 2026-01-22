import json
from pathlib import Path

class PlaylistManager:
    def __init__(self, path="./playlists.json"):
        self.path = Path(path)
        self.playlists: dict[str,list[dict]] | None = None
        self.dirty = False

    def load(self):
        if self.playlists is not None:
            return
        
        if self.path.exists():
            with open(self.path, "r") as f:
                self.playlists = json.load(f);

        else:
            self.playlists = {}

    def save(self):
        if not self.dirty:
            return
        with open(self.path, "w") as f:
            json.dump(self.playlists, f, indent=4)
        self.dirty = False

    def create(self, name:str):
        self.load()
        assert self.playlists is not None
        if name not in self.playlists:
            self.playlists[name] = []
            self._dirty = True

    def add_song(self, name: str, song: dict):
        self.load()
        assert self.playlists is not None
        self.playlists[name].append(song)
        self.dirty = True

    def get(self, name: str) -> list[dict]:
        self.load()
        assert self.playlists is not None
        return self.playlists.get(name, [])

    def all(self) -> dict[str, list[dict]]:
        self.load()
        assert self.playlists is not None
        return self.playlists
    
    def names(self) -> list[str]:
        self.load()
        assert self.playlists is not None
        return list(self.playlists.keys())