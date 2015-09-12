
"""
    script to update the fciIndex table

    by ciacicode

    Note: needs improvement
"""


import fciUtils
import operator
from database import *
import pdb


def update_fci():
    """
        updates table containing the fci_index for
        each london area.
    """
    cur = db.cursor()
    cur.execute("SELECT Postcode FROM ordered_postcodes")
    db.commit()
    postcodes = cur.fetchall()
    postcodes = sorted(set(postcodes))
    dict_fci = dict()
    for p in postcodes:
        p = p[0]
        fci = fciUtils.fci_calculate(p)
        dict_fci[p] = fci
    maximum_key = max(dict_fci.iteritems(), key=operator.itemgetter(1))[0]
    maximum = dict_fci[maximum_key]

    # clear up the fciIndex table
    cur.execute("TRUNCATE fciIndex")
    db.commit()
    for key, value in dict_fci.iteritems():
        index = (value/maximum)*100
        cur.execute("INSERT INTO fciIndex (Postcode,FCI) VALUES (%s,%s)", (key, index))
        db.commit()
    db.close()