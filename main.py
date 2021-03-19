from datetime import date
from pprint import pprint

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
ClIENT_SECRET = os.environ.get("SPOTIFY_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id=CLIENT_ID,
        client_secret=ClIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
    )
)
user_id = sp.current_user()["id"]

my_date = input("What year would you like to travel to?\nPlease enter the year in YYYY-MM-DD:\n")

URL = f"https://www.billboard.com/charts/hot-100/{my_date}"

response = requests.get(url=URL)
data = response.text

soup = BeautifulSoup(data, 'html.parser')

all_songs = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")

all_song = [song.getText() for song in all_songs]

# song_names = ["The list of song", "titles from your", "web scrape"]

song_uris = []
year = my_date.split("-")[0]

for song in all_song:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        pass

playlist = sp.user_playlist_create(user=user_id, name=f"{my_date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)