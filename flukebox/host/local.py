""" Local host module """
from typing import List
from os import listdir
from os.path import isfile, join, splitext
from flukebox.host.abstract_host import AbstractHost
from flukebox.host.path import Path
from flukebox.host.song import Song
from flukebox.config import get_config

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
