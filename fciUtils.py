'''
    fciUtils is a set of common functions used in the realm of the project

    by ciacicode
'''
from __future__ import division
import xml.etree.ElementTree as ET
from urllib2 import urlopen
import json
import re
import config
import MySQLdb
import pdb


def post_to_area(postcode):
    """takes a postcode, returns area code"""
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
    """handles mysql db connection to fci database"""
    return MySQLdb.connect(host=config.host, user=config.user, passwd=config.password, db=config.database);


def postcodes_dict(url, area_name):
    """
        Takes url of xml and area name
        output dict as {'area':{'unique postcodes'}}
    """
    # parse the file with the etree library
    read_url = urlopen(url)
    tree = ET.parse(read_url)
    root = tree.getroot()
    collection = root.find('EstablishmentCollection')
    output_dict = {}
    nest_list = []
    # iterate through the collection and append area postcode to a list
    for detail in collection.findall('EstablishmentDetail'):
        post_code = detail.findtext('PostCode')
        if post_code is not None:
            zone_postcode = post_to_area(post_code)
            # add postcodes to nested list
            nest_list.append(zone_postcode)

    #normalise list
    nest_list = set(nest_list)
    nest_list = list(nest_list)
    output_dict[area_name] = nest_list
    return output_dict


def resources_dict(url):
    """
        input url of json formatted data
        output dict
        { 'area': {'last_modified', 'url'}}
    """
    read_data = urlopen(url)
    json_simple = json.load(read_data)
    json_encoded = json.dumps(json_simple)
    json_decoded = json.loads(json_encoded)
    resources_dict= dict()
    for key in json_decoded.keys():
        if key == 'resources':
            # dive into the resources
            resources_list = json_decoded['resources']
    for entry in resources_list:
        nest_dict = dict()
        nest_dict['last_modified'] = entry['last_modified']
        nest_dict['url'] = entry['url']
        resources_dict[entry['description']] = nest_dict
    return resources_dict


def find_xml(postcode):
    """
       input a postcode returns dict of
       xml URL of area(s)
    """
    # connect to database
    p_postcode = post_to_area(postcode)
    db = connect_fci_db()
    cur = db.cursor()
    cur.execute('SELECT Area FROM fci_data.ordered_postcodes WHERE Postcode=(%s)', [p_postcode])
    db.commit()
    # create lists for the output
    nest_area_list = list()
    output_area_list = list()
    for item in cur.fetchall():
        nest_area_list.append(item)
        for i in nest_area_list:
            for x in i:
                output_area_list.append(x)
    output_area_list = set(output_area_list)
    output_area_list = list(output_area_list)
    # let us find the URLs of the xml data from the
    output_xml_dict = dict()
    for item in output_area_list:
        cur.execute('SELECT URL FROM fci_data.sources WHERE Area =(%s)', [item])
        db.commit()
        for entry in cur.fetchall():
            output_xml_dict[item] = entry
    db.close()
    return output_xml_dict


def fci_calculate(postcode):
    """
        requires postcode
        returns fciindex
    """

    # create fci counter
    fci_count = 0
    fci_index = 0
    restaurant_count = 0
    zone_input = post_to_area(postcode)
    keys = ("CHICKEN", "CHICK", "FRIED")
    no_keys = "NANDO"
    xml_dict = find_xml(zone_input)
    # unpack URLs from xml_dict
    for value in xml_dict.values():
        # each value is a tuple
        # parse the url with the etree library
        u = urlopen(value[0])
        tree = ET.parse(u)
        root = tree.getroot()
        collection = root.find('EstablishmentCollection')
        for detail in collection.findall('EstablishmentDetail'):
            xml_postcode = detail.findtext('PostCode')
            if xml_postcode is not None:
                zone_xml = post_to_area(xml_postcode)
                if zone_input == zone_xml:
                    restaurant_count += 1
                    business_name = detail.find('BusinessName').text
                    upper_business_name = business_name.upper()
                    if upper_business_name == '':
                        break
                    elif no_keys in upper_business_name:
                        break
                    else:
                        for key in keys:
                            if key in upper_business_name:
                                fci_count += 1
                                break
    if restaurant_count == 0:
        return fci_count
    else:
        result = fci_count/restaurant_count
        return result


def fci_return(postcode):
    """
        receives postcode
        returns formatted fci
    """
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
        no_data = 'There is no FCI data for this area'
        return str(no_data)
    else:
        data = data[0]
        data = data[0]
        return "{0:.3f}%".format(data * 100)

