import flask
from flask import request, jsonify, abort
from pymongo import MongoClient
import json 
from bson.objectid import ObjectId

# Set up flask 
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# set up the database access
client = MongoClient("mongodb+srv://admin:atlasadmin1@cluster0.cwe5c.mongodb.net/test")
db=client['Hesparia']
all_collections = db.list_collection_names() #TODO remove and consolodate with collections_dictionary
collections_dictionary = {}
for x in db.list_collection_names(): 
    for y in db[x].find({}): 
        collections_dictionary[x] = list(y.keys())
print(collections_dictionary)

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
    #print(collection_name)
    # print(type(request.json))
    if not request.json: 
        abort(400)
    if collection_name.title() in all_collections: #TODO
        #print("succ")
        col=db[collection_name.title()]
        x = col.insert_one(request.json)
        return(json.dumps(x.inserted_id, default=customEncoder))
    #print('no')
    return("no")
    #return(request.json)


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
# Get all docs of a given collection
@app.route('/api/v1/<collection_name>/all/', methods=['GET'])
def get_all(collection_name):
    if collection_name.title() in all_collections: #TODO
        col=db[collection_name.title()].find()
        list_of_docs=[]
        for doc in col: 
            list_of_docs.append(doc)
        return json.dumps(list_of_docs, default=customEncoder)
    else: 
        return("Error: "+collection_name+" not in db")


#TODO
# @app.route('/api/v1/property_search/<property_name>/<search_value>/', methods=['GET'])
# def propertysearch(property_name, search_value):
# http://127.0.0.1:5000/api/v1/propertysearch/name/Kobe
# anything anywhere with name "Kobe"


@app.route('/api/v1/property_collection_search/<collection_name>/<property_name>/<search_value>/', methods=['GET'])
def property_search(collection_name, property_name, search_value):
    # Example: 
    # http://127.0.0.1:5000/api/v1/property_collection_search/Person/Height/183cm
    # Anything in the collection "person" with "height" value == 183cm
    if collection_name.title() in all_collections: # TODO
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



# # unused
# @app.route('/api/v1/person/', methods=['GET'])
# def api_id():
#     # Check if an ID was provided as part of the URL.
#     # If ID is provided, assign it to a variable.
#     # If no ID is provided, display an error in the browser.
#     if 'id' in request.args:
#         id = int(request.args['id'])
#     else:
#         return "Error: No id field provided. Please specify an id."

#     # Create an empty list for our results
#     results = []

#     # Loop through the data and match results that fit the requested ID.
#     # IDs are unique, but other fields might return many results
#     for book in books:
#         if book['id'] == id:
#             results.append(book)

#     # Use the jsonify function from Flask to convert our list of
#     # Python dictionaries to the JSON format.
#     return jsonify(results)

app.run() #use_reloader=False, threaded=True

