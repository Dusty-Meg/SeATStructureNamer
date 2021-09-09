import datetime
import time
import os

import requests

import DAL

REFRESH_TOKENS = (
    " CREATE TABLE `refresh_tokens` ( "
    " `character_id` BIGINT(20) NOT NULL, "
    " `version` SMALLINT(5) UNSIGNED NOT NULL DEFAULT '2', "
    " `user_id` INT(11) NOT NULL, "
    " `refresh_token` MEDIUMTEXT NOT NULL COLLATE 'utf8mb4_unicode_ci', "
    " `scopes` LONGTEXT NOT NULL COLLATE 'utf8mb4_bin', "
    " `expires_on` DATETIME NOT NULL, "
    " `token` TEXT NOT NULL COLLATE 'utf8mb4_unicode_ci', "
    " `character_owner_hash` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_unicode_ci', "
    " `created_at` TIMESTAMP NULL DEFAULT NULL, "
    " `updated_at` TIMESTAMP NULL DEFAULT NULL, "
    " `deleted_at` TIMESTAMP NULL DEFAULT NULL, "
    " PRIMARY KEY (`character_id`) USING BTREE "
    " ) "
)

CHARACTER_AFFILIATIONS = (
    " CREATE TABLE `character_affiliations` ( "
    " `character_id` BIGINT(20) NOT NULL, "
    " `corporation_id` BIGINT(20) NOT NULL, "
    " `alliance_id` BIGINT(20) NULL DEFAULT NULL, "
    " `faction_id` BIGINT(20) NULL DEFAULT NULL, "
    " `created_at` TIMESTAMP NULL DEFAULT NULL, "
    " `updated_at` TIMESTAMP NULL DEFAULT NULL, "
    " PRIMARY KEY (`character_id`) USING BTREE "
    " ) "
)


def test_character_tokens(mysql, mocker):
    cur = mysql.cursor()
    cur.execute(REFRESH_TOKENS)
    cur.execute(CHARACTER_AFFILIATIONS)
    cur.execute(
        " INSERT INTO `refresh_tokens` VALUES "
        " ('22', '2', '1', 'ssd', 'scopes', '2021-08-23 08:57:32', 'sss', '33333', NULL, NULL, NULL); "
    )
    cur.execute(
        " INSERT INTO `character_affiliations` VALUES "
        " (22, 3, NULL, NULL, NULL, '2021-08-23 08:57:32'); "
    )
    cur.close()

    result = DAL.character_token(mysql, None)

    assert(result['token'] == '22')
