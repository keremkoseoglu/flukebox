""" Writer module """
from typing import List
import os
from os import path
import html
from flukebox.host.song import Song
from flukebox.config import get_config
from flukebox.cpp import purify_song_name

class Writer:
    """ Write class """
    def __init__(self):
        self._songs = []
        self._playlist_name = ""
        self._songlist_code = ""
        self._playlist_code = ""
        self._output = ""
        self._config = get_config()

    def execute(self, playlist_name: str, songs: List[Song]):
        """ Executes the write operation for passed songs """
        self._playlist_name = playlist_name
        self._songs = songs

        self._build_songlist_code()
        self._build_playlist_code()
        self._build_output()
        self._write()
        self._open_player()

    def _build_songlist_code(self):
        self._songlist_code = ""
        song_index = -1
        for song in self._songs:
            song_index += 1
            song_index_txt = str(song_index)
            icode = f'<img src="{song.icon_url}">'
            self._songlist_code += f'<nobr>{icode} <a href="#" onClick="setSongAndPlay({song_index_txt});">'
            self._songlist_code += f'{purify_song_name(song.name)}</a>'
            self._songlist_code += f'<span id="arrow_{song_index_txt}"><big> ⭐️</big></span></nobr> &nbsp;&nbsp;'

    def _build_playlist_code(self):
        self._playlist_code = ""
        song_index = -1
        for song in self._songs:
            song_index += 1
            if song_index > 0:
                self._playlist_code += ', '
            self._playlist_code += '{'
            self._playlist_code += f'"name": "{purify_song_name(song.name)}", '
            self._playlist_code += f'"url": "{song.url}", '
            self._playlist_code += f'"icon": "{song.icon_url}"'
            self._playlist_code += '}'

    def _build_output(self):
        self._output = ""
        tmp_path = path.join(os.getcwd(), "flukebox", "www", "player_template_v2.html")
        with open(tmp_path) as tmp_file:
            self._output = tmp_file.read()
        self._output = self._output.replace("{{PLAYLIST_NAME}}", self._playlist_name)
        self._output = self._output.replace("{{SONGLIST}}", self._songlist_code)
        self._output = self._output.replace("{{PLAYLIST}}", self._playlist_code)
        self._output = self._output.replace("{{SONGCOUNT}}", str(len(self._songs)))

    def _write(self):
        with open(self._config["settings"]["output_file"], "w") as output_file:
            output_file.write(self._output)

    def _open_player(self):
        os.system(f'open {self._config["settings"]["output_file"]}')
