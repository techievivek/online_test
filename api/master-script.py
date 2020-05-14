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
    data=[] # to store the each row entry
    conn.row_factory = sqlite3.Row #https://docs.python.org/2/library/sqlite3.html#sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM workshop_app_proposeworkshopdate")
    rows = cur.fetchall()
    for row in rows:
        dict={}
        for member in row.keys():
            cur2=conn.cursor() #second cursor to read from another model.
            #if it is a relation to other model.
            if member=='proposed_workshop_coordinator_id':
                cur2.execute('select * from auth_user where id=?',(row[member],))
                x=cur2.fetchone()
                dict['proposed_workshop_coordinator_username'] =x['username']
            elif member=='proposed_workshop_instructor_id':
                cur2.execute('select * from auth_user where id=?',(row[member],))
                x=cur2.fetchone()
                dict['proposed_workshop_instructor_username'] =x['username']
            elif member=='proposed_workshop_title_id':
                cur2.execute('select * from workshop_app_workshoptype where id=?',(row[member],))
                x=cur2.fetchone()
                #extra fields I have added for more info on workshop.
                dict["proposed_workshop_name"] =x['workshoptype_name']
                dict["proposed_workshoptype_description"]=x["workshoptype_description"]
                dict["proposed_workshop_duration"] =x['workshoptype_duration']
            else:
                dict[member]=row[member]
        data.append(dict)
    ''' for row in data:
     for key,value in row.items():
      print(" "+key.capitalize()+": "+str(value))
     print("")'''
    # print(json.dumps(data)) #for json data, will add more from here.
    url=r'http://localhost:8000/api/course/create/'
    try:
        with open('demo-data.json') as f:
            json_data=json.load(f)
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

