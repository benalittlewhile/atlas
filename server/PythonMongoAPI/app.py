import flask
from flask import request, jsonify, abort
from pymongo import MongoClient
import json 
from bson.objectid import ObjectId

# Set up flask 
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# set up the database access
from dotenv import load_dotenv
import os
load_dotenv()
MONGODB_LOGIN_PATH = os.getenv('MONGODB_LOGIN_PATH')
client = MongoClient(MONGODB_LOGIN_PATH)
db=client['Hesparia']

# Make a dictionary with key:value pairing where
# key is the collection name e.g. Person
# value is a list of properties that the collection has e.g. Name

def update_collections_dictionary():
    collections_dictionary = {}
    for collection in db.list_collection_names(): 
        collections_dictionary[collection] = []
        for properties in db[collection].find({}): 
            for property in properties.keys(): 
                if property not in collections_dictionary[collection]: 
                    collections_dictionary[collection].append(property)
    return(collections_dictionary)

collections_dictionary = update_collections_dictionary()

# we need a custom json encoder because ObjectId is a type that jsonify doesnt like
def customEncoder(o):
    if type(o) == ObjectId:
        return str(o)
    return o.__str__


# Home landing page
@app.route('/', methods=['GET', 'POST'])
def home():
    print('home')
    return "<h1>Hesparia API</h1><p>This site is a prototype API for Hesparia.</p>"


'''
                                                  ,d                
                                                  88                
 ,adPPYba,  8b,dPPYba,   ,adPPYba,  ,adPPYYba,  MM88MMM  ,adPPYba,  
a8"     ""  88P'   "Y8  a8P_____88  ""     `Y8    88    a8P_____88  
8b          88          8PP"""""""  ,adPPPPP88    88    8PP"""""""  
"8a,   ,aa  88          "8b,   ,aa  88,    ,88    88,   "8b,   ,aa  
 `"Ybbd8"'  88           `"Ybbd8"'  `"8bbdP"Y8    "Y888  `"Ybbd8"' 
'''
@app.route('/api/v1/create/<collection_name>/', methods=['GET', 'POST'])
def create(collection_name):
    # http://127.0.0.1:5000/api/v1/create/Person/
    # creates a new document in the collection Person
    if not request.json: 
        abort(400)
    if collection_name.title() in list(collections_dictionary.keys()): 
        col=db[collection_name.title()]
        x = col.insert_one(request.json)
        return(json.dumps(x.inserted_id, default=customEncoder))
    return(json.dumps("Error: "+collection_name+" not in db", default=customEncoder))


@app.route('/api/v1/create_collection/<collection_name>/', methods=['GET', 'POST'])
def create_collection(collection_name):
    # http://127.0.0.1:5000/api/v1/create/Person/
    # creates a new collection called Person
    if not request.json: 
        abort(400)
    if collection_name.title() not in list(collections_dictionary.keys()): 
        col=db[collection_name.title()]
        x = col.insert_one(request.json)
        print("done")
        return(json.dumps("created "+ str(x.inserted_id)+ " in "+ collection_name, default=customEncoder))
    else:
        return(json.dumps("Error: "+collection_name+" already exists.", default=customEncoder))

'''
                                             88  
                                             88  
                                             88  
8b,dPPYba,   ,adPPYba,  ,adPPYYba,   ,adPPYb,88  
88P'   "Y8  a8P_____88  ""     `Y8  a8"    `Y88  
88          8PP"""""""  ,adPPPPP88  8b       88  
88          "8b,   ,aa  88,    ,88  "8a,   ,d88  
88           `"Ybbd8"'  `"8bbdP"Y8   `"8bbdP"Y8
'''
# Get all collections
@app.route('/api/v1/collections/', methods=['GET'])
def collections(): 
    update_collections_dictionary
    return json.dumps(list(collections_dictionary.keys()), default=customEncoder)

# Get all docs of a given collection
@app.route('/api/v1/<collection_name>/all/', methods=['GET'])
def get_all(collection_name):
    # http://127.0.0.1:5000/api/v1/Person/all
    # returns all documents in Person collection
    if collection_name.title() in list(collections_dictionary.keys()):
        col=db[collection_name.title()].find()
        list_of_docs=[]
        for doc in col: 
            list_of_docs.append(doc)
        return json.dumps(list_of_docs, default=customEncoder)
    else: 
        return("Error: "+collection_name+" not in db")


@app.route('/api/v1/property_search/<property_name>/<search_value>/', methods=['GET', 'POST'])
def property_search(property_name, search_value):
    # http://127.0.0.1:5000/api/v1/propertysearch/name/Kobe
    # anything anywhere with name "Kobe"
    matches = []
    for collection in collections_dictionary: 
        if property_name in collections_dictionary[collection]: 
            col=db[collection].find()
            for doc in col: 
                doc_keys = [x for x in doc.keys()]
                if property_name in doc_keys: # IF PROPERTY IN 
                    if str(doc[property_name]) == search_value: 
                        matches.append(doc)
    return json.dumps(matches, default=customEncoder)


@app.route('/api/v1/property_collection_search/<collection_name>/<property_name>/<search_value>/', methods=['GET'])
def property_collection_search(collection_name, property_name, search_value):
    # Example: 
    # http://127.0.0.1:5000/api/v1/property_collection_search/Person/Height/183cm
    # Anything in the collection "person" with "height" value == 183cm
    if collection_name.title() in list(collections_dictionary.keys()):
        col = db[collection_name.title()].find()
        for doc in col: # for each doc
            doc_keys = [x.lower() for x in doc.keys()]
            if property_name.lower() in doc_keys: # IF PROPERTY IN 
                if str(doc[property_name]) == search_value: 
                    print("succ")
                    return(json.dumps(doc, default=customEncoder))
                else: 
                    return("Error: no "+collection_name.lower()+" with "+property_name.lower()+ " equal to "+search_value)
            else: 
                return("Error: "+property_name+" not a property of "+collection_name)
    else: 
        return("Error: "+collection_name+" not in db")

'''
                                   88                                  
                                   88                ,d                
                                   88                88                
88       88  8b,dPPYba,    ,adPPYb,88  ,adPPYYba,  MM88MMM  ,adPPYba,  
88       88  88P'    "8a  a8"    `Y88  ""     `Y8    88    a8P_____88  
88       88  88       d8  8b       88  ,adPPPPP88    88    8PP"""""""  
"8a,   ,a88  88b,   ,a8"  "8a,   ,d88  88,    ,88    88,   "8b,   ,aa  
 `"YbbdP'Y8  88`YbbdP"'    `"8bbdP"Y8  `"8bbdP"Y8    "Y888  `"Ybbd8"'  
             88                                                        
             88                                                   
'''



'''
         88              88                                  
         88              88                ,d                
         88              88                88                
 ,adPPYb,88   ,adPPYba,  88   ,adPPYba,  MM88MMM  ,adPPYba,  
a8"    `Y88  a8P_____88  88  a8P_____88    88    a8P_____88  
8b       88  8PP"""""""  88  8PP"""""""    88    8PP"""""""  
"8a,   ,d88  "8b,   ,aa  88  "8b,   ,aa    88,   "8b,   ,aa  
 `"8bbdP"Y8   `"Ybbd8"'  88   `"Ybbd8"'    "Y888  `"Ybbd8"'  
'''
# Delete an entry from everywhere
# returns a dictionary ['collection'] = num of items deleted in that collection
@app.route('/api/v1/delete/', methods=['POST', 'DELETE'])
def delete_one():
    if not request.json: 
        abort(400)

    # We are currently itterating through each item in the entire DB. Not ideal
    deleted = {}
    for collection in list(collections_dictionary.keys()):
        try:
            x = db[collection.title()].delete_many(request.json)
            deleted[collection] = x.deleted_count
        except: 
            return("Object you attempt to delete must be in the correct format.")
    return(json.dumps(deleted, default=customEncoder))


#TODO 
# THE REST OF CRUD (but creation first)

app.run() #use_reloader=False, threaded=True