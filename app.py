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
import data


app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False


@app.route('/')
def notdash():
    df = data.RequestParams([2020], [7], [1], ['Norris', 'Sainz'])
    #df = data.standings(type = 'driverStandings', season = 'all')
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=df[''], y=df['round'], customdata=df['driverId'], name='N.O. of Rounds'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['season'], y=df['points'], name='Points'), secondary_y=True)
    fig.update_layout(hoverinfo=customdata)
    #fig = px.line(df, x="season", y="points", hover_data=['driverId'], markers=True)
    #fig.add_bar(x=df['season'], y=df['round'])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("notdash.html", graphJSON=graphJSON)
    #return fig.show()


@app.route('/12/9/2021')
def old():
    df = data.standings(type = 'driverStandings', season = 'all')
    fig = px.line(df, x="season", y="points", hover_data=['driverId'], markers=True)
    fig.add_bar(x=df['season'], y=df['round'])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("notdash.html", graphJSON=graphJSON)


if __name__ == '__main__':
    app.run()