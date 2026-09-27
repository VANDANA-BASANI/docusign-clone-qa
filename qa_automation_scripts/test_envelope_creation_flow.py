import urllib.request
import base64
import json

auth_header = 'Basic ' + base64.b64encode(b'scalerailabs:QA@ScalerAILabs').decode('utf-8')

# Create a test envelope via API to see what fields it creates
req = urllib.request.Request(
    'http://13.207.185.159/api/v1/envelopes',
    headers={'Authorization': auth_header, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    data=b'{}',
    method='POST'
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print("Created test envelope:", data)
    env_id = data.get('id')

# Check get envelope
req2 = urllib.request.Request(
    f'http://13.207.185.159/api/v1/envelopes/{env_id}',
    headers={'Authorization': auth_header, 'User-Agent': 'Mozilla/5.0'}
)
with urllib.request.urlopen(req2) as resp:
    data2 = json.loads(resp.read().decode('utf-8'))
    print("Fetched test envelope details:", data2)
