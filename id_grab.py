import requests
from bs4 import BeautifulSoup


def grab_id(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    anime_id = soup.find("input", {"id": "movie_id"})["value"]

    return (anime_id)