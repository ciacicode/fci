__author__ = 'ciacicode'

from flask import Flask, url_for
from flask import request
from flask import json
from flask import Response
from flask import jsonify
from endpoints import fci

app = Flask(__name__)


@app.route('/')
def api_root():
    """

    :return: all the endpoints necessary to know how to use the Fried Chicken Index API
    """
    resp = jsonify(fci.fci_api_mapping)
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    app.run(debug=True)