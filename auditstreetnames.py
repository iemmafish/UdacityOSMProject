#called audit.py in the udacity case study

from collections import defaultdict
import re
import xml.etree.cElementTree as ET
import pprint

#--------------Fixing the Street Names---------------------#
#this function takes a string with a street name as an argument and
#returns the fixed name 

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
            "Square", "Lane", "Road", "Pike", "Plaza", "Way",
            "Trail", "Highway", "Parkway", "Terrace",
            "Alley", "Circle", "Commons", "Temple", "North", "South",
            "East", "West"]

mapping = { "St": "Street",
            "St.": "Street",
            "Hwy": "Highway",
            "Hwy.": "Highway",
            "Rd.": "Road",
            "Rd": "Road",
           "Ave": "Avenue",
            "Av.": "Avenue",
           "Ave.": "Avenue",
           "ave": "Avenue",
           "N.": "North",
           "N": "North",
           "S.": "South",
           "S": "South",
           "E.": "East",
           "E": "East",
           "W.": "West",
           "W": "West", 
           "Ct": "Court",
            "Blvd": "Boulevard",
            "DRive": "Drive",
            "Dr": "Drive",
            "Brdg": "Bridge",
            "Pl": "Place",
            "Sq": "Square",
            "Ter": "Terrace"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

#grabs the street name from the XML
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):

    m = street_type_re.search(name)
    if m:
        if m.group() in mapping.keys():
            better_street_type = mapping[m.group()]
            name = street_type_re.sub(better_street_type, name)
        
    return name


def test():
    st_types = audit('pittsburgh.xml')
    pprint.pprint(dict(st_types))
     
    
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            

if __name__ == '__main__':
    test()
