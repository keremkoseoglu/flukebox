import subprocess
from os import path
from incubus import IncubusFactory
import eel
from flukebox import config
from flukebox.production.producer import Producer
from flukebox.host.crawler import Crawler

_config = config.get_config()
_path = config.get_path()
_crawler = Crawler()
_incubus = IncubusFactory.get_instance()
_producer = Producer()

@eel.expose
def edit_config():
    _incubus.user_event()
    data_path = path.join(_path["data_path"], _path["config_file"])
    subprocess.call(["open", data_path])

@eel.expose
def crawl():
    _crawler.crawl()
    eel.enableButtons()

@eel.expose
def reload():
    _incubus.user_event()
    eel.clearPlaylists()
    config_dict = config.reload_config()

    for playlist in config_dict["playlists"]:
        eel.appendPlaylist(playlist["name"])

@eel.expose
def generate(name: str):
    _incubus.user_event()
    _producer.produce_with_playlist(name)

def run_eel():
    _incubus.start(5)
    web_path = path.join("flukebox", "gui", "web")
    eel.init(web_path, allowed_extensions=[".js", ".html"])
    eel.start("index.html", size=(1200, 350))
