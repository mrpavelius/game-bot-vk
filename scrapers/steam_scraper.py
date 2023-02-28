import requests
from bs4 import BeautifulSoup


def playing_games_now(num_games):
    response = requests.get("https://store.steampowered.com/stats/")
    html = BeautifulSoup(response.text, "html.parser")
    games = html.find_all("tr", class_="player_count_row")

    games_list = []
    for game in games[:num_games]:
        title = game.find("a").contents[0]
        players = game.find(class_="currentServers").contents[0]
        games_list.append(f"Игра: {title}\nКоличество игроков: {players}\n")

    return games_list
