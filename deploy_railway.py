import os
import requests

TOKEN = '11aa6d7b-f5bc-49a7-ac4a-ce73b755150b'
headers = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

# Test d'authentification
query_user = '{"query": "{ me { name email } }"}'
resp = requests.post('https://backboard.railway.com/graphql/v2', headers=headers, data=query_user)
print('Auth response:', resp.status_code, resp.text)
