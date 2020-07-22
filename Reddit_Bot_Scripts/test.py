import pickle
import pprint
import praw

info = {}
with open("stored_info/info2.txt") as f:
    for line in f:
        (key, val) = line.split()
        info[key] = val
f.close()

reddit = praw.Reddit(client_id = info['appid'],
                    client_secret = info['secret'],
                    user_agent = info['appname'],
                    username = info['username'],
                    password = info['password'])

subreddit = reddit.subreddit("copypasta")
print(subreddit.user_is_banned)
pprint.pprint(vars(subreddit))