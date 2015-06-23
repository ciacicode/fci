
'''
    script to update the fciIndex table

    by ciacicode

    Note: needs improvement
'''


import fciUtils
import operator
import pdb

def find_max():
    """returns highest fried chicken index"""
    db = fciUtils.connect_fci_db()
    cur = db.cursor()
    cur.execute("SELECT Postcode FROM ordered_postcodes")
    db.commit()
    postcodes = cur.fetchall()
    postcodes =sorted(set(postcodes))
    db.close()
    #pdb.set_trace()
    dict_fci = {}
    for p in postcodes:
        p = p[0]
        fci = fciUtils.fci_calculate(p)
        dict_fci[p] = fci
    maximum_key = max(dict_fci.iteritems(), key=operator.itemgetter(1))[0]
    maximum = dict_fci[maximum_key]
    return maximum, dict_fci




def updateFci(maximum, mydict):
    '''
    updates the fciindex table with indexes
    accepts maximum raw fci and the fci list as input
    '''

    db = fciUtils.connect_fci_db()
    cur = db.cursor()
     # clear up the fciIndex table
    cur.execute("TRUNCATE fciIndex")
    db.commit()
    for key, value in mydict.iteritems():
        index = (value/maximum)*100
        cur.execute("INSERT INTO fciIndex (Postcode,FCI) VALUES (%s,%s)", (key,index))
        db.commit()

    db.close()