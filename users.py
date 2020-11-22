#called users.py in the Udacity case study

import xml.etree.cElementTree as ET
import pprint

#----------------------------------How Many Users-------------#
#this section of code allows us to explore how many unique users have 
#have contributed to the map in this particular area

def get_user(element):
    return


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if "uid" in element.attrib:
            users.add(element.attrib["uid"])

    return users


def test():

    users = process_map('pittsburgh.xml')
    print("Number of users who have contributed to this region of the map:")
    pprint.pprint(len(users))
    
    

if __name__ == "__main__":
    test()
