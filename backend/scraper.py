import requests
from backend.database import matches_collection, live_collection, scorecard_collection
import time,json

MATCH_LIST_URL = "https://crickapi.com/fixture/getFixture"
MATCH_DETAIL_URL = "https://api-v1.com/w/sV3.php?key={}"
SCORECARD_DETAIL_URL="https://api-v1.com/w/sC4.php?key={}"
HOME_MAP_URL="https://oc.crickapi.com/mapping/getHomeMapData"

HEADERS = {"Content-Type": "application/json"}
PAYLOAD = {"tl": [0, 0, 0], "type": "0", "page": 0, "wise": "1", "lang": "en", "formatType": ""}
HOME_MAP_PAYLOAD = {"p":[],"s":[],"u":[],"v":[],"t":[],"lc":"en"}

def fetch_match_list():
    response = requests.post(MATCH_LIST_URL, json=PAYLOAD, headers=HEADERS)
    if response.status_code == 200:
        match_list = response.json()
        for match in match_list:
            HOME_MAP_PAYLOAD["t"]=[match["t1f"], match["t2f"]]
            HOME_MAP_PAYLOAD["s"]=[match["sf"]]
            teamnames=get_home_map_data(HOME_MAP_PAYLOAD)
            for teamname in teamnames["t"]:
                if teamname["f_key"]==match["t1f"]:
                    match["t1f"]=teamname["n"]
                if teamname["f_key"]==match["t2f"]:
                    match["t2f"]=teamname["n"]
            for seriesname in teamnames["s"]:
                if seriesname["f_key"]==match["sf"]:
                    match["sf"]=seriesname["n"]
            if match.get("mf"):
                matches_collection.update_one({"mf": match["mf"]}, {"$set": match}, upsert=True)
            else:
                match["mf"] = match["nf"]
                matches_collection.update_one({"mf": match["mf"]}, {"$set": match}, upsert=True)

def fetch_live_data():
    ongoing_matches = matches_collection.find({"status": {"$in": [1]}})
    for match in ongoing_matches:
        key = match["mf"]
        response = fetch_match_data(key)
        if not response=={}:
            live_collection.update_one({"match_id": match["mf"]}, {"$set": response}, upsert=True)

def get_home_map_data(payload):
    mapping_response = requests.post(HOME_MAP_URL, json=payload, headers=HEADERS)
    if mapping_response.status_code == 200:
        mapping_data = mapping_response.json()
        return mapping_data
    return {}
        
def get_scorecard(match_id):
    response = requests.get(SCORECARD_DETAIL_URL.format(match_id))
    if response.status_code == 200:
        scorecard = response.json()
        print(scorecard)
        HOME_MAP_PAYLOAD = {"p":[],"s":[],"u":[],"v":[],"t":[],"lc":"en"}
        bowler_names=[]
        bowler_names+=[player.split(".")[0] for player in scorecard[0]["a"]]
        if len(scorecard)>1 and scorecard[1].get("a"):
            bowler_names+=[player.split(".")[0] for player in scorecard[1]["a"]]
        batsman_names=[]
        for player in scorecard[0]["b"]:
            player_log=player.split(".")
            try:
                player_log[8]
                batsman_names.append(player_log[0])
            except:
                batsman_names.append(player_log[0].split("/")[0])
                continue
            if "/" in player_log[8]:
                batsman_names.append(player_log[8].split("/")[0])
            else:
                batsman_names.append(player_log[8])
                batsman_names.append(player_log[9].split("/")[0])
        if len(scorecard)>1:
            for player in scorecard[1]["b"]:
                player_log=player.split(".")
                try:
                    player_log[8]
                    batsman_names.append(player_log[0])
                except:
                    batsman_names.append(player_log[0].split("/")[0])
                    continue
                if "/" in player_log[8]:
                    batsman_names.append(player_log[8].split("/")[0])
                else:
                    batsman_names.append(player_log[8])
                    batsman_names.append(player_log[9].split("/")[0])
        
        HOME_MAP_PAYLOAD["p"]=list(set(batsman_names+bowler_names))
        playernames=get_home_map_data(HOME_MAP_PAYLOAD)
        str_json=json.dumps(scorecard)
        for playername in playernames["p"]:
            str_json=str_json.replace(playername["f_key"],playername["n"])
        json_data=json.loads(str_json)
        scorecard_collection.update_one({"match_id": match_id}, {"$set": {"match_data":json_data}}, upsert=True)
        return json_data

def fetch_match_data(match_id):
    response = requests.get(MATCH_DETAIL_URL.format(match_id))
    if response.status_code == 200 :
        json_data=response.json() 
        HOME_MAP_PAYLOAD = {"p":[],"s":[],"u":[],"v":[],"t":[],"lc":"en"}
        # print(json_data)
        HOME_MAP_PAYLOAD["p"]=json_data["p"].split(".")
        HOME_MAP_PAYLOAD["t"]=json_data["a"].split(".")
        playernames=get_home_map_data(HOME_MAP_PAYLOAD)
        new_names=""
        for name_sym in json_data["p"].split("."):
            for playername in playernames["p"]:
                if playername["f_key"]==name_sym:
                    new_names+=playername["n"]+"."
        team_names=""
        for name_sym in json_data["a"].split("."):
            for playername in playernames["t"]:
                if playername["f_key"]==name_sym:
                    try:
                        json_data["wp"].replace(name_sym,playername["n"])
                    except:
                        pass
                    team_names+=playername["n"]+"."
        json_data["a"]=team_names
        json_data["p"]=new_names
        json_data["mf"]=match_id
        return json_data
    else:
        return {}