""" Producer module """
from typing import List
from flukebox.config import get_config, get_path, get_crawled_songs
from flukebox.cpp import purify_song_name
from flukebox.host.song import Song

class Producer:
    """ Producer class """
    def __init__(self):
        self._config = get_config()
        self._path = get_path()
        self._songs = []
        self._songs_json = {}

    def build_song_list(self, playlist_name: str,
                        no_local: bool = False,
                        purify: bool = False
                       ) -> List[Song]:
        """ Builds song list """
        self._songs = []
        self._songs_json = get_crawled_songs()

        if purify:
            for path_entry in self._songs_json["path_songs"]:
                for song in path_entry["songs"]:
                    song["name"] = purify_song_name(song["name"])

        self._append_playlist_to_songs(playlist_name, no_local=no_local)
        return self._songs

    def _append_playlist_to_songs(self, playlist_name: str, no_local: bool = False):
        for playlist in self._config["playlists"]:
            if playlist["name"] == playlist_name:
                if "paths" in playlist:
                    for sub_path in playlist["paths"]:
                        self._append_path_to_songs(sub_path, no_local=no_local)
                if "playlists" in playlist:
                    for sub_playlist in playlist["playlists"]:
                        self._append_playlist_to_songs(sub_playlist, no_local=no_local)
                return

    def _append_path_to_songs(self, path_name: str, no_local: bool = False):
        for path_entry in self._songs_json["path_songs"]:
            if path_entry["path"] == path_name:
                if no_local and self._is_path_local(path_name):
                    return
                for song_dict in path_entry["songs"]:
                    if not self._is_song_appended(song_dict["name"]):
                        if "icon_url" in song_dict:
                            icon = song_dict["icon_url"]
                        else:
                            icon = ""
                        song = Song(song_dict["name"], song_dict["url"], icon)
                        self._songs.append(song)
                return

    def _is_song_appended(self, song_name: str) -> bool:
        for song in self._songs:
            if song.name == song_name:
                return True
        return False

    def _is_path_local(self, path_name: str) -> bool:
        for path_entry in self._config["paths"]:
            if path_entry["name"] == path_name:
                return path_entry["host"] == "local"
        return False
