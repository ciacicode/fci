"""
    Script to sort postcodes in database
    by grutin
"""

import fciUtils
import pdb

db = fciUtils.connect_fci_db()
cur = db.cursor()
cur.execute('TRUNCATE TABLE fci_data.ordered_postcodes')
cur.execute('SELECT Postcode, Area FROM fci_data.postcodes ORDER BY Postcode')

for Postcode, Area in cur.fetchall():
    cur.execute('INSERT INTO fci_data.ordered_postcodes (Postcode, Area) VALUES (%s,%s)', (Postcode, Area))
    db.commit()
db.close()
