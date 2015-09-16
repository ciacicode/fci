'''
    Script to update the bigger table containing the URLs of xml data
    that is available thanks too data.gov.uk

    by ciacicode
'''


import fciUtils
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import db_models


def update_sources():
    """
        performs database update
    """
    # json data
    json = 'http://data.gov.uk/api/2/rest/package/uk-food-hygiene-rating-data'
    all_areas_data = fciUtils.resources_list(json)
    # drop fcisources table
    db.drop_all(bind=['fci_sources'])
    for key , value in all_areas_data.items():
        # store the key
        temp_area = key
        # store the content of the value
        temp_value = value
        # access the temp_value dictionary to store variables
        last_modified = temp_value['last_modified']
        url = temp_value['url']
        db_id += 1
        # write in the database all this stuff
        # execute insert query
        cur.execute('INSERT INTO sources (ID,Area,LastModified,URL) VALUES (%s,%s,%s,%s)', (db_id, temp_area,
                                                                                            last_modified, url))
        # commit query and close
        db.commit()
    db.close()
    


    


    