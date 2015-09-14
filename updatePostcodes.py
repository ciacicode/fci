'''
    Script to update the bigger unsorted table of postcodes and areas

    by ciacicode
    
'''


import fciUtils
from db_models import *
import pdb

# loop through the xml files in the database and update the postcode database
# parse the file with the etree library


# creating cursor object
cur = db.cursor()
cur.execute('TRUNCATE TABLE fci_data.postcodes')
# commit query and close
    
db.commit()
db.close()

# creating cursor object
cur = db.cursor()
        
# execute insert query
cur.execute('SELECT Area, URL FROM fci_data.sources')

for area, url in cur.fetchall():
    # pass the url to an xmlparser function
    tempDict = fciUtils.postcodes_dict(url, area)
    valueList = tempDict.values()
    iterable = valueList[0]
    # parse the dict and write into database
    for value in iterable:
        if value == "":
            break
        else:
            # execute insert query
            cur.execute('INSERT INTO postcodes (Postcode,Area) VALUES (%s,%s)', (value, area))
            # commit query
            db.commit()
            # close connection

db.close()
