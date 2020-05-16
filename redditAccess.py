import praw
import pandas as pd

type_of_post_sort = "hot"

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

count = 5000

top_subreddit = subreddit.hot(limit=count)

#for submission in subreddit.top(limit=1):
#    print(submission.title, submission.id)

topics_dict = {"id":[],"title":[],"body":[]}

pd.DataFrame(topics_dict).to_csv(type_of_post_sort + 'CopyPasta' + str(count) + '.csv', index=False) 

comment_dict = {"id":[], "comment_body":[]}

pd.DataFrame(comment_dict).to_csv(type_of_post_sort + 'CopyPastaComments' + str(count) + '.csv', index=False) 

for submission in top_subreddit:
    topics_dict["title"].append(submission.title)
    topics_dict["id"].append(submission.id)
    topics_dict["body"].append(submission.selftext)

    # convert dictionary to pd
    topics_data = pd.DataFrame(topics_dict)

    # convert pd to append new submission to csv
    topics_data.to_csv(type_of_post_sort + 'CopyPasta' + str(count) + '.csv', mode='a', index=False, header=False) 
    
    # reset dictionary
    topics_dict = {"id":[],"title":[],"body":[]}

    submission.comment_sort = "top"
    for top_comments in submission.comments:
        try:
            comment_dict["comment_body"].append(top_comments.body)
            comment_dict["id"].append(top_comments.id)
            comment_dict = pd.DataFrame(comment_dict)
            comment_dict.to_csv(type_of_post_sort + 'CopyPastaComments' + str(count) + '.csv', mode='a', index=False, header=False) 
            comment_dict = {"id":[], "comment_body":[]}
        except AttributeError:
            print("error :( on comment")






