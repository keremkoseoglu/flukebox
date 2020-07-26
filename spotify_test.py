import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def test1():
    """
    os.environ["SPOTIPY_CLIENT_ID"] = "3e026c6d36f64582bbe4b0398118520d"
    os.environ["SPOTIPY_CLIENT_SECRET"] = "e16b1581dbfc4eb98fe4c3f1fdd463dc"
    os.environ["SPOTIPY_REDIRECT_URI"] = "http://www.keremkoseoglu.com"

    scope = "user-library-read"
    """

    oauth = SpotifyOAuth(
        client_id="3e026c6d36f64582bbe4b0398118520d",
        client_secret="e16b1581dbfc4eb98fe4c3f1fdd463dc",
        redirect_uri="http://www.keremkoseoglu.com",
        show_dialog=True,
        cache_path="/Users/kerem/Downloads/tmp.txt",
        scope="playlist-read-collaborative"
    )

    sp = spotipy.Spotify(auth_manager=oauth)

    results = sp.playlist_tracks("4LvKfarGwOqQZbfnlwBP95")
    for item in results['items']:
        url = item["track"]["external_urls"]["spotify"]
        print(url)