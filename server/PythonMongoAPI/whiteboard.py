import json
examplePerson1 = {
    'name': "john mulaney",
    'age': 39,
    'height': 183,
    'nationality': "U.S.A.", # this will likely be an enum
    'faction': "What's New Pussycat", # also likely enum
    'orgPosition': "On the bench",
    'job': "stand-up comedian",
}

examplePerson2 = {
    'name': "john mulaney",
    'age': 39,
    'height': 183,
    'nationality': "U.S.A.", # this will likely be an enum
    'faction': "What's New Pussycat", # also likely enum
    'orgPosition': "On the bench",
    'job': "stand-up comedian",
}

import requests


api_url ="http://localhost:5000/api/v1/create/Person/"
response = requests.post(api_url, json=examplePerson1)
print(response.json())

api_url ="http://localhost:5000/api/v1/create/Person/"
response = requests.post(api_url, json=examplePerson1)
print(response.json())

api_url ="http://localhost:5000/api/v1/create/Person/"
response = requests.post(api_url, json=examplePerson2)
print(response.json())

api_url = "http://localhost:5000/api/v1/Person/all/"
response = requests.get(api_url)
print(response.json())

api_url ="http://localhost:5000/api/v1/delete/"
response = requests.post(api_url, json=examplePerson1)

print(response.json())

api_url = "http://localhost:5000/api/v1/Person/all/"
response = requests.get(api_url)
print(response.json())