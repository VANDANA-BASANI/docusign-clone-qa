import urllib.request
import base64
import re
from html.parser import HTMLParser

url = 'http://13.207.185.159/send/home'
auth_header = 'Basic ' + base64.b64encode(b'scalerailabs:QA@ScalerAILabs').decode('utf-8')
req = urllib.request.Request(url, headers={'Authorization': auth_header, 'User-Agent': 'Mozilla/5.0'})

with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Extract links
links = re.findall(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', html, re.DOTALL)
print("=== LINKS ===")
for href, content in links:
    clean_text = re.sub(r'<[^>]+>', '', content).strip()
    print(f"Text: '{clean_text}' -> Href: '{href}'")

# Extract buttons
buttons = re.findall(r'<button[^>]*>(.*?)</button>', html, re.DOTALL)
print("\n=== BUTTONS ===")
for b in buttons:
    clean_b = re.sub(r'<[^>]+>', '', b).strip()
    if clean_b:
        print(f"Button: '{clean_b}'")

# Extract headings and inputs
inputs = re.findall(r'<input[^>]*>', html)
print("\n=== INPUTS ===")
for inp in inputs[:10]:
    print(inp)
