""" Song module """
from flukebox.config import get_config

class Song():
    """ Song class """
    def __init__(self, name:str = "", url:str = "", icon_url: str = ""):
        self.name = name
        self.url = url

        if icon_url == "":
            current_config = get_config()
            self.icon_url = current_config["settings"]["unknown_icon"]
        else:
            self.icon_url = icon_url
