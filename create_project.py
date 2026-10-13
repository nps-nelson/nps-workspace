import requests

TOKEN = '11aa6d7b-f5bc-49a7-ac4a-ce73b755150b'
headers = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
query = 'mutation { projectCreate(input: { name: "meta-agent-v1" }) { id name } }'
r = requests.post('https://backboard.railway.app/graphql/v2', json={'query': query}, headers=headers)
print('Project Create Response:', r.status_code, r.text)
