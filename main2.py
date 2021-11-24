import os
import json
import tweepy

Type = Enum("Type", "followers following")

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



followers = read_json(f"{data_folder}/utenti_followers.json")
# (Pretty) print the first three followers of Iron Man
import pprint
pp = pprint.PrettyPrinter()
utenti = ["mizzaro", "Miccighel_"]
followers_validi={}

for utente in utenti:
    temp=[]
    for follower in followers[utente]:
        if follower["followers_count"]<1000 and follower["friends_count"]<1000 and len(temp)<5:
            temp.append(follower)
        if(len(temp)==5):
            followers_validi[utente]=temp

pp.pprint(followers_validi["mizzaro"])
pp.pprint(followers_validi["Miccighel_"])