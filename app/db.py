import hashlib
import os

import psycopg2

from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# USER= os.getenv('DB_USER')
# NAME= os.getenv('DB_NAME')
# HOST= os.getenv('DB_HOST')
# PASSWORD = os.getenv('DB_PASSWORD')

# CREDENTIALS = f"dbname={NAME} user={USER} host={HOST} password={PASSWORD}"


def save_to_db(data):
    """
    Save items to the database

    :Param data: tuple of (header, url, body)
    """
    with psycopg2.connect(DATABASE_URL) as con:
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()

        header, url, body = data
        for item in body:
            cursor.execute("INSERT INTO email (header, url, body, hashed_body) \
                VALUES (%s, %s, %s, %s);", (header, url, str(item),
                                            _hash_text(str(item))))


def query_db(pk):
    """
    Query database

    :Param pk: Primary key of item to be queried for
    :Return: tuple of (header, url, body)
    """
    with psycopg2.connect(DATABASE_URL) as con:
        cursor = con.cursor()
        cursor.execute("SELECT header, url, body FROM email WHERE id = %s;",
        (pk,))

        return cursor.fetchone()


def _create_table():
    """ Create table """
    with psycopg2.connect(DATABASE_URL) as con:
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        cursor.execute(
            "CREATE TABLE email (id serial PRIMARY KEY, header varchar, \
                url varchar, body text, hashed_body varchar unique);"
        )


def _hash_text(text):
    """ Create digest """
    return hashlib.sha256(text.encode()).hexdigest()

if __name__ == "__main__":
    _create_table()
