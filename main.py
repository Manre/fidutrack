from flask import Flask
from flask import request

from cli import execute

app = Flask(__name__)


@app.route("/")
def index():
    return dict(status="invalid", message="Invalid route")


@app.route("/status")
def status():
    return dict(status="success", message="Application is running")


@app.route("/run")
def run():
    execute()
    return dict(status="success", message="Successful execution")


@app.route('/__space/v0/actions', methods=['POST'])
def actions():
    data = request.get_json()
    event = data['event']
    if event['id'] == 'scrape_all':
        execute()
