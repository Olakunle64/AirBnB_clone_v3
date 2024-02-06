#!/usr/bin/python3
"""
This module provides utility functions for processing data.

This module contains various functions for processing and manipulating
data, including functions for sorting, filtering, and transforming data.

Functions:
- sort_data(data): Sorts a list of data elements in ascending order.
- filter_data(data, threshold): Filters data elements based on a threshold value.

Examples:
    # Sort a list of numbers
    sorted_numbers = sort_data([3, 1, 4, 1, 5, 9, 2])

    # Filter a list of numbers based on a threshold
    filtered_numbers = filter_data([10, 20, 30, 40, 50], 30)
"""

from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.register_blueprint(app_views)


@app.teardown_appcontext
def closing(exception):
    """tear down method"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Not found method"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    hostname = os.getenv('HBNB_API_HOST')
    portnum = os.getenv('HBNB_API_PORT')
    if not hostname:
        hostname = '0.0.0.0'
    if not portnum:
        portnum = 5000
    app.run(host=hostname, port=portnum, threaded=True)
