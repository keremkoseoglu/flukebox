""" Primary GUI module """
import subprocess
import os
from os import path
from typing import List
from flask import Flask, jsonify, request
import webview
from flukebox import config
from flukebox.production.producer import Producer
from flukebox.host.crawler import Crawler

_CONFIG = config.get_config()
_PATH = config.get_path()
_CRAWLER = Crawler()
_PRODUCER = Producer()
_APP = Flask(__name__, static_folder=path.join("web", "static"))
_PLAYLIST_WINDOW = webview.create_window("FlukeBox", _APP, width=896, height=1120, x=0, y=0)
_PLAYER_WINDOW = webview.create_window("Player",
                                       html="<body bgcolor=black />",
                                       width=896,
                                       height=1120,
                                       x=896,
                                       y=0)
_START_PLAYLIST = ""
_START_NO_LOCAL = False
_SEEKER_PLAYLIST = ""
_SEEKER_SONGS = []

@_APP.route("/")
def home():
    """ Main view """
    return _APP.send_static_file("index.html")

@_APP.route("/api/start_playlist")
def start_playlist():
    """ Main view """
    output = {"start_playlist": _START_PLAYLIST,
              "no_local": _START_NO_LOCAL}
    return jsonify(output)

@_APP.route("/api/playlists")
def api_playlists():
    """ Returns all playlists """
    if _SEEKER_PLAYLIST != "":
        seeker_list = [{"name": _SEEKER_PLAYLIST}]
        return jsonify(seeker_list)
    config_dict = config.reload_config()
    return jsonify(config_dict["playlists"])

@_APP.route("/api/edit_config")
def edit_config():
    """ Edit configuration file """
    data_path = path.join(_PATH["data_path"], _PATH["config_file"])
    subprocess.call(["open", data_path])
    return ""

@_APP.route("/api/crawl")
def crawl():
    """ Crawls websites """
    _CRAWLER.crawl()
    return ""

@_APP.route("/api/generate")
def api_generate():
    """ Generates file list of playlist """
    no_local = request.args.get("no_local") == "true"
    if len(_SEEKER_SONGS) > 0:
        songs = _SEEKER_SONGS
    else:
        songs = _PRODUCER.build_song_list(request.args.get("playlist"),
                                          no_local=no_local, purify=True)
    return jsonify(songs)

@_APP.route("/api/play")
def api_play():
    """ Plays given URL """
    url = request.args.get("url")
    _PLAYER_WINDOW.load_url(url)
    return ""

@_APP.route("/api/stop")
def api_stop():
    """ Stops player """
    #_PLAYER_WINDOW.load_url("https://this-page-intentionally-left-blank.org/")
    _PLAYER_WINDOW.load_html("")
    return ""

@_APP.route("/api/quit")
def api_quit():
    """ Quits app """
    os._exit(os.EX_OK)
    return ""

def start_gui(playlist:str=None,
              no_local:bool=None,
              seeker_playlist:str=None,
              seeker_songs:List=None):
    """ Main method to start GUI """
    global _START_PLAYLIST
    global _START_NO_LOCAL
    global _SEEKER_PLAYLIST
    global _SEEKER_SONGS

    if playlist is not None:
        _START_PLAYLIST = playlist
    if no_local is not None:
        _START_NO_LOCAL = no_local
    if seeker_playlist is not None:
        _SEEKER_PLAYLIST = seeker_playlist
        _START_PLAYLIST = seeker_playlist
    if seeker_songs is not None:
        _SEEKER_SONGS = seeker_songs

    #_APP.run(host="0.0.0.0", port=5001, debug=True)
    webview.start()
