#FCI

This is a python project to create an application that calculates a London area's Fried Chicken Index (FCI).
The FCI is calculated based on instances of fried chicken shops in the area. The front-end of this app is done with flask and can be found in the khaleesicode repo

## Requirements
*python 2.7
*MySQL

## Databases
* fci_data.sources
* fci_data.postcodes
* fci_data.ordered_postcodes
* fci_data.fciIndex

## List of custom libraries
* fciUtils.py

The functions included in fciUtils take care of database update and maintenance for the application. There are also small helper functions to normalise input.

