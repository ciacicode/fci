'''
    script to update the fciIndex table

    by ciacicode

    Note: needs improvement
'''


import fciUtils
import pdb

def updateFci():
    '''updates the fciindex table '''
    # connect to the database
    db = fciUtils.connect_fci_db()
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
        fci = fciUtils.fci_index(value)
        cur.execute("INSERT INTO fciIndex (Postcode,FCI) VALUES (%s,%s)", (value,fci))
        db.commit()
    db.close()