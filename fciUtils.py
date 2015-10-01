'''
    fciUtils is a set of common functions used in the realm of the project

    by ciacicode
'''
from __future__ import division
import xml.etree.ElementTree as ET
from urllib2 import urlopen
import json
import re
import db_models
from datetime import datetime
import string


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


def resources_list(url):
    """
        input url of json formatted data
        output list
        crete a list of FciSources database objects
    """
    read_data = urlopen(url)
    json_simple = json.load(read_data)
    json_encoded = json.dumps(json_simple)
    json_decoded = json.loads(json_encoded)
    resources_list= list()
    final_list = list()
    for key in json_decoded.keys():
        if key == 'resources':
            # dive into the resources
            resources_list = json_decoded['resources']
    for entry in resources_list:
        last_modified = entry['last_modified']
        # Remove the bloody T from the date
        last_modified = string.split(last_modified,'T')
        day = last_modified[0]
        hours = last_modified[1]
        dt_last_modified = day + " " + hours
        dt_last_modified = datetime.strptime(dt_last_modified, "%Y-%m-%d %H:%M:%S.%f")
        url = entry['url']
        area = entry['description']
        source = db_models.FciSources(area, url, dt_last_modified)
        final_list.append(source)
    return final_list



def fci_calculate(postcode):
    """
        requires postcode
        returns fciindex
    """

    # create fci counter
    fci_count = 0
    restaurant_count = 0
    zone_input = post_to_area(postcode)
    keys = ("CHICKEN", "CHICK", "FRIED")
    no_keys = "NANDO"
    url = db_models.find_xml(zone_input)
    # unpack URLs from xml_dict
    u = urlopen(url)
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

