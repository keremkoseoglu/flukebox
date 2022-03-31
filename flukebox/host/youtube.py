""" YouTube module """
from typing import List
import requests
from flukebox.host.abstract_host import AbstractHost
from flukebox.host.path import Path
from flukebox.host.song import Song
from flukebox.config import get_config, get_path

class YouTube(AbstractHost):
    """ YouTube class """
    def __init__(self):
        self._config = get_config()
        self._key = self._config["hosts"]["youtube"]["key"]
        self._icon = self._config["hosts"]["youtube"]["icon"]

    def get_songs_in_path(self, path: Path) -> List[Song]:
        """ Reads path and returns a list of URL's of songs within """
        assert path.host == "youtube"
        output = []
        url_split = path.url.split("=")
        list_id = url_split[len(url_split)-1]
        
        base_youtube_url = f"https://www.googleapis.com/youtube/v3/playlistItems?key=" \
                           f"{self._key}&playlistId={list_id}&part=contentDetails,snippet&maxResults=50"
        
        has_next_page = True
        next_page_token = ""

        while has_next_page:
            youtube_url = base_youtube_url
            if next_page_token != "":
                youtube_url += f"&pageToken={next_page_token}"

            request = requests.get(youtube_url)
            response = request.json()

            if "items" not in response:
                has_next_page = False
                continue

            for item in response["items"]:
                song_title = item["snippet"]["title"]
                song_url = "https://www.youtube.com/watch?v=" + item["contentDetails"]["videoId"]
                song = Song(song_title, song_url, self._icon)
                output.append(song)
            if "nextPageToken" not in response or response["nextPageToken"] == "":
                has_next_page = False
            else:
                next_page_token = response["nextPageToken"]
        return output
