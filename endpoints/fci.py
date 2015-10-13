__author__ = 'ciacicode'

# This file contains the response of the Fried Chicken API that is returned by the: api.khaleesicode/fci endpoint

fci_api_mapping ={
    "url": "http://api.khaleesicode.com/fci",
    "description": "Returns FCI value for a given postcode as GET parameter api.khaleesicode.com/fci?postcode=<postcode>",
    "resources": {
        "postcodes": {
            "url": "http://api.khaleesicode.com/fci/postcodes",
            "description":"Returns list of postcodes comprised in the FCI"
        },
        "history": {
            "url": "http://api.khaleesicode.com/fci/history",
            "description": "Returns the known history of FCI values for a given postcode. It requires GET parameter postcode as api.khaleesicode.com/fci/history?postcode=<postcode>"
        },
        "maximum": {
            "url": "http://api.khaleesicode.com/fci/maximum",
            "description": "Returns the postcode associated with the maximum value of FCI as of latest available information",
        },
    },
}
