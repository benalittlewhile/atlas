import json
exampleThing = {
    'example': 1,
    'bananas': "yes please",
    }

import requests

api_url ="http://localhost:5000/api/v1/create/person"
response = requests.post(api_url, json=exampleThing)
print(response.json)