""" Song module """
from dataclasses import dataclass
from flukebox.config import get_config

@dataclass
class Song():
    """ Song class """
    name: str = ""
    url: str = ""
    icon_url: str = ""

    def __post_init__(self):
        if self.icon_url == "":
            current_config = get_config()
            self.icon_url = current_config["settings"]["unknown_icon"]
