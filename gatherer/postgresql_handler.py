#! /usr/bin/python

import json
import psycopg2

#Load IDs and connect to DB
def connection():
    ids = json.load(open("PRIVATE.json"))
    try:
        conn = psycopg2.connect( "dbname="+ids['dbname']+
                                " user="+ids['user']+
                                " host="+ids['host']+
                                " port="+ids['port']+
                                " password="+ids['passwd'])
        return conn
    except:
        print("Unable to connect to the database")
        exit()


conn = connection()
cur = conn.cursor()
cur.execute("SELECT * FROM api_forex;")
print(cur.fetchmany(100))
cur.close()
conn.close()
