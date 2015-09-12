__author__ = 'ciacicode'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('fci.cfg')
db = SQLAlchemy(app)


class FciSources(db.Model):
    """
        Database Model of the Sources table containing
        all necessary URLs to calculate to Fried Chicken Index
    """
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(80), db.ForeignKey('postcodes.area'))
    last_modified = db.Column(db.String(60), unique=True)
    postcodes = db.relationship('Postcodes', backref=db.backref('fcisources', lazy='dynamic'))
    url = db.Column(db.String(255), unique=True)

    def __init__(self, area, last_modified, url):
        self.area = area
        self.last_modified = last_modified
        self.url = url

    def __repr__(self):
        return '<Source for %r>' % self.area


class Postcodes(db.Model):
    """
        Database Model of the Postcodes and Areas of
        London that will be used to associate area to fci index
    """
    postcode = db.Column(db.String(20), db.ForeignKey('fciindex.postcode'))
    fciindex = db.relationship('FcIIndex', backref=db.backref('postcodes', lazy='dynamic'))
    area = db.Column(db.String(80), primary_key=True)

    def __init__(self, area, postcode):
        self.area = area
        self.postcode = postcode

    def __repr__(self):
        return '<Postcode %r>' % self.postcode


class FciIndex(db.Model):
    """
        Database Model of the fried chicken index and the
        related area postcode
    """
    postcode = db.Column(db.String(20), primary_key=True)
    fci = db.Column(db.Float, unique=True)
    date = db.Column(db.DateTime, unique=True)

    def __init__(self, postcode, fci, date):
        self.postcode = postcode
        self.fci = fci
        self.date = date

    def __repr__(self):
        return '<Fci for %r>' % self.postcode + 'is %r' % self.fci
