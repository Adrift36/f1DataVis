import requests
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import json

endpoint = 'http://ergast.com/api/f1/'
_json = '.json'

def findkeys(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, kv):
               yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in findkeys(j, kv):
                yield x


#def raceAndResults():

def standings(**params): # TODO for selecting year add 'price slider' add make request only that segment with ?limit and ?offset //type, season, round, driver, constructor
    if params['season'] == 'all':
        response = json.loads(requests.get(endpoint + params['type'] + '/1' + _json + '?limit=10').text)
        print(response)
        return pd.DataFrame({response['points'], response['driverId'], response['season']})


#def lapsAndStops():

print(standings(type = 'driverStandings', season = 'all'))