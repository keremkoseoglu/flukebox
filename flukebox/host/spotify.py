""" Spotify module """
from typing import List
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flukebox.host.host import Host
from flukebox.host.path import Path
from flukebox.host.song import Song
from flukebox.config import get_config, get_path

class Spotify(Host):
    """ Spotify class """
    def __init__(self):
        self._config = get_config()
        self._path = get_path()
        cache_path = os.path.join(self._path["data_path"],
                                  self._config["hosts"]["spotify"]["cache_file"])
        self._icon = self._config["hosts"]["spotify"]["icon"]

        oauth = SpotifyOAuth(
            client_id=self._config["hosts"]["spotify"]["client_id"],
            client_secret=self._config["hosts"]["spotify"]["client_secret"],
            redirect_uri=self._config["hosts"]["spotify"]["redirect_uri"],
            show_dialog=True,
            cache_path=cache_path,
            scope="playlist-read-collaborative")

        self._spotipy = spotipy.Spotify(auth_manager=oauth)

    def get_songs_in_path(self, path: Path) -> List[Song]:
        """ Reads path and returns a list of URL's of songs within """
        assert path.host == "spotify"
        output = []
        playlist_id = path.url.split(":")[2]
        offset = 0
        while True:
            spotify_songs = self._spotipy.playlist_tracks(playlist_id, offset=offset)
            for item in spotify_songs["items"]:
                if len(item["track"]["external_urls"]) <= 0:
                    continue
                song = Song(item["track"]["name"],
                            item["track"]["external_urls"]["spotify"],
                            self._icon)
                output.append(song)
            if spotify_songs["next"] is None:
                return output
            offset += spotify_songs["limit"]
