import praw
import pandas as pd
import sys

# python emoji_reddit_bot.py

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

subreddit = reddit.subreddit('copypasta')

def process_submission(submission):
    print(submission.title)
    print()
    print(submission.selftext)
    print()

for submission in subreddit.stream.submissions():
    process_submission(submission)






