import urllib.request
import base64
import json

auth_header = 'Basic ' + base64.b64encode(b'scalerailabs:QA@ScalerAILabs').decode('utf-8')

def get_api(endpoint):
    url = f'http://13.207.185.159{endpoint}'
    req = urllib.request.Request(url, headers={'Authorization': auth_header, 'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read().decode('utf-8', errors='ignore')
            return json.loads(data)
    except Exception as e:
        return {"error": str(e)}

envelopes = get_api('/api/v1/envelopes?view=inbox&page_size=10')
print("=== INBOX ENVELOPES ===")
print(json.dumps(envelopes, indent=2)[:1500])

all_docs = get_api('/api/v1/envelopes')
print("=== ALL ENVELOPES ===")
print(json.dumps(all_docs, indent=2)[:1500])
