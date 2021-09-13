import requests
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import json

endpoint = 'http://ergast.com/api/f1/'
_json = '.json'

def getNestedJSON(node, kv): #function for extracting values of keys from nestes json
    if isinstance(node, list):
        for i in node:
            for x in getNestedJSON(i, kv):
                try:                # trying to return value as an integer 
                   yield int(x)
                except ValueError:
                    yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in getNestedJSON(j, kv):
                try:                # trying to return value as an integer
                   yield int(x)
                except ValueError:
                    yield x

#def raceAndResults():

def standings(**params): # TODO for selecting year add 'price slider' add make request only that segment with ?limit and ?offset //type, season, round, driver, constructor
    if params['season'] == 'all':
        response = json.loads(requests.get(endpoint + params['type'] + '/1' + _json + '?limit=1000').text)
        keys = ['points', 'driverId', 'season', 'round']
        return pd.DataFrame({key: list(getNestedJSON(response, key)) for key in keys})
        #return list(getNestedJSON(response, 'points'))

#def lapsAndStops():

#print(standings(type = 'driverStandings', season = 'all'))

df = pd.DataFrame({
      "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
      "Amount": [4, 1, 2, 2, 4, 5],
      "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]})

#print(standings(type = 'driverStandings', season = 'all'))