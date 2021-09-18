from os import name
from flask import Flask, render_template, request, redirect, jsonify
import matplotlib.pyplot as plt
import requests
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import ergast
import fasterf1

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False


@app.route('/')
def notdash():
    df = ergast.RequestParams(2020, 7, [1], ['Norris', 'Hamilton'], limit='100').laptimes()
    #df = data.standings(type = 'driverStandings', season = 'all')
    fig = make_subplots() #specs=[[{"secondary_y": True}]]
    fig.add_trace(go.Scatter(y=df['Norris'].str[1], y0=df['Norris'].str[0], x=df['lap'], name='norris'))
    fig.add_trace(go.Scatter(y=df['Hamilton'].str[1], x=df['lap'], name='Hamilton'))
    #fig.update_layout(hoverinfo=customdata)
    #fig = px.line(df, x="season", y="points", hover_data=['driverId'], markers=True)
    #fig.add_bar(x=df['season'], y=df['round'])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("main.html", graphJSON=graphJSON)
    #return fig.show()

@app.route('/fasterf1')
def fastestf1():
    bot_data = fasterf1.get_fastest('BOT', 2021, 'monza', 'Q')
    ham_data = fasterf1.get_fastest('HAM', 2021, 'monza', 'Q')

    fig = make_subplots()
    fig.add_trace(go.Scatter(y=bot_data['Speed'], x=bot_data['Time'], name='Bottas'))
    fig.add_trace(go.Scatter(y=ham_data['Speed'], x=ham_data['Time'], name='Hamilton'))

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("main.html", graphJSON=graphJSON)

@app.route('/12/9/2021')
def old():
    df = ergast.standings(type = 'driverStandings', season = 'all')
    fig = px.line(df, x="season", y="points", hover_data=['driverId'], markers=True)
    fig.add_bar(x=df['season'], y=df['round'])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("main.html", graphJSON=graphJSON)


if __name__ == '__main__':
    app.run()