from flask import Flask
from flask import json
from flask import render_template
from fml_knapsack import lookup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', lookup=lookup)
