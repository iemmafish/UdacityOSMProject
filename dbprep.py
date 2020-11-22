#called data.py in the Udacity case study

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH = "pittsburgh.xml"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

def process_key(key_string): 
      """
      This function processes 'k' values to slice and separate key strings into
      their respective keys and tag types. It returns an ordered listed with
      the new key and the tag type. 
      """
      if ":" in key_string:   
            indexed_string = key_string.find(":")
            tag_type = key_string[:indexed_string]
            new_key = key_string[indexed_string+1:]
            return [new_key, tag_type]
      else:
            new_key = key_string
            tag_type = "regular"
            return [new_key, tag_type]


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    if element.tag == 'node':

      # first loop through to get node's attributes and values into a dictinonary
        for attrName, attrValue in element.attrib.items():
            if attrName in NODE_FIELDS:
                node_attribs[attrName] = attrValue
        #print node_attribs

        """ 
        Next, loop through the child tags and parse out the
        key, value, and clean up the 'key' to create types. Then
        put everything into a dictionary to append to tags list.
        """
        for i in element.iter('tag'):
            #print i
            temp_dict = {}
            if PROBLEMCHARS.search(i.attrib['k']):
                continue
            else:
                temp_dict['id'] = element.attrib['id']
                temp_dict['key'] = process_key(i.attrib['k'])[0]
                temp_dict['type'] = process_key(i.attrib['k'])[1]
                temp_dict['value'] = i.attrib['v']
                #print temp_dict
            tags.append(temp_dict)
        #print tags

        return {'node': node_attribs, 'node_tags': tags}

    elif element.tag == 'way':

        for attrName, attrValue in element.attrib.items():
            if attrName in WAY_FIELDS:
                #print attrName
                #print attrValue
                way_attribs[attrName] = attrValue
        #print way_attribs

        """ 
        Since the way tags follow the same rules as the node tags, these
        are processed the same way.
        """
        for i in element.iter('tag'):
            temp_dict = {}
            if PROBLEMCHARS.search(i.attrib['k']):
                continue
            else:
                temp_dict['id'] = element.attrib['id']
                temp_dict['key'] = process_key(i.attrib['k'])[0]
                temp_dict['type'] = process_key(i.attrib['k'])[1]
                temp_dict['value'] = i.attrib['v']
            tags.append(temp_dict)
        print tags

        """
        enumerate() is used here to create a counter for each 'nd' child node.
        """

        for counter, i in enumerate(element.iter('nd')):
            temp_dict = {}
            temp_dict['id'] = element.attrib['id']
            temp_dict['node_id'] = i.attrib['ref']
            temp_dict['position'] = counter
            way_nodes.append(temp_dict)
        #print way_nodes

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)
