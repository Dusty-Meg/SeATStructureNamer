import os
import sys
import time

import json
import requests


def structure(character_token, structure_id, logging, count=0):
    headers = {}
    headers['Content-Type'] = "application/json"
    headers['Accept'] = "application/json"
    headers['Authorization'] = f"Bearer {character_token['token']}"
    headers['UserAgent'] = os.environ['USER_AGENT']

    response = requests.get(
        f"https://esi.evetech.net/v2/universe/structures/{structure_id}/",
        headers=headers
    )

    if response.status_code == 200:
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return structure(character_token, structure_id, logging, count + 1)
    elif response.status_code == 502 and count < 5:
        return structure(character_token, structure_id, logging, count + 1)
    elif response.status_code == 401 or response.status_code == 403:
        reponse_json = response.json()
        logging.error(f"{str(response.status_code)} Structure Response:{str(reponse_json)}")
        if "error" in reponse_json:
            if reponse_json["error"] == "token is expired":
                return "Token"
            else:
                time.sleep(60)
                return None
    else:
        logging.error("Error fetching Structure" + str(response))
        sys.exit(1)
