'''
    Script to update the bigger table containing the URLs of xml data
    that is available thanks too data.gov.uk

    by ciacicode
'''

import fciUtils

def updateSources():
    """
    performs database update
    """
    # json data
    json = 'http://data.gov.uk/api/2/rest/package/uk-food-hygiene-rating-data'
    allAreasData = fciUtils.resourcesDict(json)

    '''This script aims to update all database tables so to provide a fresh data set'''

    db = fciUtils.connect_fci_db()
    # creating cursor object
    cur = db.cursor()

    # execute insert query
    cur.execute('TRUNCATE TABLE fci_data.sources')
    # commit query and close

    db.commit()

    # loop through the dictionary and store the xml data in the database

    dbID = 0
    for key , value in allAreasData.items():
        # store the key
        tempArea = key
        # store the content of the value
        tempValue = value
        # access the tempValue dictionary to store variables
        lastModified = tempValue['last_modified']
        url = tempValue['url']
        dbID = dbID + 1
        # write in the database all this stuff
        # execute insert query
        cur.execute('INSERT INTO sources (ID,Area,LastModified,URL) VALUES (%s,%s,%s,%s)',(dbID,tempArea,lastModified,url))

        # commit query and close
        db.commit()
    db.close()
    


    


    