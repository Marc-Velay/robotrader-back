#! /usr/bin/python

import json
import datetime
import psycopg2

#Load IDs and connect to DB
def connection():
    global conn, cur
    ids = json.load(open("../PRIVATE.json"))
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

#Insert a row in api_gdax table
def insertRow(data, commitNow):
    global conn, cur
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO api_gdax (timestamp, opening, high, low, closing, volume) VALUES (%s, %s, %s, %s, %s, %s);",
                    (data[0], data[1], data[2], data[3], data[4], data[5]))
        if commitNow:
            conn.commit()
    except:
        print("Unable to insert data. Rolling back...")
        conn.rollback()
        close()

def commit():
    global conn, cur
    conn.commit()

#Close all connections to DB
def close():
    global conn, cur
    try:
        cur.close()
    except:
        print("Va te faire mettre")
    conn.close()

#test = [datetime.datetime.fromtimestamp(1422748800), 218.67, 218.7, 218.67, 218.7, 0.02]
#connection()
#cur = conn.cursor()
#insertRow(test)
#cur.execute("SELECT * FROM api_gdax;")
#print(cur.fetchmany(100))
#close()
