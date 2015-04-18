'''
    script to update the fciIndex table

    by ciacicode

    Note: needs improvement
'''


import fciUtils
import MySQLdb
import config
import pdb

def updateFci():
    '''updates the fciindex table '''
    # connect to the database
    db = MySQLdb.connect(host=config.host,user=config.user, passwd= config.password, db = config.database);
    cur = db.cursor()
    # clear up the fciIndex table
    cur.execute("TRUNCATE fciIndex")
    db.commit()
    # select postcodes from ordered_postcode
    # pdb.set_trace()
    cur.execute("SELECT Postcode FROM ordered_postcodes")
    db.commit()
    data = cur.fetchall()
    data = sorted(set(data))
    for value in data:
        # calculate index
        value = value[0]
        fci = fciUtils.fciIndex(value)
        cur.execute("INSERT INTO fciIndex (Postcode,FCI) VALUES (%s,%s)", (value,fci))
        db.commit()
    db.close()