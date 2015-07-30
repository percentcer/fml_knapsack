from flask import Flask
from flask import json
from flask import render_template
from fml_knapsack import lookup

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', lookup=lookup)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15745, debug=True)
