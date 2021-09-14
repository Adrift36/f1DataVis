import requests
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import json
import datetime

## TODO store round: circuit dictionary in frontend for each year

_json = '.json'

def getNestedJSON(node, kv): #function for extracting values of keys from nestes json (response, key)
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


def getResponse(*params, limit='20', offset='0'):
    endpoint = 'http://ergast.com/api/f1'
    for param in params:
        endpoint += ('/' + str(param))
    endpoint += ('.json?' + 'limit=' + limit + '&offset=' + offset)
    response = json.loads(requests.get(endpoint).text)
    return response

class RequestParams:
    def __init__(self, season, round, positions, drivers, limit='20', offset='0'):
        #self.resultsType = resultsType
        self.season = season
        self.round = round
        self.positions = positions
        self.drivers = drivers
        self.limit = limit
        self.offset = offset
        '''keys = {
            seasons: 'season',
            rounds: 'round',
            positions: 'position',
            drivers: 'driverId'
        }'''
    
    #def laptimes(self, seasons, rounds, drivers, limit='100', offset='0'):
    def laptimes(self):
        totalLaps = list(getNestedJSON(getResponse(self.season, self.round, 'results', '1'), 'laps'))[0]
        df = pd.DataFrame({'lap': list(range(1, int(totalLaps) + 1))})
        for driver in self.drivers:
            response = getResponse(self.season, self.round, 'drivers/' + driver, 'laps', limit=self.limit, offset=self.offset)
            times = []
            timeLabels = list(getNestedJSON(response, 'time'))[1:]
            for time in timeLabels:
                split = time.replace('.', ':').split(':')
                times.append(datetime.timedelta(minutes=int(split[0]), seconds=int(split[1]), milliseconds=int(split[2])).total_seconds())
            #times = [time.replace('.', ':').split(':') for time in list(getNestedJSON(response, 'time'))[1:]]
            extracted = pd.DataFrame({driver: list(zip(timeLabels, times))})
            df = pd.concat([df, extracted], axis=1)
            #print(extracted)
            #df.append(pd.DataFrame({driver: list(getNestedJSON(response, 'time'))[1:]}))
        #df = pd.DataFrame({driver: list(getNestedJSON(getResponse(self.season, self.round, 'drivers/' + driver, 'laps', limit=self.limit, offset=self.offset), 'time')) for driver in self.drivers})
        return df

    #def standings(self, season, round, *participant):


#def raceAndResults():

#def standings(**params): # TODO for selecting year add 'price slider' add make request only that segment with ?limit and ?offset //type, season, round, driver, constructor
    #if params['season'] == 'all':
        #response = json.loads(requests.get(endpoint + params['type'] + '/1' + _json + '?limit=1000').text)
        #keys = ['points', 'driverId', 'season', 'round']
        #return pd.DataFrame({key: list(getNestedJSON(response, key)) for key in keys})
        #return list(getNestedJSON(response, 'points'))

#def lapsAndStops():

#print(standings(type = 'driverStandings', season = 'all'))

#df = pd.DataFrame({
      #"Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
      #"Amount": [4, 1, 2, 2, 4, 5],
      #"City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]})

#print(standings(type = 'driverStandings', season = 'all'))

df = RequestParams(2020, 7, [1], ['norris', 'leclerc'], limit='100')
print(df.laptimes()['norris'].str[1])