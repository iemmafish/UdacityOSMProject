import sqlite3
import csv

#------------------------------------CREATES THE NODES TABLE IN THE DATABASE ----------------------------------#

osmdb = 'pitts.db'

connection = sqlite3.connect(osmdb)
write_cursor = connection.cursor()
write_cursor.execute('''DROP TABLE IF EXISTS nodes;''')
write_cursor.execute('''
                    CREATE TABLE nodes(id INTEGER, lat TEXT, lon TEXT, user TEXT, uid INTEGER, version TEXT, changeset TEXT, timestamp TEXT)''')

connection.commit()

with open('nodes.csv', 'r') as csvfile:
    middleman = csv.DictReader(csvfile) # comma is default delimiter
    to_db = [(i['id'].decode("utf-8"), i['lat'].decode("utf-8"), i['lon'].decode("utf-8"), i['user'].decode("utf-8"), i["uid"].decode("utf-8"), i["version"].decode("utf-8"),i["changeset"].decode("utf-8"),i["timestamp"].decode("utf-8")) for i in middleman]


write_cursor.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?,?,?,?,?,?,?,?);", to_db)

connection.commit()
print('Table nodes created')
connection.close()

#--------------------------------------------CREATES TABLE NODES_TAGS ----------------------------------#

connection = sqlite3.connect(osmdb)
write_cursor = connection.cursor()
write_cursor.execute('''DROP TABLE IF EXISTS nodes_tags;''')
write_cursor.execute('''
                    CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT, type TEXT)''')

connection.commit()

with open('nodes_tags.csv', 'r') as csvfile:
    middleman = csv.DictReader(csvfile) # comma is default delimiter
    to_db = [(i['id'].decode("utf-8"), i['key'].decode("utf-8"), i['value'].decode("utf-8"), i['type'].decode("utf-8")) for i in middleman]

write_cursor.executemany("INSERT INTO nodes_tags(id, key, value, type) VALUES (?,?,?,?);", to_db)

connection.commit()
print('Table nodes_tags created')
connection.close()


#-----------------------------------CREATES TABLE WAYS --------------------------------------------#

connection = sqlite3.connect(osmdb)
write_cursor = connection.cursor()
write_cursor.execute('''DROP TABLE IF EXISTS ways;''')
write_cursor.execute('''
                    CREATE TABLE ways(id INTEGER, user TEXT, uid TEXT, version TEXT, changeset TEXT, timestamp TEXT)''')

connection.commit()

with open('ways.csv', 'r') as csvfile:
    middleman = csv.DictReader(csvfile) # comma is default delimiter
    to_db = [(i['id'].decode("utf-8"), i['user'].decode("utf-8"), i['uid'].decode("utf-8"), i['version'].decode("utf-8"), i["changeset"].decode("utf-8"), i["timestamp"].decode("utf-8")) for i in middleman]

write_cursor.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?,?,?,?,?,?);", to_db)

connection.commit()
print('Table ways created')
connection.close()


#---------------------------------------------TABLE WAYS_TAGS CREATED -----------------------------------------#

connection = sqlite3.connect(osmdb)
write_cursor = connection.cursor()
write_cursor.execute('''DROP TABLE IF EXISTS ways_tags;''')
write_cursor.execute('''
                    CREATE TABLE ways_tags(id INTEGER, key TEXT, value TEXT, type TEXT)''')

connection.commit()

with open('ways_tags.csv', 'r') as csvfile:
    middleman = csv.DictReader(csvfile) # comma is default delimiter
    to_db = [(i['id'].decode("utf-8"), i['key'].decode("utf-8"), i['value'].decode("utf-8"), i['type'].decode("utf-8")) for i in middleman]

write_cursor.executemany("INSERT INTO ways_tags(id, key, value, type) VALUES (?,?,?,?);", to_db)

connection.commit()
print('Table ways_tags created')
connection.close()


#---------------------------------------------TABLE WAYS_NODES CREATED -----------------------------------------#

connection = sqlite3.connect(osmdb)
write_cursor = connection.cursor()
write_cursor.execute('''DROP TABLE IF EXISTS ways_nodes;''')
write_cursor.execute('''
                    CREATE TABLE ways_nodes(id INTEGER, node_id INTEGER, position INTEGER)''')

connection.commit()

with open('ways_nodes.csv', 'r') as csvfile:
    middleman = csv.DictReader(csvfile) # comma is default delimiter
    to_db = [(i['id'].decode("utf-8"), i['node_id'].decode("utf-8"), i['position'].decode("utf-8")) for i in middleman]

write_cursor.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?,?,?);", to_db)

connection.commit()
print('Table ways_nodes created')
connection.close()

