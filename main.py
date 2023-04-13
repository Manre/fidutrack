import flask
from flask import Flask
from flask import request

from cli import execute

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "OK"


@app.route("/status")
def status():
    return "OK"


@app.route("/run")
def run():
    execute()
    return "OK"


# using flask
@app.route('/__space/v0/actions', methods=['POST'])
def actions():
    data = request.get_json()
    event = data['event']
    if event['id'] == 'cleanup':
        execute()
