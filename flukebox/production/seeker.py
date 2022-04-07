""" Seeker module """
from dataclasses import dataclass
import json
from pathlib import Path
from typing import List
from flukebox.host.song import Song
from flukebox.config import get_crawled_songs, get_config
from flukebox.cpp import purify_name
from flukebox.gui import prime

@dataclass
class UrlCandidate:
    """ A candidate URL for a song """
    song: Song = None
    score: int = 0

    def __post_init__(self):
        if self.song is None:
            self.song = Song()

@dataclass
class SongContest:
    """ Song with candidate URL's """
    name: str = ""
    url_candidates: List = None

    def __post_init__(self):
        if self.url_candidates is None:
            self.url_candidates = []

    @property
    def winner(self) -> Song:
        """ Returns winner """
        output = None
        winner_score = -1
        for candidate in self.url_candidates:
            if candidate.score > winner_score:
                output = candidate.song
                winner_score = candidate.score
        if output is None:
            output = Song(name=self.name + " (?)", url="http://www.blank.org")
        return output

    def has_url_candidate(self, name: str) -> bool:
        """ Returns true if the provided name is among URL candidates """
        for candidate in self.url_candidates:
            if name == candidate.song.name:
                return True
        return False

@dataclass
class SeekState:
    """ Seek state class """
    file_path: str = ""
    seek: dict = None
    output: List = None
    crawled_songs: List = None
    song_contests: List = None

    def __post_init__(self):
        if self.seek is None:
            self.seek = {}
        if self.output is None:
            self.output = []
        if self.crawled_songs is None:
            self.crawled_songs = []
        if self.song_contests is None:
            self.song_contests = []

class ScoreCalculator:
    """ Calculates score for song name similarity """
    def __init__(self):
        self._song_name = ""
        self._candidate_name = ""
        self._score = 0

    def calculate(self, song_name: str, candidate_name: str) -> int:
        """ Calculates score """
        self._song_name = purify_name(song_name)
        self._candidate_name = purify_name(candidate_name)
        self._score = 0
        self._eval_exact()
        self._eval_contains()
        self._eval_words()
        return self._score

    def _eval_exact(self):
        if self._song_name == self._candidate_name:
            self._score += 10

    def _eval_contains(self):
        if self._song_name in self._candidate_name:
            self._score += 5

    def _eval_words(self):
        song_split = self._song_name.split(" ")
        candidate_split = self._candidate_name.split(" ")
        for song_word in song_split:
            if song_word in("", " "):
                continue
            if len(song_word) <= 1:
                continue
            for candidate_word in candidate_split:
                if song_word == candidate_word:
                    self._score += 1

class Seeker:
    """ Seeker class """
    def __init__(self):
        self._state = SeekState()
        self._config = get_config()
        self._score_calculator = ScoreCalculator()

    def seek_and_produce(self, file_path: str):
        """ Reads file, seeks contents and produces output """
        self._state = SeekState(file_path=file_path)
        self._state.crawled_songs = get_crawled_songs()
        self._read_seek_file()
        self._init_song_contests()
        self._seek()
        self._build_output()
        playlist_name = Path(file_path).name.split(".")[0]
        prime.start_gui(seeker_playlist=playlist_name, seeker_songs=self._state.output)

    def _read_seek_file(self):
        with open(self._state.file_path, encoding="utf-8") as seek_file:
            self._state.seek = json.load(seek_file)

    def _init_song_contests(self):
        for search_song in self._state.seek["seek_songs"]:
            contest = SongContest(name=search_song)
            self._state.song_contests.append(contest)

    def _seek(self):
        for contest in self._state.song_contests:
            for seekable_playlist in self._state.seek["seek_in_playlists"]:
                self._seek_playlist(contest, seekable_playlist)

    def _seek_playlist(self, contest: SongContest, seekable_playlist: str):
        for playlist in self._config["playlists"]:
            if playlist["name"] != seekable_playlist:
                continue
            if "paths" in playlist:
                for path in playlist["paths"]:
                    self._seek_path(contest, path)
            if "playlists" in playlist:
                for sub_playlist in playlist["playlists"]:
                    self._seek_playlist(contest, sub_playlist)

    def _seek_path(self, contest: SongContest, seekable_path: str):
        for path_song in self._state.crawled_songs["path_songs"]:
            if path_song["path"] != seekable_path:
                continue
            for song in path_song["songs"]:
                if contest.has_url_candidate(song["name"]):
                    continue
                score = self._score_calculator.calculate(contest.name, song["name"])
                if score <= 0:
                    continue
                if "icon_url" in song:
                    icon = song["icon_url"]
                else:
                    icon = ""
                candidate_song = Song(name=song["name"], url=song["url"], icon_url=icon)
                candidate = UrlCandidate(candidate_song, score)
                contest.url_candidates.append(candidate)

    def _build_output(self):
        for contest in self._state.song_contests:
            self._state.output.append(contest.winner)
