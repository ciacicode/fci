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
    id = db.Column(db.Integer, primary_key=True)
    postcode = db.Column(db.String(10))
    #fci_index = db.relationship('FciIndex', backref=db.backref('locations', lazy='dynamic'))
    area = db.Column(db.String(50))

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
    fci = db.Column(db.Float)
    date = db.Column(db.DateTime)

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


# Functions to update or search databases

def update_sources():
    """
        performs database update of the FciSources table
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


def update_locations():
    """
    performs database update of the Locations Table
    """
    # execute select query

    results = db.session.query(FciSources.area, FciSources.url)
    results = results.all()

    for area, url in results:
        # pass the url to an xmlparser function
        temp_dict = fciUtils.postcodes_dict(url, area)
        value_list = temp_dict.values()
        iterable = value_list[0]
        # parse the dict and write into database
        for value in iterable:
            if value == "":
                break
            else:
                # create instance of location
                location = Locations(area, value)
                # execute insert query
                db.session.add(location)
                # commit query
    db.session.commit()


def update_fci():
    '''
        updates the fciindex table
    '''
    results = db.session.query(Locations.postcode)
    results = results.all()
    postcodes = sorted(set(results))
    maximum = 0.0
    fci_dict = dict()
    for p in postcodes:
        p = str(p[0])
        fci = fciUtils.fci_calculate(p)
        fci_dict[p] = fci
        if fci > maximum:
            maximum = fci

    # time to write in the table
    for key, value in fci_dict.iteritems():
        fci = (value/maximum)*100
        record = FciIndex(key, fci)
        db.session.add(record)
    db.session.commit()


def find_xml(postcode):
    """
       input a postcode returns dict of
       xml URL of area(s)
    """
    p_postcode = fciUtils.post_to_area(postcode)
    location = Locations.query.filter_by(postcode= p_postcode).first()
    area = location.area
    source = FciSources.query.filter_by(area=area).first()
    url_xml = source.url
    return url_xml


def fci_return(postcode):
    """
        receives postcode
        returns formatted fci
    """
    # normalise input
    postcode = fciUtils.post_to_area(postcode)
    fci = FciIndex.query.filter_by(postcode=postcode).first()
    if fci.fci is None:
        return 'There is no FCI for this area'
    else:
        return "{0:.2f}".format(fci.fci)


def fci_object_return(postcode):
    """

    :param postcode:
    :return: the entire fci object
    """
    fci_object = dict()
    postcode = fciUtils.post_to_area(postcode)
    query_object = FciIndex.query.filter_by(postcode=postcode).first()
    fci_object['postcode'] = query_object.postcode
    fci_object['fci'] = query_object.fci
    fci_date = query_object.date
    fci_object['last_updated'] = fci_date.strftime("%Y-%m-%d")
    return fci_object


def postcodes_return():
    """
    :return: all postcodes for which we have an fci value
    """
    postcodes = db.session.query(FciIndex.postcode)
    all_postcodes = postcodes.all()
    postcode_list = list()
    for postcode in all_postcodes:
        postcode_list.append(postcode[0])
    j_object = dict()
    j_object["postcodes"] = postcode_list
    return j_object


def find_max():
    """
    :return: the fci object that is found to be the highest
    """
    query_object = FciIndex.query.filter_by(fci=100).first()
    max_postcode = query_object.postcode
    maximum_fci = fci_object_return(max_postcode)
    return maximum_fci