from datetime import datetime, timedelta
import sys

import DAL
import ESI


def check_token(character_token):
    now_plus_1 = datetime.utcnow() + timedelta(minutes=1)

    if character_token[3] < now_plus_1:
        result = ESI.refresh_token(character_token)

        character_token[1] = result["access_token"]
        character_token[2] = result["refresh_token"]
        character_token[3] = (
            datetime.utcnow() + timedelta(seconds=int(result["expires_in"])))

    return character_token


db_connection = DAL.db_connect()

character_token = DAL.character_token(db_connection)

character_token = check_token(character_token)

structures = DAL.all_structures(db_connection)

for structure in structures:
    print(f"Running structure: {structure[0]}")
    character_token = check_token(character_token)

    esi_model = ESI.structure(
        character_token,
        structure[0]
    )

    if esi_model is None:
        DAL.FailStructure(db_connection, structure[0])
    else:
        DAL.UpdateStructure(db_connection, structure[0], esi_model)

print(f"Finished successfully at {str(datetime.utcnow())}")
sys.exit(0)
