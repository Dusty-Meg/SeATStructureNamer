import os
import sys
import time

import json
import requests


def structure(character_token, structure_id, count=0):
    headers = {}
    headers['Content-Type'] = "application/json"
    headers['Accept'] = "application/json"
    headers['Authorization'] = f"Bearer: {character_token['token']}"
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
