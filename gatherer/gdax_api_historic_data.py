#! /usr/bin/python

import requests
import json
import time
import datetime
import dateutil.parser as dp

#Server URL
url_gdax = "https://api.gdax.com/products/BTC-USD/candles?"
url = "http://86.64.78.32:30000/api/gdax/"

#End timestamp
end = 1519858800

#Granularity and request interval
gran = 60   #1 / minute
interval = 240  #240 minutes

def getNextTS():
    global checkTS
    r = requests.get(url + "lastEntry/", auth=('user', 'picklerick'))
    checkTS = r.json()['timestamp'] + 60
    return checkTS

def insertRow(row):
    global checkTS
    if row[0] == checkTS:   #Check the timestamp
        checkTS += 60
        if checkTS % 86400 == 0:
            print(row[0])
        requests.post(url + "2015/",
                      data = {"item": 2,
                              "timestamp": row[0],
                              "opening":   row[1],
                              "high":      row[2],
                              "low":       row[3],
                              "closing":   row[4],
                              "volume":    round(row[5], 2)},
                      auth=('user', 'picklerick'))
    else:
        print("timestamps don't match : " + str(row[0]) + ", expected : " + str(checkTS))
        quit()

#Get next time interval (we can't fetch all data in one request)
def getNextTimestamp(time1):
    gap = end - time1
    if gap >= interval*gran:
        time1 += interval*gran
    else:
        time1 = end
    return time1

#Check if there are no missing value (a missing value appears when nobody trade on gdax on a given minute)
def handleGap(lastTs, ts, lastC):
    if lastC == -1:
        return
    timestamp = lastTs + gran
    while timestamp < ts:
        insertRow([timestamp, lastC, lastC, lastC, lastC, 0])
        #print(str(timestamp) + "  | " + str(lastC) + "  | " + str(lastC) + "  | " + str(lastC) + "  | " + str(lastC) + "  | " + "0")
        timestamp += gran

checkTS = getNextTS()
t1 = checkTS
lastTimestamp = t1
lastClosing = -1
while True:
    if t1 == end:
        break
    t2 = getNextTimestamp(t1)
    
    request = url_gdax + "start=" + (datetime.datetime.fromtimestamp(t1) + datetime.timedelta(hours=-2)).isoformat() +\
                         "&end=" + (datetime.datetime.fromtimestamp(t2) + datetime.timedelta(hours=-2)).isoformat() +\
                         "&granularity=" + str(gran)
    #print(request)
    try:
        res = requests.get(request)
        data = res.json()
    except:
        print("Canno't parse into json...")
        print(res)
        continue
    #print("start : "+t1+"\nend   : "+t2)
    if 'message' in data:   #It often means that we send too much request to gdax api
        print(data)
        #print("start : "+t1+"\nend   : "+t2)
        time.sleep(5)
        continue
    for i in range(len(data)-1, -1, -1):
        if data[i][0] - lastTimestamp > gran:
            handleGap(lastTimestamp, data[i][0], lastClosing)
        lastTimestamp = data[i][0]
        lastClosing = data[i][4]
        insertRow(data[i])
        #print(str(data[i][0]) + "  | " + str(data[i][1]) + "  | " + str(data[i][2]) + "  | " + str(data[i][3]) + "  | " + str(data[i][4]) + "  | " + "{0:.2f}".format(data[i][5]))
    t1 = t2
    time.sleep(0.3)
