import requests
import json

#url needs to add gameID.json
url = "https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_"

payload = ""
headers = {
    "cookie": "ak_bmsc=55F7E0A5A45CF8D77178F2A0055B2E1B~000000000000000000000000000000~YAAQq7vOFzjNoKCMAQAAX5QwwhbYZG%2Bu9EkLNnoHBJPBP3Nrv3oQXCtZhzJ9EHYSA%2Fue6EKRJ8kjrVagcHmkyItgMqIzeg9juh38wi5myBYYbCfEamFhiXqBPy%2BtQiDb7DQYaqZ5HnYy2q47v7AF%2FI39sFuzlB6%2Bg6RloQfB5O6kjZYwI6a64awmhNbJz%2BvCSzF7e7NcQb0OWehoBF53TIEkwW0%2BeKh3ProUkpkA%2FN0WFKPtLROmv885VMZ5gyPijvOCjM73Mh3UrAReju8TONZt0Zfi6FT%2BmKLoQrCedXv7fksnFk9RMBU35oC%2BmTx8wpTQI3nI9wO6x1YOv0B%2Fk%2BhP7CEhBnfgjL9aUSqG4v4vg3gjr%2FBxj%2F6PAi5Na1h1dDHNv%2FXKXBbWeorFMXeJwaMdr2jApL0evblY0W2MN24%3D",
    "authority": "cdn.nba.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "if-modified-since": "Sat, 30 Dec 2023 00:38:26 GMT",
    "if-none-match": "^\^4674c746d4c2445a576b4b7a02e4e3bb^^",
    "origin": "https://www.nba.com",
    "referer": "https://www.nba.com/",
    "sec-ch-ua": "^\^Not_A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def missed_freethrows():
    try:
        with open('jsonFiles/jsonClippers/liveBasketballData.json') as f:
            jsondata = json.load(f)

        actions = jsondata['game']['actions']
        for actionNum in range(len(actions)):
            action = actions[actionNum]
            if action['period'] == 4 and action['actionType'] == 'freethrow' and action['teamTricode'] != "LAC" and action['subType'] == "1 of 2" and action['shotResult'] == 'Miss' and actionNum != len(actions)-1:
                actionNumPlus = actions[actionNum+2]
                if actionNumPlus['shotResult'] == 'Missed':
                    return True
        return False
    except:
        RuntimeError("could not retrieve data")

def clippers_game_over(gameId):
    try:
        response = requests.request("GET", url+gameId+".json", data=payload, headers=headers)
        data = response.text

        json_data = json.loads(data)

        with open('jsonFiles/jsonClippers/liveBasketballData.json', 'w') as json_file:
            json.dump(json_data, json_file, indent = 2)

        with open('jsonFiles/jsonClippers/liveBasketballData.json') as f:
            jsondata = json.load(f)

        actions = jsondata['game']['actions']

        return actions[len(actions)-1] == 'Game End'
    except:
        RuntimeError("could not retrieve data")

def game_over(gameId):
    try:
        response = requests.request("GET", url+gameId+".json", data=payload, headers=headers)
        data = response.text

        json_data = json.loads(data)

        with open('jsonFiles/jsonClippers/liveBasketballData.json', 'w') as json_file:
            json.dump(json_data, json_file, indent = 2)

        with open('jsonFiles/jsonClippers/liveBasketballData.json') as f:
            jsondata = json.load(f)

        actions = jsondata['game']['actions']

        return actions[len(actions)-1] == 'Game End'
    except:
        RuntimeError("could not retrieve data")

# def clippers_test():
#     with open('jsonFiles/jsonClippers/liveBasketballData.json') as f:
#         jsondata = json.load(f)
#
#     actions = jsondata['game']['actions']
#
#     return actions[len(actions) - 1]['description'] == 'Game End'