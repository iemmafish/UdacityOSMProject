#called mapparser.py in the Udacity case study

import xml.etree.cElementTree as ET
import pprint

#--------------------------Iterative Parsing---------------------------------#


def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag not in tags:
            tags[elem.tag] = 1
        else:
            tags[elem.tag] += 1
    return tags

def test():

    tags = count_tags('pittsburgh.xml')
    pprint.pprint(tags)
      

if __name__ == "__main__":
    test()
