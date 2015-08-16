from flask import Flask
from flask import json
from flask import render_template
from retrieval import projections_table
import datetime

app = Flask(__name__)

lookup = None
last_lookup = None

@app.route('/')
def index():
    global lookup, last_lookup
    if last_lookup is None or datetime.date.today() - last_lookup >= datetime.timedelta(1):
        last_lookup = datetime.date.today()
        lookup = projections_table()
    return render_template('index.html', lookup=lookup)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15745, debug=True)
