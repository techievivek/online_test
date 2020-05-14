#! /usr/bin/env python3
import sqlite3
from sqlite3 import Error
import json
import requests
from requests.exceptions import HTTPError
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_all_data(conn):
    url=r'http://localhost:8000/api/course/create/'
    try:
        # read the demo json file
        with open('demo-data.json') as f:
            json_data=json.load(f)
        #create a post request to the api end-point.
        response=requests.post("http://localhost:8000/api/course/create/",json=json_data)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Request Success!') #The request was successful.
        print(response.text)
def main():
    database = "db.sqlite3"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        select_all_data(conn)


if __name__ == '__main__':
    main()

