import os
import sys
import base64
import time

import json
import requests


def refresh_token(character_token, count=0):
    token = base64.b64encode(os.environ['ESI_KEY'].encode("utf-8"))
    token = str(token, "utf-8")

    headers = {}
    headers['Content-Type'] = "application/x-www-form-urlencoded"
    headers['Host'] = "login.eveonline.com"
    headers['Authorization'] = f"Basic {token}"

    data = "grant_type=refresh_token&refresh_token=" + character_token[2]

    response = requests.post(
        "https://login.eveonline.com/v2/oauth/token/",
        headers=headers,
        data=data)

    if response.status_code == 200:
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return refresh_token(character_token, count + 1)
    elif count < 2:
        time.sleep(5 * (count + 1))
        return refresh_token(character_token, count + 1)
    else:
        print("Error refreshing token: " + str(response))
        sys.exit(1)


def structure(character_token, structure_id, count=0):
    headers = {}
    headers['Content-Type'] = "application/json"
    headers['Accept'] = "application/json"
    headers['Authorization'] = f"Bearer: {character_token[1]}"
    headers['UserAgent'] = os.environ['USER_AGENT']

    response = requests.get(
        f"https://esi.evetech.net/v2/universe/structures/{structure_id}/",
        headers=headers
    )

    if response.status_code == 200:
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return structure(character_token, structure_id, count + 1)
    elif response.status_code == 502 and count < 5:
        return structure(character_token, structure_id, count + 1)
    elif response.status_code == 401 or response.status_code == 403:
        time.sleep(60)
        return None
    else:
        print("Error fetching Structure" + str(response))
        sys.exit(1)
