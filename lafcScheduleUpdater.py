import json
from datetime import datetime
import os


def get_entire_schedule(file_path_from, file_path_to):
    with open(file_path_from) as file:
        json_data = json.load(file)

    home_game_data = []

    for game in json_data:
        date = game['matchDate']
        current_date = datetime.now()
        game_date = datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), int(date[11:13]), int(date[14:16]),0)
        if game['home']['shortName'] == 'LAFC' and current_date < game_date:
            # home_game_data.append(str(game_date))
            g = {}
            g['date'] = str(game_date)
            g['opponent'] = game['away']['fullName']
            home_game_data.append(g)

    with open(file_path_to, 'w') as json_file:
        json.dump(home_game_data, json_file,indent=2)


def update_schedule(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    if data:
        data.pop(0)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# def print_remaining_schedule(file_path):
#     f = os.path.join('jsonFiles', file_path)
#     with open(f) as file:
#         json_data = json.load(file)
#
#     for game in json_data:
#         print(game)

# def return_first_game(file_path):
#     f = os.path.join('jsonFiles', file_path)
#     with open(f) as file:
#         json_data = json.load(file)
#
#     return json_data[0]

def get_next_gametime(file_path):
    with open(file_path) as file:
        json_data = json.load(file)
    return json_data[0]


# get_entire_schedule('allDucksGames.json', 'ducksScheduleUpdated.json')
# update_schedule("ducksScheduleUpdated.json")
get_entire_schedule('jsonFiles/allLafcGames.json', 'jsonFiles/lafcGamesUpdated.json')

