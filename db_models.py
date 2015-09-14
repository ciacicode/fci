__author__ = 'ciacicode'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('fci.cfg')
db = SQLAlchemy(app)


class Locations(db.Model):
    """
        Defines the columns and keys for Locations table
    """
    postcode = db.Column(db.String(10), db.ForeignKey('fci_index.postcode'))
    fci_index = db.relationship('FciIndex', backref=db.backref('locations', lazy='dynamic'))
    area = db.Column(db.String(50), primary_key=True)

    def __init__(self, area, postcode):
        self.area = area
        self.postcode = postcode

    def __repr__(self):
        return '%r' % self.area


class FciIndex(db.Model):
    """
        Defines the columns and keys for the Fried Chicken Index Table
    """
    id = db.Column(db.Integer, primary_key=True)
    postcode = db.Column(db.String(10))
    fci = db.Column(db.Float, unique=True)
    date = db.Column(db.DateTime, unique=True)

    def __init__(self, postcode, fci, date=None):
        self.postcode = postcode
        self.fci = fci
        if date is None:
            date = datetime.utcnow()
        self.date = date

    def __repr__(self):
        return 'fci for %r is %f' % (self.postcode, self.fci)