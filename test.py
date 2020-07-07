import requests
import json

x = requests.get('https://emoji-map.s3.amazonaws.com/emoji_mapping.json').text
y = json.loads(x)

print(y['dog'])