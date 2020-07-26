import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flukebox.config import get_config, get_path

def test1():
    config = get_config()
    fpath = get_path()
    cache_path = os.path.join(fpath["data_path"], config["api"]["spotify"]["cache_file"])

    oauth = SpotifyOAuth(
        client_id=config["api"]["spotify"]["client_id"],
        client_secret=config["api"]["spotify"]["client_secret"],
        redirect_uri=config["api"]["spotify"]["redirect_uri"],
        show_dialog=True,
        cache_path=cache_path,
        scope="playlist-read-collaborative"
    )

    sp = spotipy.Spotify(auth_manager=oauth)

    results = sp.playlist_tracks("4LvKfarGwOqQZbfnlwBP95")
    for item in results['items']:
        url = item["track"]["external_urls"]["spotify"]
        print(url)