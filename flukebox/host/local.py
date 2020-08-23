""" Local host module """
from typing import List
from os import listdir
from os.path import isfile, join, splitext
import json
import ntpath
from flukebox.host.abstract_host import AbstractHost
from flukebox.host.path import Path
from flukebox.host.song import Song
from flukebox.config import get_config, get_path

class LocalHost(AbstractHost):
    """ Local host class """
    def get_songs_in_path(self, path: Path) -> List[Song]:
        """ Reads path and returns a list of URL's of songs within """
        assert path.host == "local"
        config = get_config()
        output = []
        all_files_in_path = [f for f in listdir(path.url) if isfile(join(path.url, f))]
        for candidate in all_files_in_path:
            file_split = splitext(candidate)
            extension = file_split[1].replace(".", "")
            if extension in config["hosts"]["local"]["extensions"]:
                full_path = join(path.url, candidate)
                song = Song(file_split[0], full_path)
                output.append(song)
        return output


class NewFileDetector():
    """ Detects new files on the disk """
    def __init__(self):
        self._config = get_config()
        self._path = get_path()
        self._song_file = join(self._path["data_path"], self._path["song_file"])
        self._song_dict = {}
        self._dir_list = []
        self._dir_file_list = []

    def are_there_new_files(self) -> bool:
        """ Primary method """
        self._build_dir_list()
        self._build_file_list()
        return self._delta_exists()

    def _build_dir_list(self):
        self._dir_list = []
        self._song_dict = {}
        with open(self._song_file) as song_file:
            self._song_dict = json.load(song_file)
        for path in self._song_dict["path_songs"]:
            for song in path["songs"]:
                dir, file = ntpath.split(song["url"])
                if not NewFileDetector._is_local_url(dir):
                    continue
                if not dir in self._dir_list:
                    self._dir_list.append(dir)

    @staticmethod
    def _is_local_url(url: str) -> bool:
        return url.lower()[:4] != "http"

    def _build_file_list(self):
        for dir in self._dir_list:
            for file in listdir(dir):
                full_path = join(dir, file)
                self._dir_file_list.append(full_path)

    def _delta_exists(self):
        for existing_file in self._dir_file_list:
            filename, extension = splitext(existing_file)
            extension = extension.replace(".", "")
            if not extension in self._config["hosts"]["local"]["extensions"]:
                continue
            already_exists_in_json = False
            for path in self._song_dict["path_songs"]:
                for song in path["songs"]:
                    if song["url"] == existing_file:
                        already_exists_in_json = True
                        exit
                if already_exists_in_json:
                    exit
            if not already_exists_in_json:
                return True

        for path in self._song_dict["path_songs"]:
            for song in path["songs"]:
                if not NewFileDetector._is_local_url(song["url"]):
                    continue
                if not song["url"] in self._dir_file_list:
                    return True
