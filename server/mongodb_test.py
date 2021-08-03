# requires pymongo and pymongo[srv]

from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB
client = MongoClient("mongodb+srv://admin:atlasadmin1@cluster0.cwe5c.mongodb.net/test")

# set the db to be Hesparia 
db=client['hesparia']

# set the speciific collection 
mycol=db['example1']
# mycol.insert_one({'key1':'value1'})
# mycol.delete_one({'key1':'value1'})

pprint(mycol.estimated_document_count())

if 'example1' in db.list_collection_names():
    print('example1 exists')
# Issue the serverStatus command and print the results
#serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)

# Get some data output from hesparia db
# pprint(client.hesparia.objects)


