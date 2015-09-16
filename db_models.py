__author__ = 'ciacicode'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import fciUtils
import pdb

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
    postcode = db.Column(db.String(10), index=True)
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


class FciSources(db.Model):
    """
        Defines the columns and keys for the Sources table
    """
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(50))
    last_modified = db.Column(db.DateTime)
    url = db.Column(db.String(255))

    def __init__(self, area, url, last_modified=None):
        self.area = area
        self.url = url
        if last_modified is None:
            last_modified = datetime.utcnow()
        self.last_modified = last_modified

    def __repr__(self):
        return 'Source for %r was last modified on %r' % (self.area, self.last_modified)


def update_sources():
    """
        performs database update
    """
    # json data
    json = 'http://data.gov.uk/api/2/rest/package/uk-food-hygiene-rating-data'
    all_areas_data = fciUtils.resources_list(json)
    # drop fcisources table
    db.drop_all()
    db.create_all()
    for s in all_areas_data:
        db.session.add(s)
    db.session.commit()

