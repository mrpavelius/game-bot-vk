import requests
from bs4 import BeautifulSoup


def get_top_games(num_games):
    response = requests.get("https://stopgame.ru/topgames")
    html = BeautifulSoup(response.content, "html.parser")

    top_games = []
    for game in html.select(".details"):
        title = game.select(".caption-bold > a")[0].text
        specs = game.select(".game-spec")
        genre = specs[1].text.replace("\n", " ").lstrip(" ")
        date = specs[2].text.replace("\n", " ").lstrip(" ")

        top_games.append(f"\n{title}\n{genre}\n{date}")

    return top_games[:num_games]
