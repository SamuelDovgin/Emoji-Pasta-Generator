import praw
import pprint
info = {}
with open("info.txt") as f:
    for line in f:
        (key, val) = line.split()
        info[key] = val
f.close()
reddit = praw.Reddit(client_id = info['appid'],
                     client_secret = info['secret'],
                     user_agent = info['appname'],
                     username = info['username'],
                     password = info['password'])



#print(reddit.submission("hsnp8v").selftext.replace("&#x200B;", ''))
temp = '👨'
temp2 = '👨👨🙈'
print(temp in temp2 and temp+'‍' not in temp2)
print(temp+'‍' not in temp2)
