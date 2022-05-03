""" Abstract host module """
from typing import List, Protocol
from flukebox.host.path import Path
from flukebox.host.song import Song

class Host(Protocol):
    """ Host protocol
    Each concrete host class must be derived from this abstract class
    """
    def get_songs_in_path(self, path: Path) -> List[Song]:
        """ Reads path and returns a list of URL's of songs within """
