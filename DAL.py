import os
import sys

import mariadb


def db_connect(logging):
    try:
        return mariadb.connect(
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=int(os.environ['DB_PORT']),
            database=os.environ['DB_DATABASE']
            )
    except mariadb.Error as e:
        logging.error(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)


def character_token(db_connection, character_id, logging):
    with db_connection.cursor(dictionary=True, buffered=False) as cursor:
        sql = (" SELECT refresh_tokens.token, refresh_tokens.expires_on, refresh_tokens.character_id "
               " FROM refresh_tokens "
               " LEFT JOIN character_affiliations ON refresh_tokens.character_id = character_affiliations.character_id "
               " WHERE refresh_tokens.deleted_at IS NULL "
               " AND TIMESTAMPDIFF(MINUTE, refresh_tokens.expires_on, UTC_TIMESTAMP()) BETWEEN -20 AND -3 "
               " AND character_affiliations.corporation_id = %s ")
        data = (os.environ['CORPORATION_ID'], )

        if character_id is not None:
            sql = (f" {sql} "
                   " AND refresh_tokens.character_id != %s ")
            data += (character_id, )

        sql = (f" {sql} "
               " ORDER BY character_affiliations.updated_at DESC, refresh_tokens.expires_on DESC "
               " LIMIT 1 ")

        cursor.execute(sql, data)

        results = cursor.fetchone()
        logging.error(results)
        logging.error(cursor.statement)

    return results


def all_structures(db_connection):
    with db_connection.cursor(dictionary=True, buffered=False) as cursor:
        cursor.execute(
            " SELECT structure_id "
            " FROM universe_structures "
            " WHERE (FailedCount < 6 OR FailedCount IS NULL) "
            " AND TIMESTAMPDIFF(HOUR, updated_at, UTC_TIMESTAMP()) > 24 "
            " ORDER BY updated_at "
        )

        return cursor.fetchall()


def FailStructure(db_connection, structure_id):
    with db_connection.cursor(dictionary=True, buffered=False) as cursor:
        cursor.execute(
            "UPDATE universe_structures "
            "SET FailedCount = COALESCE(FailedCount, 0) + 1 "
            "WHERE structure_id = %s",
            (structure_id, )
        )

        db_connection.commit()


def UpdateStructure(db_connection, structure_id, esi_structure):
    with db_connection.cursor(dictionary=True, buffered=False) as cursor:
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
            "FailedCount = 0 "
            "WHERE structure_id = %s",
            (
                esi_structure["name"],
                esi_structure["owner_id"],
                esi_structure["solar_system_id"],
                esi_structure["type_id"],
                esi_structure["position"]["x"],
                esi_structure["position"]["y"],
                esi_structure["position"]["z"],
                structure_id
            )
        )

        db_connection.commit()
