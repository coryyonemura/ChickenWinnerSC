import requests
import json
import os

url = "https://api.sofascore.com/api/v1/sport/ice-hockey/events/live"

payload = ""
headers = {
    "authority": "api.sofascore.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "if-none-match": "W/^\^0af0ad12c9^^",
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

def get_score():
    try:
        response = requests.request("GET", url, data=payload, headers=headers)
        data = response.text

        json_data = json.loads(data)

        with open('jsonFiles/liveData.json', 'w') as json_file:
            json.dump(json_data, json_file, indent = 2)

        with open('jsonFiles/liveData.json') as f:
            jsondata = json.load(f)
        # print('works')

    except:
        # print("didn't work")
        RuntimeError("Could not retrieve data")

    for game in jsondata['events']:
        if game['homeTeam']['name'] == 'Anaheim Ducks':
            return game['homeScore']['current']

    return -1



print(get_score())