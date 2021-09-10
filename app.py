from os import name
from flask import Flask, render_template, request, redirect, jsonify
import matplotlib.pyplot as plt
import requests
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import json


app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

@app.route('/')
def notdash():
    df = pd.DataFrame({
      "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
      "Amount": [4, 1, 2, 2, 4, 5],
      "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]})
    fig = px.bar(df, x="Fruit", y="Amount", color="City",    barmode="group")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("notdash.html", graphJSON=graphJSON)


if __name__ == '__main__':
    app.run()