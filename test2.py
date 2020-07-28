import json
import string

import boto3

s3 = boto3.client('s3')
bucket = "emoji-map-edits"
key = "emoji_edits.json"
response = s3.get_object(Bucket=bucket, Key=key)
#print(response["Body"].read().decode())

emoji_map_probability = {}
with open('edited_emoji_mapping.json','r', encoding="utf8") as fp:
    emoji_map_probability = json.load(fp)
fp.close()
#print(emoji_map_probability["black"])
#print(emoji_map_probability["offend"])

emoji_map_probability = {}
with open('emoji_mapping_initial.json','r', encoding="utf8") as fp:
    emoji_map_probability = json.load(fp)
fp.close()
print(emoji_map_probability["black"])
#print(emoji_map_probability["offend"])
#print(emoji_map_probability["black"])
print(emoji_map_probability["blacks"])

emoji_map_probability = {}
with open('emoji_mapping_secondary.json','r', encoding="utf8") as fp:
    emoji_map_probability = json.load(fp)
fp.close()
#print(emoji_map_probability["black"])
#print(emoji_map_probability["offend"])
#print(emoji_map_probability["black"])
#print(emoji_map_probability["blacks"])

with open('emoji_mapping.json','r', encoding="utf8") as fp:
    emoji_map_probability = json.load(fp)
fp.close()
#print(emoji_map_probability["black"])
#print(emoji_map_probability["offend"])
#print(emoji_map_probability["black"])
#print(emoji_map_probability["blacks"])

#print('👁'.encode('utf-16','surrogatepass').decode('utf-16'))
#print('👁' == '\ud83d\udc41'.encode('utf-16','surrogatepass').decode('utf-16'))

emoji_map = {"black":{"👁":True,"🙈🍗🅿":False,"💩":False,"🐵":False,"🅱":True,"👱🏿🔫👶🏾":True,"👨🏿":True,"⬛":True,"👱🏿👵🏿👩🏿":True,"🎅🏿":True,"👦🏿":True,"⚫":True,"🙉👮":False,"🙊🙈🙉":False,"🙈🙉🙊":False,"◾▪☑":False}, "garbage":{"👳🏾‍♂️👨🏿↙":False,"😤":True,"🗑":True,"🗑🚮":True,"♻":True}, "offend":{"😫😒":True,"😂😅🤣":True,"🍼👶":True,"👨🏿🐵":False,"😈":True,"✔":False,"💆🏼‍♂️":True,"😨":True,"😤":True,"😠😡":True}}
#print(emoji_map["offend"])
with open('emoji_edits.json','w') as fp:
    json.dump(emoji_map, fp)