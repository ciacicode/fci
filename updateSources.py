'''
    Script to update the bigger table containing the URLs of xml data
    that is available thanks too data.gov.uk

    by ciacicode
'''

import fciUtils


def update_sources():
    """
        performs database update
    """
    # json data
    json = 'http://data.gov.uk/api/2/rest/package/uk-food-hygiene-rating-data'
    all_areas_data = fciUtils.resources_dict(json)
    '''This script aims to update all database tables so to provide a fresh data set'''
    db = fciUtils.connect_fci_db()
    # creating cursor object
    cur = db.cursor()
    # execute insert query
    cur.execute('TRUNCATE TABLE fci_data.sources')
    # commit query and close
    db.commit()
    # loop through the dictionary and store the xml data in the database
    db_id = 0
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
    


    


    