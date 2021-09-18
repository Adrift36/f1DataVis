from os import name
from flask import Flask, render_template, request, redirect, jsonify
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import shape
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

#def getAndPlot(drivers, year, circuit, session)

def plot_lap(drivers, year, circuit, session):
    fig = make_subplots()
    for driver in drivers:
        driver_data = fasterf1.get_fastest(driver, year, circuit, session)
        fig.add_trace(go.Scatter(y=driver_data['Speed'], x=driver_data['Time'], name=driver))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/')
def main():
    return render_template('landing.html')

@app.route('/ergast', methods=['GET', 'POST'])
def ergast_():
    df = ergast.RequestParams(2020, 7, [1], ['Norris', 'Hamilton'], limit='100').laptimes()
    #df = data.standings(type = 'driverStandings', season = 'all')
    fig = make_subplots() #specs=[[{"secondary_y": True}]]
    fig.add_trace(go.Scatter(y=df['Norris'].str[1], y0=df['Norris'].str[0], x=df['lap'], name='norris'))
    fig.add_trace(go.Scatter(y=df['Hamilton'].str[1], x=df['lap'], name='Hamilton'))
    #fig.update_layout(hoverinfo=customdata)
    #fig = px.line(df, x="season", y="points", hover_data=['driverId'], markers=True)
    #fig.add_bar(x=df['season'], y=df['round'])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("plotly.html", graphJSON=graphJSON)
    #return fig.show()

@app.route('/fastf1', methods=['GET', 'POST'])
def fastf1_():
    if request.method == 'POST':
        year = request.form['year']
        circuit = request.form['circuit']
        drivers = request.form.getlist('drivers')
        print(drivers)
        graphJSON = plot_lap(drivers, int(year), circuit, 'Q')
        return render_template("plotly.html", graphJSON=graphJSON)
    else:
        return render_template('plotly.html')

@app.route('/12/9/2021')
def old():
    df = ergast.standings(type = 'driverStandings', season = 'all')
    fig = px.line(df, x="season", y="points", hover_data=['driverId'], markers=True)
    fig.add_bar(x=df['season'], y=df['round'])
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("plotly.html", graphJSON=graphJSON)


if __name__ == '__main__':
    app.run()