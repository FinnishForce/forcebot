import json
import random


def get_game_by_provider(provider):
    with open("gamelists/"+provider+".txt", 'r') as f:
        gamelist = json.load(f)
    random.shuffle(gamelist)
    return random.choice(gamelist)