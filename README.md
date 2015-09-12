#FCI

This is a python project to create an application that calculates a London area's Fried Chicken Index (FCI).
The FCI is calculated based on instances of fried chicken shops in the area. The front-end of this app is done with flask and can be found in the khaleesicode repo

## Requirements
* Python 2.7
* MySQL
* Flask
* SQLAlchemy > 0.6
* Flask-SQLAlchemy

## Databases Tables
|fci_data.sources|
```
ID	int(11)
Area	varchar(255)
LastModified	varchar(255)
URL	varchar(255)
```|
|fci_data.postcodes|
```
Postcode	varchar(15)
Area	varchar(255)
```|

|fci_data.ordered_postcodes|
```
Postcode	varchar(15)
Area	varchar(255)
```|
|fci_data.fciIndex|
```
Postcode	varchar(15)
FCI	float
```
|

## List of custom libraries
* fciUtils.py

The functions included in fciUtils take care of database update and maintenance for the application. There are also small helper functions to normalise input.

## Installation and use

Clone the repository in the chosen directory:
``` git clone https://github.com/ciacicode/fci.git ```

Set up the environment so that you have all required modules as listed above in the Requirements section.

### Step 1: Update Sources
After setting up the databases on your localhost, define variables in the config.py file. Those variables will be used to connect to the database. The process starts with the function ```update_sources() ``` in the updateSources.py script. The function starts off building the table fci_data.sources based on the content of the xml returned by the Food Hygiene API for London. The fci_data.sources table always contains the freshest data in terms of links to the individual areas information.

### Step 2: Update list of postcodes
After updating the sources we can make sure we have a fresh list of related postcodes. This is possible by running the script in updatePostcodes.py. This script updates the fci_data.postcodes table, while the script called orderedPostcodes, makes sure we create another table of ordered postcodes. This is a flaw in design as we could simply sort the postcode table and rewrite it there but for the moment I do not care.

### Step 3: Update the fciIndex table
After the postcodes are all set in their tables it is only necessary to run the ```update_fci()``` function in the updateFciIndex.py file to refresh the table with new fci data.

### Notes
At the moment the database structure is not taking into consideration historical data.




