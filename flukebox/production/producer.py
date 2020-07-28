""" Producer module """
from os import path
import json
from flukebox.config import get_config, get_path
from flukebox.production.writer import Writer
from flukebox.host.song import Song

class Producer:
    """ Producer class """
    def __init__(self):
        self._config = get_config()
        self._path = get_path()
        self._songs = []
        self._songs_json = {}

    def produce_with_playlist(self, playlist_name: str):
        """ Produces output for the given playlist """
        self._songs = []
        self._read_songs_json()
        self._append_playlist_to_songs(playlist_name)
        Writer().execute(self._songs)

    def _read_songs_json(self):
        self._songs_json = {}
        song_path = path.join(self._path["data_path"], self._path["song_file"])
        with open(song_path) as song_file:
            self._songs_json = json.load(song_file)

    def _append_playlist_to_songs(self, playlist_name: str):
        for playlist in self._config["playlists"]:
            if playlist["name"] == playlist_name:
                if "paths" in playlist:
                    for sub_path in playlist["paths"]:
                        self._append_path_to_songs(sub_path)
                if "playlists" in playlist:
                    for sub_playlist in playlist["playlists"]:
                        self._append_playlist_to_songs(sub_playlist)
                return

    def _append_path_to_songs(self, path_name: str):
        for path in self._songs_json["path_songs"]:
            if path["path"] == path_name:
                for song_dict in path["songs"]:
                    if not self._is_song_appended(song_dict["name"]):
                        song = Song(song_dict["name"], song_dict["url"])
                        self._songs.append(song)
                return

    def _is_song_appended(self, song_name: str) -> bool:
        for song in self._songs:
            if song.name == song_name:
                return True
        return False
