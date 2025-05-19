import base64
import requests
import re

client_id = "wpierdol_tu_client_id"
client_secret = "wpierdol_tu_client_secret"

def get_access_token():
    auth = f"{client_id}:{client_secret}"
    auth_bytes = auth.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = { "Authorization": f"Basic {auth_base64}" }
    data = { "grant_type": "client_credentials" }

    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    access_token = response.json()['access_token']
    return access_token

def get_track_name(access_token, track_id):
    headers = { "Authorization": f"Bearer {access_token}" }
    url = f"https://api.spotify.com/v1/tracks/{track_id}" 

    response = requests.get(url, headers=headers)
    data = response.json()

    print("Tytuł:", data["name"])
    print("Wykonawca:", data["artists"][0]["name"])

def get_track_id(url):
    match = re.search(r"open\.spotify\.com/track/([a-zA-Z0-9]+)", url)
    if match:
        return match.group(1)
    return None

if __name__ == "__main__":
    access_token = get_access_token()
    track_id = get_track_id("https://open.spotify.com/track/1uBAuWOJkBnGCBBr3aiczY?si=70d5b45dd30c4e44")
    if track_id == None:
        print("Invalid track link.")
    else:
        print("Track ID:", track_id)
    get_track_name(access_token, "track_id")



    