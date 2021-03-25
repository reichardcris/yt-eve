import json
import urllib.request
from collections import defaultdict
from datetime import datetime


def calculate_match_points(team1, team2, score1, score2):
    if score1 == score2:
        return {team1: 1, team2: 1}
    elif score1 > score2:
        return {team1: 3, team2: 0}
    else:
        return {team1: 0, team2: 3}


class Convert:
    def __init__(self, league):
        print(league)
