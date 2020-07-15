import praw
import pprint
info = {}
with open("info2.txt") as f:
    for line in f:
        (key, val) = line.split()
        info[key] = val
f.close()
reddit = praw.Reddit(client_id = info['appid'],
                     client_secret = info['secret'],
                     user_agent = info['appname'],
                     username = info['username'],
                     password = info['password'])

# if item.type == "username_mention"

for item in reddit.inbox.stream():
    if item.type == "username_mention":
        parent_object_type = item.parent_id[:2]
        parent = item.parent()
        if parent_object_type == "t1":
            print(parent.body)
        elif parent_object_type == "t3":
            print(parent.selftext)
