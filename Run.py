from datetime import datetime, timedelta
import sys
from time import sleep
import logging

import DAL
import ESI

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


def check_token(character_token, db_connection, loop=1):
    now_plus_1 = datetime.utcnow() + timedelta(minutes=1)

    if character_token is None:
        if loop == 20:
            logging.error("No character tokens available!")
            sys.exit(1)
        sleep(60 * loop)
        character_token = DAL.character_token(db_connection, logging)
        return check_token(character_token, db_connection, loop+1)
    else:
        if character_token['expires_on'] < now_plus_1:
            character_token = DAL.character_token(db_connection, logging)
            return check_token(character_token, db_connection)

    return character_token


def check_structure(character_token, structure, logging, db_connection):
    esi_model = ESI.structure(
        character_token,
        structure['structure_id'],
        logging
    )

    if esi_model == "Token":
        character_token = check_token(character_token, db_connection)
        check_structure(character_token, structure, logging, db_connection)
    elif esi_model is None:
        DAL.FailStructure(db_connection, structure['structure_id'])
    else:
        DAL.UpdateStructure(db_connection, structure['structure_id'], esi_model)


logging.info(f"Starting at {str(datetime.utcnow())}")

db_connection = DAL.db_connect(logging)

character_token = DAL.character_token(db_connection, logging)
logging.error(f"Char token! {character_token}")

character_token = check_token(character_token, db_connection)

structures = DAL.all_structures(db_connection)

logging.info(f"Got { len(structures) } structures to update!")

for structure in structures:
    now = datetime.utcnow()
    downtime_start = datetime(
        now.year,
        now.month,
        now.day,
        10, 58, 00)
    downtime_end = datetime(
        now.year,
        now.month,
        now.day,
        11, 15, 00)

    if now > downtime_start and now < downtime_end:
        logging.info("Finishing as hit Downtime!")
        sys.exit(0)

    logging.info(f"Running structure: {structure['structure_id']}")
    check_structure(character_token, structure, logging, db_connection)

logging.info(f"Finished successfully at {str(datetime.utcnow())}")
sys.exit(0)
