__author__ = 'ciacicode'

from flask import Flask, url_for
from flask import request
from flask import json
from flask import Response
from flask import jsonify
from endpoints import fci
from endpoints import postcodes
from db_models import *

app = Flask(__name__)


@app.route('/')
def api_root():
    """

    :return: in case of no parameters given it returns the entire mapping of the api endpoints. if a postcode is provided in the form of a gest parameter, it will return the value of the resource
    """
    if 'postcode' in request.args:
        resp = fci_object_return(request.args['postcode'])

    else:
        resp = jsonify(fci.fci_api_mapping)
        resp.status_code = 200
        return resp

@app.route('/postcodes')
def api_postcodes():
    """

    :return: all the postcodes where there is a Fried Chicken Index value
    """
    resp = jsonify(postcodes.fci_api_postcodes)
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    app.run(debug=True)