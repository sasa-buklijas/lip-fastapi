from flask import Flask
import time

app = Flask(__name__)

@app.route("/bhi/<int:wait_time>")
def blocking_greet(wait_time):
    time.sleep(wait_time)
    return f"blocking Hello? World? after {wait_time} seconds"

# in Flask blocking can be demonstrated, if gunicorn is run with only 1 worker
# eg. gunicorn -w 1 -b 0.0.0.0:8000 002_why_async_in_flask:app

# if you run it with gunicorn -w 2, two workers than it can handel 2 connections
