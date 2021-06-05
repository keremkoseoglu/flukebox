""" Host crawler module """
from os.path import join
import json
from flukebox.host.abstract_host import AbstractHost
from flukebox.host.local import LocalHost
from flukebox.host.spotify import Spotify
from flukebox.host.youtube import YouTube
from flukebox.host.path import Path
from flukebox.config import get_config, get_path

class Crawler:
    """ Host crawler class """
    def __init__(self):
        self._result = {}
        self._config = get_config()
        self._path = get_path()

    def crawl(self):
        """ Crawls all hosts """
        self._result["path_songs"] = []
        self._crawl_host(LocalHost(), "local")
        self._crawl_host(Spotify(), "spotify")
        self._crawl_host(YouTube(), "youtube")

        output_path = join(self._path["data_path"], self._path["song_file"])
        with open(output_path, "w") as song_file:
            json.dump(self._result, song_file)

    def _crawl_host(self, host: AbstractHost, name: str):
        for path_config in self._config["paths"]:
            if path_config["host"] != name:
                continue
            path_output = {"path": path_config["name"], "songs": []}
            path_obj = Path(path_config["name"], path_config["host"], path_config["url"])
            songs = host.get_songs_in_path(path_obj)
            for song in songs:
                song_json = {"name": song.name, "url": song.url, "icon_url": song.icon_url}
                path_output["songs"].append(song_json)
            self._result["path_songs"].append(path_output)
