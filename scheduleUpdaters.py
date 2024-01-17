import json
from datetime import datetime
import pytz


def get_entire_ducks_schedule(file_path_from, file_path_to):
    with open(file_path_from) as file:
        json_data = json.load(file)

    home_game_data = []

    for game in json_data['events']:
        date = game['dateET']
        current_date = datetime.now()
        game_date = datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), int(date[11:13])-3, int(date[14:16]),0)
        if game['homeEventResult']['competitor']['name'] == 'Anaheim Ducks' and current_date < game_date:
            # home_game_data.append(game)
            g = {}
            g['date'] = str(game_date)
            g['opponent'] = game['awayEventResult']['competitor']['name']
            home_game_data.append(g)

    with open(file_path_to, 'w') as json_file:
        json.dump(home_game_data, json_file,indent=2)

def get_entire_angels_schedule(file_path_from, file_path_to):
    with open(file_path_from) as file:
        json_data = json.load(file)

    home_game_data = []
    for game in json_data['dates']:
        if game['games'][0]['teams']['home']['team']['name'] == 'Los Angeles Angels':
            dict = {}
            dict['date'] = utc_to_pt(game['games'][0]['gameDate'])
            dict['opponent'] = game['games'][0]['teams']['away']['team']['name']
            home_game_data.append(dict)

    with open(file_path_to, 'w') as json_file:
        json.dump(home_game_data, json_file,indent=2)

def utc_to_pt(time):
    timestamp_utc = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    utc_timezone = pytz.timezone("UTC")
    timestamp_utc = utc_timezone.localize(timestamp_utc)

    # Convert to Pacific Time
    pt_timezone = pytz.timezone("America/Los_Angeles")
    timestamp_pt = timestamp_utc.astimezone(pt_timezone)
    return str(timestamp_pt)[0:19]
    # print("UTC:", timestamp_utc)
    # print("Pacific Time:", timestamp_pt)

def get_entire_lafc_schedule(file_path_from, file_path_to):
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

def return_first_game(file_path):
    with open(file_path) as file:
        json_data = json.load(file)

    return json_data[0]

#gets all clippers home games from all nba games
# def get_entire_clippers_schedule(file_path_from, file_path_to):
#     with open(file_path_from) as file:
#         json_data = json.load(file)
#
#     all_clippers_games = []
#     for day in json_data['leagueSchedule']['gameDates']:
#         for game in day['games']:
#             if game['homeTeam']['teamName'] == 'Clippers':
#                 all_clippers_games.append(game)
#
#
#     with open(file_path_to, 'w') as file:
#         json.dump(all_clippers_games, file, indent=2)


def get_current_clippers_game(file_path):
    with open(file_path) as file:
        json_data = json.load(file)
    return json_data

def send_current_clippers_game(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent = 2)



def get_entire_clippers_schedule(file_path_from, file_path_to):
    with open(file_path_from) as file:
        json_data = json.load(file)

    data = []
    for game in json_data:
        date = game['homeTeamTime']
        current_date = datetime.now()
        game_date = datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), int(date[11:13]),int(date[14:16]), 0)
        if current_date < game_date:
            dic = {}
            dic['date'] = game['homeTeamTime'][0:10]+" "+game['homeTeamTime'][11:19]
            dic['opponent'] = game['awayTeam']['teamCity']+" "+game['awayTeam']['teamName']
            dic['gameId'] = game['gameId']
            data.append(dic)


    with open(file_path_to, 'w') as file:
        json.dump(data, file, indent=2)

get_entire_ducks_schedule('jsonFiles/jsonDucks/allDucksGames.json', 'jsonFiles/jsonDucks/ducksGamesUpdated.json')
get_entire_lafc_schedule('jsonFiles/jsonLAFC/allLafcGames.json', 'jsonFiles/jsonLAFC/lafcGamesUpdated.json')
get_entire_clippers_schedule('jsonFiles/jsonClippers/allClippersGames.json', 'jsonFiles/jsonClippers/clippersGamesUpdated.json')
get_entire_angels_schedule('jsonFiles/jsonAngels/allAngelsGames.json',
                           'jsonFiles/jsonAngels/angelsGamesUpdated.json')