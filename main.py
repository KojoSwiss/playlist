import requests
from bs4 import BeautifulSoup
my_date = input("What year would you like to travel to?\nPlease enter the year in YYYY-MM-DD:\n")

URL = f"https://www.billboard.com/charts/hot-100/{my_date}"

response = requests.get(url=URL)
data = response.text

soup = BeautifulSoup(data, 'html.parser')

all_songs = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")


all_songs = [song.getText() for song in all_songs]

playlist = [f"{song}\n"for song in all_songs]

print(playlist)
