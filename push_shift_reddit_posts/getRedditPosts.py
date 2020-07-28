import pandas as pd
import sys
from datetime import datetime
import requests
import time
import json
import time

""" topics_dict = {"id":[],"title":[],"body":[]}

current_post_file = "reddit_posts/posts/" + type_of_post_sort + 'EmojiPasta' + str(count) + "_" + now.strftime("%Y-%m-%d-%H-%M") + '.csv'
pd.DataFrame(topics_dict).to_csv(current_post_file, index=False)  """

#https://api.pushshift.io/reddit/search/submission/?subreddit=learnpython&sort=desc&sort_type=created_utc&af1
# by year 31536000
# by approx month (year/12) 2628000

current_url = 'https://api.pushshift.io/reddit/search/submission/?subreddit=emojipasta&sort=desc&sort_type=created_utc&size=500&before='

MONTH_UNIX = 2628000
current_time = int(time.time())
current_month_starting_time = current_time
current_unix_time = current_time

#edited_emoji_map = emoji_map_editor(emoji_map, emoji_edits)

topics_dict = {"id":[],"title":[],"body":[],"score":[]}

current_post_file = "posts/" + 'EmojiPasta' + str(current_month_starting_time) + '.csv'
pd.DataFrame(topics_dict).to_csv(current_post_file, index=False)

while True:
    print("current_time:" + str(current_unix_time))

    emojipasta_json = requests.get(current_url + str(current_unix_time))
    print(emojipasta_json.status_code)
    while emojipasta_json.status_code != 200:
        print("sleeping for 5 because bad status code")
        time.sleep(5)
        emojipasta_json = requests.get(current_url + str(current_unix_time))
    emojipasta_dict = emojipasta_json.json()
    current_data = emojipasta_dict["data"]

    if len(current_data) == 0:
        break
    
    for i in current_data:
        topics_dict["title"].append(i.get("title", ""))
        topics_dict["id"].append(i.get("id", ""))
        topics_dict["body"].append(i.get("selftext", ""))
        topics_dict["score"].append(i.get("score", ""))

        # convert dictionary to pd
        topics_data = pd.DataFrame(topics_dict)

        # convert pd to append new submission to csv
        topics_data.to_csv(current_post_file, mode='a', index=False, header=False) 
        
        # reset dictionary
        topics_dict = {"id":[],"title":[],"body":[],"score":[]}

    last_utc_time = current_data[len(current_data) - 1]["created_utc"]

    if last_utc_time < current_month_starting_time - MONTH_UNIX:
        current_month_starting_time = current_month_starting_time - MONTH_UNIX

        print("new file with month:" + str(current_month_starting_time))
        #make new file now

        current_post_file = "posts/" + 'EmojiPasta' + str(current_month_starting_time) + '.csv'
        pd.DataFrame(topics_dict).to_csv(current_post_file, index=False)
    
    current_unix_time = last_utc_time
    