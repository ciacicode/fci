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


def postToArea(postcode):
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


def postcodesDict (url, areaName):
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
            zonePostcode = postToArea(postCode)
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

def findXml(postcode):
    '''
       input a postcode returns dict of
       xml URL of area(s)
    '''
    # connect to database
    pPostcode = postToArea(postcode)
    db = MySQLdb.connect(host=config.host,user=config.user, passwd= config.password, db = config.database);
    cur = db.cursor()
    cur.execute('SELECT Area FROM fci_data.ordered_postcodes WHERE Postcode=(%s)',[pPostcode])
    db.commit()
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
        for entry in cur.fetchall():
           outputXmlDict[item] = entry
    return outputXmlDict
    db.close()

def fciIndex(postcode):
    '''
        requires postcode
        returns fciindex
    '''

    # create fci counter
    fciIndex = 0
    zoneInput = postToArea(postcode)
    keys = ("CHICKEN", "CHICK")
    noKeys = "NANDO"
    xmlDict = findXml(zoneInput)
    # unpack URLs from xmlDict
    for value in xmlDict.values():
        # each value is a tuple
        # parse the url with the etree library
        u = urlopen(value[0])
        tree = ET.parse(u)
        root = tree.getroot()
        collection = root.find('EstablishmentCollection')
        for detail in collection.findall('EstablishmentDetail'):
            postCode = detail.findtext('PostCode')
            if postCode is not None:
                zoneXML = postToArea(postCode)
                if zoneInput == zoneXML:
                    businessName = detail.find('BusinessName').text
                    upperBusinessName = businessName.upper()
                    pdb.set_trace()
                    if upperBusinessName == '':
                        break
                    elif noKeys in upperBusinessName:
                        break
                    else:
                        for key in  keys:
                            if key in upperBusinessName:
                                fciIndex = fciIndex + 1

    return fciIndex


def fciReturn(postcode):
    '''
    receives postcode
    returns fci
    '''
    # normalise input
    postcode = postToArea(postcode)
    # connect to database and create cursor
    db = MySQLdb.connect(host=config.host,user=config.user, passwd= config.password, db = config.database);
    cur = db.cursor()
    # check if there is already an entry in the database for that postcode
    # pdb.set_trace()
    cur.execute("SELECT FCI FROM fciIndex WHERE Postcode=(%s)", [postcode])
    db.commit()
    data = cur.fetchall()
    if len(data) == 0:
        error = 'There is no FCI data for this area'
        return str(error)
    else:
        data = data[0]
        data = data[0]
        return str(data)
    db.close()
