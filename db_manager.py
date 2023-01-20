"""
Provides functions for working with the database. Most of the defined
functions do not handle psycopg2 errors.
"""

import psycopg2
from psycopg2 import sql


def is_opened(connection=None):
    return connection and connection.closed == 0


def set_connection(connection, dbname: str, user: str, password: str,
                   host: str, port: str):
    """Opens connection if it is closed"""
    if is_opened(connection):
        return connection
    connection = psycopg2.connect(dbname=dbname, user=user, password=password,
                                  host=host, port=port)
    return connection


def close_connection(connection):
    """Tries to close the connection if it exists"""
    if connection:
        try:
            connection.close()
        except psycopg2.DatabaseError as error:
            print(f"Failed to close a database connection.\n{error}")


def create_table(connection):
    """
    Creates a table in the database if it doesn't exist. Returns -1 if the
    connection is closed, otherwise returns 0.
    """
    if not is_opened(connection):
        return -1

    create_sql = """
        CREATE TABLE IF NOT EXISTS page_content (
            id SERIAL PRIMARY KEY,
            parent_id INT NULL,
            content TEXT,
            title VARCHAR(200) NULL,
            url VARCHAR(2048),
            CONSTRAINT FK_parent_page_content
            FOREIGN KEY (parent_id)
            REFERENCES page_content (id) ON DELETE CASCADE
        );
    """
    with connection.cursor() as cursor:
        cursor.execute(create_sql)
    connection.commit()
    return 0


def insert_to_db(connection, values: list) -> int:
    """
    Writes data to a table. Returns a new row ID. Do not handle psycopg
    errors and don't check database connection.
    Values list must be have a structure:
        [
            (
                id of a parent row from a database table (type of int),
                html text (type of str),
                title of the web page (type of str),
                url of the web page (type of str)
            ),
            ...
        ]
    """
    with connection.cursor() as cursor:
        sql_string = """
            INSERT INTO page_content (parent_id, content, title, url)
            VALUES {} RETURNING id
        """
        insert = sql.SQL(sql_string).format(
            sql.SQL(",").join(map(sql.Literal, values))
        )
        cursor.execute(insert)
        content_id = cursor.fetchone()[0]
    connection.commit()
    return content_id


RECURSIVE_SQL = """
    WITH RECURSIVE page_tree (id, level, url, title) AS
        (SELECT
            id,
            0,
            url,
            title
        FROM page_content
        WHERE parent_id IS NULL AND url LIKE %s ESCAPE ''
        UNION ALL
        SELECT
            p.id,
            pt.level + 1,
            p.url,
            p.title
        FROM page_content p, page_tree pt
        WHERE p.parent_id = pt.id )
    SELECT * FROM page_tree
    ORDER BY level LIMIT %s
"""


def get_page_tree(connection, url: str, row_numbers: int = 1):
    """
    Recursively selects row_numbers rows for the given url from the database.
    Returns -1 if the connection is closed, otherwise returns a list of rows.
    """
    if not is_opened(connection):
        return -1
    with connection.cursor() as cursor:
        cursor.execute(RECURSIVE_SQL, (url, row_numbers))
        results = cursor.fetchall()
    return results


def search_url(connection, url: str):
    """
    Looks up a given url in the database. Returns -1 if the connection is
    closed, otherwise returns a list of rows.
    """
    if not is_opened(connection):
        return -1
    row_id = 0
    with connection.cursor() as cursor:
        sql_string = "SELECT id FROM page_content WHERE parent_id IS NULL " \
                     "AND url LIKE %s ESCAPE ''"
        cursor.execute(sql_string, (url, ))
        results = cursor.fetchone()
        row_id = results[0] if results else row_id
    return row_id


def clear_table(connection, url: str):
    """
    Removes a row with an url column value like a url parameter. Returns -1 if
    the connection is closed, otherwise returns 0.
    """
    if not is_opened(connection):
        return -1
    with connection.cursor() as cursor:
        sql_string = "DELETE FROM page_content WHERE parent_id IS NULL " \
                     "AND url LIKE %s ESCAPE ''"
        cursor.execute(sql_string, (url, ))
    return 0


def put_page_tree(page_tree: list):
    """Print page_tree on console"""
    for node in page_tree:
        print(f"Depth: {node[1]}: {node[2]}: {node[3]}")
