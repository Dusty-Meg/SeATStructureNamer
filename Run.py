from datetime import datetime, timedelta
import sys
from time import sleep

import DAL
import ESI


def check_token(character_token, loop=1):
    now_plus_1 = datetime.utcnow() + timedelta(minutes=1)

    if character_token is None:
        if loop == 6:
            print("No character tokens available!")
            sys.exit(1)
        sleep(60 * loop)
        character_token = DAL.character_token(db_connection)
        return check_token(character_token, loop+1)
    else:
        if character_token['expires_on'] < now_plus_1:
            character_token = DAL.character_token(db_connection)
            return check_token(character_token)

    return character_token


print(f"Starting at {str(datetime.utcnow())}")

db_connection = DAL.db_connect()

character_token = DAL.character_token(db_connection)

character_token = check_token(character_token)

structures = DAL.all_structures(db_connection)

print(f"Got { len(structures) } structures to update!")

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
