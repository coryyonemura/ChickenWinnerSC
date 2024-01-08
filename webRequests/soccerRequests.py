import requests
import json

url = "https://api.sofascore.com/api/v1/sport/football/events/live"

payload = ""
headers = {
    "authority": "api.sofascore.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "if-none-match": "W/^\^f1a4d0cd51^^",
    "origin": "https://www.sofascore.com",
    "referer": "https://www.sofascore.com/",
    "sec-ch-ua": "^\^Not_A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def lafc_game_over():
    try:
        response = requests.request("GET", url, data = payload, headers = headers)
        data = response.text

        json_data = json.loads(data)
        with open("jsonFiles/jsonLAFC/liveSoccerData.json", 'w') as json_file:
            json.dump(json_data, json_file, indent = 2)

        with open('jsonFiles/jsonLAFC/liveSoccerData.json') as f:
            jsondata = json.load(f)

        for game in jsondata["events"]:
            if game['homeTeam']['name'] == "LAFC":
                return False
        return True

    except:
        RuntimeError("could not retrieve data")

def lafc_game():
    with open('jsonFiles/jsonLAFC/liveSoccerData.json') as f:
        jsondata = json.load(f)

    for game in jsondata['events']:
        if game['homeTeam']['name'] == "LAFC":
            lafcScore = game['homeScore']['current']
            awayScore = game['awayScore']['current']
            return lafcScore > awayScore


