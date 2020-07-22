import json
import string

emoji_map_probability = {}
with open('emoji_mapping_secondary.json','r', encoding="utf8") as fp:
    emoji_map_probability = json.load(fp)
fp.close()
#print(emoji_map_probability["black"])

#print('👁'.encode('utf-16','surrogatepass').decode('utf-16'))
#print('👁' == '\ud83d\udc41'.encode('utf-16','surrogatepass').decode('utf-16'))


emoji_map = {"hello":{"👁":True,"🙈🍗🅿":False,"💩":False,"🐵":False,"🅱":True,"👱🏿🔫👶🏾":True,"👨🏿":True,"⬛":True,"👱🏿👵🏿👩🏿":True,"🎅🏿":True,"👦🏿":True,"⚫":True,"🙉👮":False,"🙊🙈🙉":False,"🙈🙉🙊":False,"◾▪☑":False}, "garbage":{"👳🏾‍♂️👨🏿↙":False,"😤":True,"🗑":True,"🗑🚮":True,"♻":True}}
with open('emoji_edits.json','w') as fp:
    json.dump(emoji_map, fp)