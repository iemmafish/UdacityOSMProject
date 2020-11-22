from collections import defaultdict
import re
import xml.etree.cElementTree as ET
import pprint

expected = ["PA"]

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#mapping
mapping = { "15219": "PA",
            "Pa": "PA",
            "p":"PA",
            "Pennsylvania":"PA",
            "pa": "PA"
          }
#gets the name of the state from the XML file
def is_state_name(elem):
    return (elem.attrib['k'] == "addr:state")

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def audit_state(osmfile):
    osm_file = open(osmfile, "r")
    state_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_state_name(tag):
                    audit_street_type(state_types, tag.attrib['v'])
    osm_file.close()
    return state_types

#Create list of mapping keys
mapping_keys = []
for k,v in mapping.items():
    mapping_keys.append(k)

def update_state_name(name):
    if name in mapping_keys: 
        #If the bad key is in the mapping dictionary perform a substitution, otherwise leave it alone
        good = mapping[name]
        return good
    else:
        return name
    
def test():
    st_types = audit_state('pittsburgh.xml')
    pprint.pprint(dict(st_types))
      
    
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_state_name(name)
            print name, "=>", better_name
            

if __name__ == '__main__':
    test()
