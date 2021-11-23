import os
import json
import tweepy
from enum import Enum

Type=Enum("Type","followers following")
    

api_key = "VlNL2LO3nPv8sN7HoTwiHPWRJ"
api_secret = "0x66wQ6hJrEF0sRsDDBk5F84GPdZrW7ofrLAHG9d4VOKpuNDU8"
access_token = "4878912292-yHYq0PzMFAzOgHmQ5CQG0Ls7tiqGOIcV7jKOxzu"
access_secret = "9uJKXlMqXrRtn9TxqtAL2SBv8fLGVZH4bu6IcHhKCDbMt"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAA2xVwEAAAAAWWRrvmkGwNuTP%2FMltp7z1%2F1Wh5A%3DuCQUQaeBJ9EEmLrOPUGoDZ4bI6s1fEzguiNNOyceGGFjhKmFPn"

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
if (api.verify_credentials):
    print('Authentication completed successfully!')


data_folder = "data"


def serialize_json(folder, filename, data):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    with open(f"{folder}/{filename}", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.close()
    print(f"Data serialized to path: {folder}/{filename}")


def read_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf8") as file:
            data = json.load(file)
        print(f"Data read from path: {path}")
        return data
    else:
        print(f"No data found at path: {path}")
        return {}

def findUsers(utente,type):
    print(f"Processing User {utente}")
    users = []

    while len(users) < 5:
        if(type==Type.followers):
            item = tweepy.Cursor(api.followers, screen_name=utente, skip_status=True, include_user_entities=False).items(1).next()
        elif(type==Type.following):
            item = tweepy.Cursor(api.friends, screen_name=utente, skip_status=True, include_user_entities=False).items(1).next()

        json_data = item._json

        found_user = {}
        found_user["id"] = json_data["id"]
        found_user["name"] = json_data["name"]
        found_user["screen_name"] = json_data["screen_name"]
        found_user["location"] = json_data["location"]
        found_user["followers_count"] = json_data["followers_count"]
        found_user["friends_count"] = json_data["friends_count"]

        if found_user not in users and found_user["followers_count"] < 1000 and found_user["friends_count"] < 1000:
            users.append(found_user)

    return users

def userDetails(utente):
    raw_data = api.get_user(utente)
    json_data = raw_data._json
    profile_data = {}
    profile_data["id"] = json_data["id"]
    profile_data["name"] = json_data["name"]
    profile_data["screen_name"] = json_data["screen_name"]
    profile_data["location"] = json_data["location"]
    profile_data["description"] = json_data["description"]
    profile_data["followers_count"] = json_data["followers_count"]

    return profile_data

utenti = ["mizzaro", "Miccighel_"]
followersl1 = {}
followingl1 = {}
followersl2 = {}
followingl2 = {}
followers_datal1 = {}
following_datal1 = {}

#Followers e following dei primi due account (followers e following di primo livello)
for utente in utenti:

    print(f"Processing User {utente}")

    followersl1[utente] = findUsers(utente, Type.followers)

    followingl1[utente] = findUsers(utente, Type.following)

    #Follower e following dei followers di primo livello
    for follower in followersl1[utente]:
        followers_datal1[follower["id"]]=userDetails(follower["id"])
        followersl2[utente][follower["id"]]=findUsers(follower["id"],Type.followers)

        followingl2[utente][follower["id"]] = findUsers(follower["id"], Type.following)

    # Follower e following dei following di primo livello
    for following in followingl1[utente]:
        followersl2[utente][following["id"]] = findUsers(following["id"], Type.followers)

        following_datal1[following["id"]] = userDetails(following["id"])
        followingl2[utente][following["id"]] = findUsers(following["id"], Type.following)


    print(f"Found {len(followersl1[utente])} followers for user {utente}")




