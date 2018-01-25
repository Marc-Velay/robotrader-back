#! /usr/bin/python

import requests
import json
import time
import datetime
import dateutil.parser as dp

#Server URL
url = "https://api.gdax.com/products/BTC-USD/candles?"

#Interesting period
start = "2015-02-01T00:00:00"
end = "2018-01-15T00:00:00"

#Granularity and request interval
gran = 60   #1 / minute
interval = 240  #240 mins

#Get next time interval (we can't fetch all data in one request)
def getNextTimestamp(time1):
    timestamp = int(dp.parse(time1).strftime('%s'))
    gap = int(dp.parse(end).strftime('%s')) - timestamp
    if gap >= interval*gran:
        timestamp += interval*gran
    else:
        timestamp = int(dp.parse(end).strftime('%s'))
    return datetime.datetime.fromtimestamp(timestamp).isoformat()

#Check if there are no missing value (a missing value appears when nobody trade on gdax on a given minute)
def handleGap(lastTs, ts, lastC):
    if lastC == -1:
        return
    timestamp = lastTs + gran
    while timestamp < ts:
        t = datetime.datetime.fromtimestamp(timestamp).isoformat()
        #print(t + "  | " + str(lastC) + "  | " + str(lastC) + "  | " + str(lastC) + "  | " + str(lastC) + "  | " + "0")
        timestamp += gran


print(" Time  | Opening  |   High   |   Low    | Closing  | Volume")
t1 = start
lastTimestamp = int(dp.parse(t1).strftime('%s'))
lastClosing = -1
while True:
    if t1 == end:
        break
    t2 = getNextTimestamp(t1)
    request = url + "start=" + t1 + "&end=" + t2 + "&granularity=" + str(gran)
    data = requests.get(request).json()
    #print("start : "+t1+"\nend   : "+t2)
    print(t1)
    if 'message' in data:   #It often means that we send too much request to gdax api
        #print(data)
        #print("start : "+t1+"\nend   : "+t2)
        time.sleep(5)
        continue
    #print(len(data))
    for i in range(len(data)-1, -1, -1):
        if data[i][0] - lastTimestamp > gran:
            handleGap(lastTimestamp, data[i][0], lastClosing)
        lastTimestamp = data[i][0]
        lastClosing = data[i][4]
        t = datetime.datetime.fromtimestamp(data[i][0]).isoformat()
        #print(t + "  | " + str(data[i][1]) + "  | " + str(data[i][2]) + "  | " + str(data[i][3]) + "  | " + str(data[i][4]) + "  | " + "{0:.2f}".format(data[i][5]))
    t1 = t2
    time.sleep(0.3)
