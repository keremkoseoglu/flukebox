""" Config module """
import os
from os import path
import json

_PATH_FILE = "path.json"
_CONFIG = {}
_PATH = {}

def get_config() -> dict:
    """ Returns configuration """
    global _CONFIG
    if _CONFIG == {}:
        _read_config()
    return _CONFIG

def get_path() -> dict:
    """ Returns path configuration """
    global _PATH
    if _PATH == {}:
        _read_path()
    return _PATH

def get_crawled_songs() -> dict:
    """ Reads the song file and returns contents """
    output = {}
    song_path = path.join(_PATH["data_path"], _PATH["song_file"])
    with open(song_path) as song_file:
        output = json.load(song_file)
    return output

def reload_config() -> dict:
    """ Reloads config from the disk """
    global _CONFIG
    _CONFIG = {}
    return get_config()

def _read_config():
    global _CONFIG, _PATH
    _CONFIG = {}
    _read_path()
    config_path = path.join(_PATH["data_path"], _PATH["config_file"])
    with open(config_path) as config_file:
        _CONFIG = json.load(config_file)

def _read_path():
    global _PATH
    _PATH = {}
    path_path = path.join(os.getcwd(), _PATH_FILE)
    with open(path_path) as path_file:
        _PATH = json.load(path_file)
