'''
    fciUtils is a set of common functions used in the realm of the project

    by ciacicode
'''

import xml.etree.ElementTree as ET
from urllib import urlopen
import json
import re
import config
import MySQLdb
import pdb


def post_to_area(postcode):
    '''takes a postcode, returns area code'''
    # normalise user input
    postcode = postcode.upper()
    postcode = re.sub('[\W_]', '', postcode)
    # remove last three chars for the house
    if len(postcode) >= 5:
        postcode = postcode[:-3]
        return postcode
    else:
        return postcode

def connect_fci_db():
    '''handles mysql db connection to fci database'''
    return MySQLdb.connect(host=config.host,user=config.user, passwd= config.password, db = config.database);


def postcodes_dict (url, areaName):
    ''' takes url of xml and area name
        output dict as {'area':{'unique postcodes'}}
    '''
    # parse the file with the etree library
    readURL = urlopen(url)
    tree = ET.parse(readURL)
    root = tree.getroot()
    collection = root.find('EstablishmentCollection')
    outputDict = {}
    nestList = []
    # iterate through the collection and append area postcode to a list
    for detail in collection.findall('EstablishmentDetail'):
        postCode = detail.findtext('PostCode')
        if postCode is not None:
            zonePostcode = post_to_area(postCode)
            #add postcodes to nested list
            nestList.append(zonePostcode)

    #normalise list
    nestList = set(nestList)
    nestList = list(nestList)
    outputDict[areaName] = nestList
    return outputDict

def resourcesDict(url):
    '''
        input url of json formatted data
        output dict
        { 'area': {'last_modified', 'url'}}
    '''
    readData = urlopen(url)
    jsonSimple = json.load(readData)
    jsonEncoded = json.dumps(jsonSimple)
    jsonDecoded = json.loads(jsonEncoded)
    resourcesDict={}
    for key in jsonDecoded.keys():
        if key == 'resources':
            #dive into the resources
            resourcesList = jsonDecoded['resources']
    for entry in resourcesList:
        nestDict = {}
        nestDict['last_modified'] = entry['last_modified']
        nestDict['url'] = entry['url']
        resourcesDict[entry['description']] = nestDict
    return resourcesDict

def find_xml(postcode):
    '''
       input a postcode returns dict of
       xml URL of area(s)
    '''
    # connect to database
    pPostcode = post_to_area(postcode)
    db = connect_fci_db()
    cur = db.cursor()
    cur.execute('SELECT Area FROM fci_data.ordered_postcodes WHERE Postcode=(%s)',[pPostcode])
    db.commit()
    # create lists for the output
    nestAreaList=[]
    outputAreaList = []
    for item in cur.fetchall():
        nestAreaList.append(item)
        for i in nestAreaList:
            for x in i:
                outputAreaList.append(x)
    outputAreaList = set(outputAreaList)
    outputAreaList = list(outputAreaList)
    # let us find the URLs of the xml data from the
    outputXmlDict = {}
    for item in outputAreaList:
        cur.execute('SELECT URL FROM fci_data.sources WHERE Area =(%s)',[item])
        db.commit()
        entries = cur.fecthall()
        db.close()
        for entry in entries:
           outputXmlDict[item] = entry
    return outputXmlDict

def fci_index(postcode):
    '''
        requires postcode
        returns fciindex
    '''

    # create fci counter
    fci_count = 0
    fci_index = 0
    restaurant_count = 0
    zone_input = post_to_area(postcode)
    keys = ("CHICKEN", "CHICK")
    no_keys = "NANDO"
    xmlDict = find_xml(zone_input)
    # unpack URLs from xmlDict
    for value in xmlDict.values():
        # each value is a tuple
        # parse the url with the etree library
        u = urlopen(value[0])
        tree = ET.parse(u)
        root = tree.getroot()
        collection = root.find('EstablishmentCollection')
        for detail in collection.findall('EstablishmentDetail'):
            postcode = detail.findtext('PostCode')
            if postcode is not None:
                zone_xml = post_to_area(postcode)
                if zone_input == zone_xml:
                    restaurant_count = restaurant_count + 1
                    business_name = detail.find('BusinessName').text
                    upper_business_name = business_name.upper()
                    if upper_business_name == '':
                        break
                    elif no_keys in upper_business_name:
                        break
                    else:
                        for key in  keys:
                            if key in upper_business_name:
                                fci_count = fci_count + 1
    fci_index = fci_count/restaurant_count
    return fci_index


def fci_return(postcode):
    '''
    receives postcode
    returns fci
    '''
    # normalise input
    postcode = post_to_area(postcode)
    # connect to database and create cursor
    db = connect_fci_db()
    cur = db.cursor()
    # check if there is already an entry in the database for that postcode
    # pdb.set_trace()
    cur.execute("SELECT FCI FROM fciIndex WHERE Postcode=(%s)", [postcode])
    db.commit()
    data = cur.fetchall()
    db.close()
    if len(data) == 0:
        error = 'There is no FCI data for this area'
        return str(error)
    else:
        data = data[0]
        data = data[0]
        return str(data)

