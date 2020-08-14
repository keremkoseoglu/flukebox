""" Primary GUI module """
from os import path
import subprocess
from PyQt5.Qt import QWidget, QLabel, QComboBox, QHBoxLayout, QVBoxLayout
from flukebox.config import get_config, get_path
from flukebox.production.producer import Producer
from flukebox.host.crawler import Crawler


class Prime(QWidget):
    """ Main GUI window """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._crawler = Crawler()
        self._producer = Producer()
        self._config = get_config()
        self._path = get_path()
        self._selected_playlist_index = 0
        self._crawl_button = QLabel(self)
        self._build_gui()

    def _build_gui(self):
        main_layout = QVBoxLayout()
        main_layout.addLayout(self._build_playlist_layout())
        main_layout.addLayout(self._build_button_layout())

        self.setLayout(main_layout)
        self.setWindowTitle("FlukeBox")
        self.show()

    def _build_playlist_layout(self) -> QHBoxLayout:
        playlist_label = QLabel(self)
        playlist_label.setText("Playlist")
        playlist_combo = QComboBox(self)
        playlist_combo.currentIndexChanged.connect(self._playlist_selected)
        for playlist in self._config["playlists"]:
            playlist_combo.addItem(playlist["name"])
        playlist_layout = QHBoxLayout()
        playlist_layout.addWidget(playlist_label)
        playlist_layout.addWidget(playlist_combo)
        return playlist_layout

    def _build_button_layout(self) -> QVBoxLayout:
        edit_button = QLabel(self)
        edit_button.setText("Edit")
        edit_button.mousePressEvent = self._edit_clicked

        self._crawl_button.setText("Crawl")
        self._crawl_button.mousePressEvent = self._crawl_clicked

        gen_button = QLabel(self)
        gen_button.setText("Play")
        gen_button.mousePressEvent = self._generate_clicked

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(edit_button)
        btn_layout.addWidget(self._crawl_button)
        btn_layout.addWidget(gen_button)
        return btn_layout

    def _playlist_selected(self, i):
        self._selected_playlist_index = i

    def _edit_clicked(self, event): # pylint: disable=W0613, R0201
        data_path = path.join(self._path["data_path"], self._path["config_file"])
        subprocess.call(["open", data_path])

    def _crawl_clicked(self, event): # pylint: disable=W0613, R0201
        self._crawl_button.setText("...")
        self._crawler.crawl()
        self._crawl_button.setText("Crawl")

    def _generate_clicked(self, event): # pylint: disable=W0613
        selected_playlist = self._config["playlists"][self._selected_playlist_index]["name"]
        self._producer.produce_with_playlist(selected_playlist)
        self.close()
