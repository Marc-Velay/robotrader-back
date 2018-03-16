#! /usr/bin/python

import csv
import requests
from datetime import datetime
from api.models import *

#Server settings
item = "apple"
itemID = 4
csvFile = "../media/gatherer/AAPL.USUSD_Candlestick_1_M_BID_26.01.2017-10.03.2018.csv"
url = "http://10.8.176.101:30000/api/" + item + "/"

def getNextTS():
    r = requests.get(url + "lastEntry/", auth=('user', 'picklerick'))
    try:
        checkTS = r.json()['timestamp'] + 60
    except:
        checkTS = -1
    return checkTS

## From outside but very slow
def insertRowThrowAPI(row):
    global checkTS
    if row[0] == checkTS:   #Check the timestamp
        checkTS += 60
        if checkTS % 864000 == 0:
            print(row[0])
        requests.post(url + "2015/",
                      data = {"item": itemID,
                              "timestamp": row[0],
                              "opening":   row[1],
                              "high":      row[2],
                              "low":       row[3],
                              "closing":   row[4],
                              "volume":    row[5], },
                      auth=('user', 'picklerick'))
    else:
        print("Timestamps don't match : " + str(row[0]) + ", expected : " + str(checkTS))
        quit()

## Very fast but only from inside
def insertRow(row):
    _, created = Candles.objects.get_or_create(
        item = itemID
        timestamp = row[0],
        opening = row[1],
        high = row[2],
        low = row[3],
        closing = row[4],
        volume = row[5],
        )


checkTS = getNextTS()
reader = []
days = 0
print("### Load and parse CSV ###")
with open(csvFile, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar="'")
    reader = list(reader)[1:]
    days = len(reader)//60//24
    for i in range(len(reader)):
        d = datetime.strptime(reader[i][0], '%d.%m.%Y %H:%M:%S.%f')
        reader[i][0] = int(d.timestamp())
        if reader[i][0] % 86400 == 0:
            print(i//60//24, "/", days)
if checkTS == -1:
    checkTS = reader[0][0]
print("### Insert data ###")
for i in range(len(reader)):
    insertRowThrowAPI(reader[i])
print("done")
