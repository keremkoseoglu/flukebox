""" Primary GUI module """
from os import path
import subprocess
from PyQt5.Qt import QWidget, QLabel, QComboBox, QHBoxLayout, QVBoxLayout
from flukebox.config import get_config, get_path, reload_config
from flukebox.production.producer import Producer
from flukebox.host.crawler import Crawler
from flukebox.host.local import NewFileDetector


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
        self._playlist_combo = QComboBox(self)
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
        self._playlist_combo.currentIndexChanged.connect(self._playlist_selected)
        self._fill_playlist_combo()
        playlist_layout = QHBoxLayout()
        playlist_layout.addWidget(playlist_label)
        playlist_layout.addWidget(self._playlist_combo)
        return playlist_layout

    def _fill_playlist_combo(self):
        self._playlist_combo.clear()
        for playlist in self._config["playlists"]:
            self._playlist_combo.addItem(playlist["name"])

    def _build_button_layout(self) -> QVBoxLayout:
        edit_button = QLabel(self)
        edit_button.setText("Edit")
        edit_button.mousePressEvent = self._edit_clicked

        reload_button = QLabel(self)
        reload_button.setText("Reload")
        reload_button.mousePressEvent = self._reload_clicked

        crawl_text = "Crawl"
        if NewFileDetector().are_there_new_files():
            crawl_text += "!"
        self._crawl_button.setText(crawl_text)
        self._crawl_button.mousePressEvent = self._crawl_clicked

        gen_button = QLabel(self)
        gen_button.setText("Play")
        gen_button.mousePressEvent = self._generate_clicked

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(edit_button)
        btn_layout.addWidget(reload_button)
        btn_layout.addWidget(self._crawl_button)
        btn_layout.addWidget(gen_button)
        return btn_layout

    def _playlist_selected(self, i):
        self._selected_playlist_index = i

    def _edit_clicked(self, event): # pylint: disable=W0613, R0201
        data_path = path.join(self._path["data_path"], self._path["config_file"])
        subprocess.call(["open", data_path])

    def _reload_clicked(self, event): # pylint: disable=W0613, R0201
        self._config = reload_config()
        self._fill_playlist_combo()

    def _crawl_clicked(self, event): # pylint: disable=W0613, R0201
        self._crawl_button.setText("...")
        self._crawler.crawl()
        self._crawl_button.setText("Crawl")

    def _generate_clicked(self, event): # pylint: disable=W0613
        selected_playlist = self._config["playlists"][self._selected_playlist_index]["name"]
        self._producer.produce_with_playlist(selected_playlist)
        self.close()
