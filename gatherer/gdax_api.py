#! /usr/bin/python

##{'last_size': '0.00325643',
## 'time': '2018-01-18T22:35:49.954000Z',
## 'low_24h': '11346.02000000',
## 'best_ask': '11346.02',
## 'open_24h': '11337.01000000',
## 'side': 'buy',
## 'price': '11346.02000000',
## 'high_24h': '12123.10000000',
## 'product_id': 'BTC-USD',
## 'trade_id': 34042311,
## 'volume_24h': '32474.08162829',
## 'best_bid': '11346.01',
## 'type': 'ticker',
## 'volume_30d': '815048.9627287',
## 'sequence': 4895742045}

import asyncio
import websockets
import json

oldMinute = ""
opening = -1
closing = -1
volume = 0
price_list = []

async def gdax_websocket():
    async with websockets.connect('wss://ws-feed.gdax.com') as websocket:
        #name = '{"type": "subscribe","product_ids": ["ETH-EUR"],"channels": ["ticker",{"name": "ticker","product_ids": ["ETH-EUR"]}]}'
        subsribe = '{"type":"subscribe","channels":[{"name":"ticker","product_ids":["BTC-EUR"]}]}'
        await websocket.send(subsribe)
        print("> {}".format(subsribe))
        #print("< {}".format(greeting))
        #await websocket.send(name2)
        #print("> {}".format(name2))
        while json.loads(await websocket.recv())["type"] != "subscriptions":
            continue
        print(" Min  | Opening  |   High   |   Low    | Closing  | Volume")
        while True:
            message = await websocket.recv()
            gdax_handling(json.loads(message))

def gdax_handling(data):
    global oldMinute, opening, closing, volume, price_list
    #print(str(data))
    minute = getMinute(data["time"])
    price = float(data["price"])
    last_size = float(data["last_size"])
    if oldMinute == "":
        oldMinute = minute
    if minute == oldMinute:
        volume += last_size
        price_list.append(price)
    else:
        high = -1
        low = -1
        if len(price_list) != 0:
            closing = price_list[-1]
            high = max(price_list)
            low = min(price_list)
            if opening == -1:
                opening = price_list[0]
        print("  " + oldMinute + "  | " + "{0:.2f}".format(opening) + " | " + "{0:.2f}".format(high) + " | " + "{0:.2f}".format(low) + " | " + "{0:.2f}".format(closing) + " | " + "{0:.2f}".format(volume))
        oldMinute = minute
        opening = price
        volume = last_size
        price_list = []

def getMinute(timestamp):
    return timestamp.split(':')[1]

asyncio.get_event_loop().run_until_complete(gdax_websocket())
