# requires pymongo and pymongo[srv]
import os, sys
import re

from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB
client = MongoClient("mongodb+srv://admin:atlasadmin1@cluster0.cwe5c.mongodb.net/test")

# set the db to be Hesparia 
db=client['Hesparia']

# create or access "Pins"  collection 
mycol=db['Pins']

# import data from types.tx
parent_folder = (os.path.dirname(os.getcwd()))
with open(parent_folder+"\\client\\src\\types.ts", 'r',) as f: 
    types = f.read() 

# get the names of each collection
for paragraph in types.split("}"):
    for line in paragraph.splitlines(): 
        if re.match(r'^\s*$', line):
            continue
        if 'export' in line: 
            new_col = line.split()[2]

            # make the collection
            col=db[new_col]
            exampleData = {
                'example': 1
            }
            col.insert_one(exampleData)       