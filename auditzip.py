from collections import defaultdict
import re
import xml.etree.cElementTree as ET
import pprint

#all zip codes that could be in the data set
expected =  ['15106',
    '15203',
    '15207',
    '15212',
    '15216',
    '15220',
    '15120',
    '15201',
    '15202',
    '15204',
    '15205',
    '15206',
    '15208',
    '15210',
    '15211',
    '15213',
    '15214',
    '15215',
    '15217',
    '15218',
    '15219',
    '15221',
    '15222',
    '15224',
    '15226',
    '15227',
    '15230',
    '15232',
    '15233',
    '15234',
    '15236',
    '15238',
    '15240',
    '15250',
    '15251',
    '15252',
    '15253',
    '15254',
    '15255',
    '15257',
    '15258',
    '15259',
    '15260',
    '15261',
    '15262',
    '15264',
    '15265',
    '15267',
    '15272',
    '15274',
    '15275',
    '15276',
    '15278',
    '15281',
    '15282',
    '15283',
    '15289',
    '15290',
    '15295',
             '15012',
             '15017',
             '15025',
             '15031',
             '15034',
             '15071',
             '15085',
             '15102',
             '15104',
             '15108',
             '15110',
             '15112',
             '15116',
             '15122',
             '15131',
             '15132',
             '15133',
             '15137',
             '15139',
             '15142',
             '15143',
             '15145',
             '15146',
             '15147',
             '15148',
             '15035',
             '15136',
             '15209',
             '15223',
             '15225',
             '15228',
             '15229',
             '15235',
             '15237',
             '15239',
             '15241',
             '15247',
             '15321',
             '15642',
             '16063',
             '15243'
                     ]        



#initial mapping
mapping = {}

#14233 shows up in the data but it's a buffalo, ny zip?
#151363 shows up in the data which is too many numbers!

#Create list of mapping keys
mapping_keys = []
for k,v in mapping.items():
    mapping_keys.append(k)
    
#get the zip code from the XML file
def is_zip(elem):
    return (elem.attrib['k'] == "addr:postcode")

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit_zip(osmfile):
    osm_file = open(osmfile, "r")
    zipcodes = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zip(tag):
                    audit_street_type(zipcodes, tag.attrib['v'])
    osm_file.close()
    return zipcodes

def update_zip(name):
    if name in mapping_keys: #If the bad key is in the mapping dictionary, then perform a substitute
        good = mapping[name]
        return good
    elif len(name) > 5: #If the zip is in the longer format, just use the first 5 numbers
        return name[0:5]
    else:
        return name

def test():
    st_types = audit_zip('pittsburgh.xml')
    pprint.pprint(dict(st_types))
    
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_zip(name)
            print name, "=>", better_name
            

if __name__ == '__main__':
    test()
