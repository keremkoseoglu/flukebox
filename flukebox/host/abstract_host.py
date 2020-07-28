""" Abstract host module """
from abc import ABC, abstractmethod
from typing import List
from flukebox.host.path import Path
from flukebox.host.song import Song

class AbstractHost(ABC):
    """ Abstract host class
    Each concrete host class must be derived from this abstract class
    """

    @abstractmethod
    def get_songs_in_path(self, path: Path) -> List[Song]:
        """ Reads path and returns a list of URL's of songs within """
