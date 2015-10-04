__author__ = 'ciacicode'

from flask import Flask, url_for
from flask import request
from flask import json
from flask import Response
import pdb
from flask import jsonify
from endpoints import fci
from db_models import *
from fciUtils import *

app = Flask(__name__)


@app.route('/')
def api_root():
    return "Welcome"


@app.route('/fci')
def api_fci():
    """
    :return: in case of no parameters given it returns the entire mapping of the api endpoints. if a postcode is provided in the form of a gest parameter, it will return the value of the resource
    """
    all_postcodes = postcodes_return()
    all_postcodes = all_postcodes['postcodes']
    if 'postcode' in request.args:
        # check also if the postcode is among the ones we have data for
        p = post_to_area(request.args['postcode'])
        if p in all_postcodes:
            resp = fci_object_return(request.args['postcode'])
            resp = jsonify(resp)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    else:
        resp = jsonify(fci.fci_api_mapping)
        resp.status_code = 200
        return resp


@app.route('/fci/postcodes')
def api_postcodes():
    """

    :return: all the postcodes where there is a Fried Chicken Index value
    """
    fci_api_postcodes = postcodes_return()
    resp = jsonify(fci_api_postcodes)
    resp.status_code = 200
    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/fci/maximum')
def api_maximum():
    """

    :return: the maximum value of fci in the database
    """
    resp = find_max()
    resp = jsonify(resp)
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    app.run(debug=True)