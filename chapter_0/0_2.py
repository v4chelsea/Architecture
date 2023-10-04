import json
from urllib.request import urlopen
from urllib.parse import urlencode

params = dict(q="Sausages", format="json")
handle = urlopen('http://api.duckduckgo.com' + '?' + urlencode(params))
raw_text = handle.read().decode('utf8')
parsed = json.loads(raw_text)

resutls = parsed['RelatedTopics']

for r in resutls:
    if "Text" in r:
        print(r['FirstURL'] + " - " + r['Text'])

print(" ================================================= ")


import requests

params = dict(q='Sausages',format='json')
parsed = requests.get('http://api.duckduckgo.com/', params=params).json()
results = parsed['RelatedTopics']
                 
for r in results:
    if 'Text' in r:
        print(r['FirstURL'] + " - " + r['Text'])