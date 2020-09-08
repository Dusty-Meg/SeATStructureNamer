import os
import sys

import mariadb


def db_connect():
    try:
        return mariadb.connect(
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=int(os.environ['DB_PORT']),
            database=os.environ['DB_DATABASE']
            )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)


def character_token(db_connection):
    cursor = db_connection.cursor()

    cursor.execute(
        "SELECT "
        "user.character_id, refreshtoken.token, "
        "refreshtoken.refresh_token, refreshtoken.expires_on "
        "FROM character_infos AS user "
        "INNER JOIN "
        "refresh_tokens AS refreshtoken "
        "ON user.character_id = refreshtoken.character_id "
        "WHERE refreshtoken.deleted_at IS NULL "
        "AND user.corporation_id = %s "
        "ORDER BY refreshtoken.expires_on DESC "
        "LIMIT 1 ",
        (os.environ['CORPORATION_ID'], )
    )

    return list(cursor.fetchone())


def all_structures(db_connection):
    cursor = db_connection.cursor()

    cursor.execute(
        "SELECT structure_id "
        "FROM universe_structures "
        "WHERE FailedCount < 6 OR FailedCount IS NULL "
        "ORDER BY updated_at "
    )

    return cursor.fetchall()


def FailStructure(db_connection, structure_id):
    cursor = db_connection.cursor()

    cursor.execute(
        "UPDATE universe_structures "
        "SET FailedCount = COALESCE(FailedCount, 0) + 1 "
        "WHERE structure_id = %s",
        (structure_id, )
    )

    db_connection.commit()


def UpdateStructure(db_connection, structure_id, esi_structure):
    cursor = db_connection.cursor()

    cursor.execute(
        "UPDATE universe_structures "
        "SET name = %s, "
        "owner_id = %s, "
        "solar_system_id = %s, "
        "type_id = %s, "
        "x = %s, "
        "y = %s, "
        "z = %s, "
        "updated_at = UTC_TIMESTAMP(), "
        "FailedCount = null "
        "WHERE structure_id = %s",
        (
            esi_structure["name"],
            esi_structure["owner_id"],
            esi_structure["solar_system_id"],
            esi_structure["type_id"],
            esi_structure["position"]["x"],
            esi_structure["position"]["y"],
            esi_structure["position"]["z"],
        )
    )

    db_connection.commit()
