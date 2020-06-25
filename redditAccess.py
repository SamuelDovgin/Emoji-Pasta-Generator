import praw
import pandas as pd
import sys
from datetime import datetime

now = datetime.now()

type_of_post_sort = sys.argv[1]
count = int(sys.argv[2])

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

subreddit = reddit.subreddit('emojipasta')

reddit_instances = None

if type_of_post_sort == "hot":
    reddit_instances = subreddit.hot(limit=count)
elif type_of_post_sort == "top":
    reddit_instances = subreddit.top(limit=count)
elif type_of_post_sort == "new":
    reddit_instances = subreddit.new(limit=count)



#for submission in subreddit.top(limit=1):
#    print(submission.title, submission.id)

topics_dict = {"id":[],"title":[],"body":[]}

current_post_file = "reddit_posts/posts/" + type_of_post_sort + 'EmojiPasta' + str(count) + "_" + now.strftime("%Y-%m-%d-%H-%M") + '.csv'
pd.DataFrame(topics_dict).to_csv(current_post_file, index=False) 

comment_dict = {"id":[], "comment_body":[]}

current_comment_file = "reddit_posts/comments/" + type_of_post_sort + 'EmojiPastaComments' + str(count) + "_" + now.strftime("%Y-%m-%d-%H-%M") + '.csv'
pd.DataFrame(comment_dict).to_csv(current_comment_file, index=False) 

for submission in reddit_instances:
    topics_dict["title"].append(submission.title)
    topics_dict["id"].append(submission.id)
    topics_dict["body"].append(submission.selftext)

    # convert dictionary to pd
    topics_data = pd.DataFrame(topics_dict)

    # convert pd to append new submission to csv
    topics_data.to_csv(current_post_file, mode='a', index=False, header=False) 
    
    # reset dictionary
    topics_dict = {"id":[],"title":[],"body":[]}

    submission.comment_sort = "top"
    for top_comments in submission.comments:
        try:
            comment_dict["comment_body"].append(top_comments.body)
            comment_dict["id"].append(top_comments.id)
            comment_dict = pd.DataFrame(comment_dict)
            comment_dict.to_csv(current_comment_file, mode='a', index=False, header=False) 
            comment_dict = {"id":[], "comment_body":[]}
        except AttributeError:
            print("error :( on comment")






