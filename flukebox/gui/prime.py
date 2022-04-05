import subprocess
from os import path
from flask import Flask, jsonify, request
import webview
from incubus import IncubusFactory
from flukebox import config
from flukebox.production.producer import Producer
from flukebox.host.crawler import Crawler

_CONFIG = config.get_config()
_PATH = config.get_path()
_CRAWLER = Crawler()
_INCUBUS = IncubusFactory.get_instance()
_PRODUCER = Producer()
_APP = Flask(__name__, static_folder=path.join("web", "static"))
_WINDOW = webview.create_window("FlukeBox", _APP, width=1200, height=800)

@_APP.route("/")
def home():
    """ Main view """
    return _APP.send_static_file("index.html")

@_APP.route("/api/playlists")
def api_playlists():
    _INCUBUS.user_event()
    config_dict = config.reload_config()
    return jsonify(config_dict["playlists"])

@_APP.route("/api/edit_config")
def edit_config():
    _INCUBUS.user_event()
    data_path = path.join(_PATH["data_path"], _PATH["config_file"])
    subprocess.call(["open", data_path])
    return ""

@_APP.route("/api/crawl")
def crawl():
    _CRAWLER.crawl()
    return ""

@_APP.route("/api/generate")
def api_generate():
    _INCUBUS.user_event()
    _PRODUCER.produce_with_playlist(request.args.get("playlist"))

def start_gui():
    _INCUBUS.start(5)
    #_APP.run(host="0.0.0.0", port=5001, debug=True)
    webview.start()
