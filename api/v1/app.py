#!/usr/bin/python3
'''create a variable app, instance of Flask'''
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(error):
    '''close session'''
    storage.close()

if __name__ == "__main__":
    API_HOST = os.getenv('HBNB_API_HOST')
    API_PORT = os.getenv('HBNB_API_PORT')

    host = '0.0.0.0' if not API_HOST else API_HOST
    port = 5000 if not API_PORT else API_PORT
    app.run(host=host, port=port, threaded=True)
