from collections import defaultdict
import re
import xml.etree.cElementTree as ET
import pprint

expected = []

#get the phone number from the XML file
def is_phonenumber(elem):
    return (elem.attrib['k'] == "phone")

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit_phonenumber(osmfile):
    osm_file = open(osmfile, "r")
    phone_numbers = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_phonenumber(tag):
                    audit_street_type(phone_numbers, tag.attrib['v'])
    osm_file.close()
    return phone_numbers

def update_phonenumbers(phonenumber):
    #print phonenumber 
    clean_number = phonenumber
    # remove all non digits
    clean_number = re.sub(r'\D', "", clean_number)
    #print clean_number

    if len(clean_number) == 11:
        # full phone number
        formatted_number =  '+{0} {1} {2}-{3}'.format(clean_number[0:1], clean_number[1:4], clean_number[4:7], clean_number[7:])
    elif len(clean_number) == 10:
        # partial phone number, no international code, starting with 0
        formatted_number =  '+1 {0} {1}-{2}'.format(clean_number[0:3], clean_number[3:6], clean_number[6:])
    else:
        # invalid number
        formatted_number = ""

    return formatted_number

def test():
    st_types = audit_phonenumber('pittsburgh.xml')
    #pprint.pprint(dict(st_types))
    
    
    
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_phonenumbers(name)
            print name, "=>", better_name
            

if __name__ == '__main__':
    test()
