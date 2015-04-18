'''
    Script to update the bigger unsorted table of postcodes and areas

    by ciacicode
    
'''




import MySQLdb
import config
import fciUtils
import pdb

# loop through the xml files in the database and update the postcode database
# parse the file with the etree library

# connect to database
db = MySQLdb.connect(host=config.host,user=config.user, passwd= config.password, db = config.database);
# creating cursor object
cur = db.cursor()
cur.execute('TRUNCATE TABLE fci_data.postcodes')
# commit query and close
    
db.commit()
db.close()

# connect to database
db = MySQLdb.connect(host=config.host,user=config.user, passwd= config.password, db = config.database);
# creating cursor object
cur = db.cursor()
        
# execute insert query
cur.execute('SELECT Area, URL FROM fci_data.sources')

#pdb.set_trace()
for area, url in cur.fetchall():
    # pass the url to an xmlparser function
    tempDict = fciUtils.postcodesDict(url,area)
    valueList = tempDict.values()
    iterable = valueList[0]
    # parse the dict and write into database
    for value in iterable:
        if value == "":
            break
        else:
            # execute insert query
            cur.execute('INSERT INTO postcodes (Postcode,Area) VALUES (%s,%s)',(value,area))
            # commit query
            db.commit()
            # close connection

db.close()
