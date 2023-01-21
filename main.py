import getopt
import os
import sys

import psycopg2
from dotenv import load_dotenv

import core.db_manager as mydb
from core.parser_manager import HtmlParser


def validate_env_values(values: dict) -> dict:
    """
    Checks the required values. Returns empty dict if at least one of the
    required values is None.
    Required values:
        - DB_NAME
        - DB_USER
        - DB_PASSWORD
    """
    required_values = ["DB_NAME", "DB_USER", "DB_PASSWORD"]
    is_valid = True
    err_msg = "{} environment value is required"
    for value_name in required_values:
        if not values.get(value_name):
            print(err_msg.format(value_name))
            is_valid = False
    return values if is_valid else dict()


def get_env_values() -> dict:
    """
    Reads the environment values from the .env file and returns dict. Returns
    an empty dict if the .env file is empty. Returns an empty dict if the
    required values are not defined.
    """
    if not load_dotenv("./.env"):
        print("An environment .env file is required.")
        return dict()
    env_values = {
        "DB_NAME": os.getenv("DB_NAME"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD"),
        "DB_HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "DB_PORT": os.getenv("DB_PORT", "5432"),
    }
    return validate_env_values(env_values)


def read_yes_no() -> bool:
    reading = True
    result = False
    while reading:
        answer = input('Input "Y" to clear the database and continue. '
                       'Input "N" to exit.\n')
        answer = answer.lower()
        if answer in ("y", "n"):
            if answer == "y":
                result = True
            reading = False
    return result


def parse_arg(number: str) -> int:
    """
    Tries to convert a string to int. Returns -1 if value is not number else
    returns number value.
    """
    result = -1
    try:
        result = int(number)
    except ValueError:
        pass
    return result


def main():
    rows = 1
    depth = 0

    # parse command line parameters
    argc = len(sys.argv)
    if argc < 3:
        print("Wrong number of parameters.")
        sys.exit(2)
    action = sys.argv[1]
    if action not in ["load", "get"]:
        print(f'Unknown command "{action}". Use command "load" or "get".')
        sys.exit(2)
    url = sys.argv[2]

    try:
        if argc > 3:
            opts, _ = getopt.getopt(sys.argv[3:], "", ["depth=", "rows="])
            for opt, arg in opts:
                if opt == "--depth":
                    depth = parse_arg(arg)
                    if depth < 0:
                        print("--depth parameter must be a positive number.")
                        sys.exit(2)
                elif opt == "--rows":
                    rows = parse_arg(arg)
                    if rows < 0:
                        print("--rows parameter must be a positive number.")
                        sys.exit(2)
                else:
                    print(f"Unknown parameter {opt}.")
                    sys.exit(2)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    env_values = get_env_values()
    if not env_values:
        print("Not all required environment values are defined in the .env "
              "file.")
        sys.exit(3)

    exit_status = 0
    try:
        connection = mydb.set_connection(
            None,
            dbname=env_values["DB_NAME"],
            user=env_values["DB_USER"],
            password=env_values["DB_PASSWORD"],
            host=env_values["DB_HOST"],
            port=env_values["DB_PORT"]
        )
        mydb.create_table(connection)
        if action == "load":
            url_is_exists = mydb.search_url(connection, url)
            allow_start = True
            if url_is_exists:
                print(f"Url {url} was parsed.")
                allow_start = read_yes_no()
                if allow_start:
                    mydb.clear_table(connection, url)
            elif url_is_exists == -1:
                print("The database connection was closed or terminated.")
                sys.exit(1)
            if not url_is_exists or (url_is_exists and allow_start):
                html_parser = HtmlParser(connection, url, depth)
                html_parser.run_with_profile()

        elif action == "get":
            page_tree = mydb.get_page_tree(connection, url, rows)
            mydb.put_page_tree(page_tree)
    except psycopg2.DatabaseError as db_err:
        print(f"An error occurred while working with the database.\n{db_err}")
        exit_status = 1
        mydb.close_connection(connection)
    sys.exit(exit_status)


if __name__ == "__main__":
    main()
