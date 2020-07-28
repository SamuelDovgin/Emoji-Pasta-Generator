#https://api.pushshift.io/reddit/comment/search?ids=
#https://api.pushshift.io/reddit/submission/comment_ids/btm2kc
#"author": "AutoModerator",
#"author": "CummyBot2000",
import pandas as pd
import sys
from datetime import datetime
import requests
import time
import json
import time
import pickle

with open("submission_ids.pickle", "rb") as f:
    push_shift_reddit_submissions = pickle.load(f)

POSTS_PER_FILE = 1000
current_file_post = 0
starting_post = 0

topics_dict = {"id":[],"body":[],"score":[]}

comment_ids_url = 'https://api.pushshift.io/reddit/submission/comment_ids/'
comments_url = "https://api.pushshift.io/reddit/comment/search?ids="

current_post_file = "comments/" + 'EmojiPasta' + str(current_file_post) + '.csv'
pd.DataFrame(topics_dict).to_csv(current_post_file, index=False)

comment_ids_list = []

for idx, submission in enumerate(push_shift_reddit_submissions):
    if submission[1] > 5:
        print("current submission:", submission[0], ", number completed:", str(starting_post))
        comment_ids_json = requests.get(comment_ids_url + submission[0])
        print("comment_ids_json:", comment_ids_json.status_code)
        while comment_ids_json.status_code != 200:
            print("sleeping for 5 because bad status code")
            time.sleep(5)
            comment_ids_json = requests.get(comment_ids_url + submission[0])
        comment_ids_list += comment_ids_json.json()["data"]
        
        print("current_idx:", idx)
        if len(comment_ids_list) < 200 and idx != len(push_shift_reddit_submissions) - 1:
            continue

        #split list into list of lists each with max size 100
        MAX_COMMENTS_PER_REQUEST = 100
        list_of_lists_comment_ids = [comment_ids_list[i:i + MAX_COMMENTS_PER_REQUEST] for i in range(0, len(comment_ids_list), MAX_COMMENTS_PER_REQUEST)]  
        print(list_of_lists_comment_ids)

        comment_ids_list = []

        for j in list_of_lists_comment_ids:
            comments_json = requests.get(comments_url + ','.join(j))
            print("comments_json:", comments_json.status_code)
            while comments_json.status_code != 200:
                print("sleeping for 5 because bad status code")
                time.sleep(5)
                comments_json = requests.get(comments_url + ','.join(j))
            comments_json_list = comments_json.json()["data"]

            if len(comments_json_list) == 0:
                continue
            
            for i in comments_json_list:
                if i.get("author", "") == "AutoModerator" or i.get("author", "") == "CummyBot2000":
                    continue
                topics_dict["id"].append(i.get("id", ""))
                topics_dict["body"].append(i.get("body", ""))
                topics_dict["score"].append(i.get("score", ""))

                # convert dictionary to pd
                topics_data = pd.DataFrame(topics_dict)

                # convert pd to append new submission to csv
                topics_data.to_csv(current_post_file, mode='a', index=False, header=False) 
                
                # reset dictionary
                topics_dict = {"id":[],"body":[],"score":[]}

            starting_post += len(comments_json_list)

            if starting_post > current_file_post + POSTS_PER_FILE:
                current_file_post = current_file_post + POSTS_PER_FILE

                print("new file submission count:" + str(current_file_post))
                #make new file now

                current_post_file = "comments/" + 'EmojiPasta' + str(current_file_post) + '.csv'
                pd.DataFrame(topics_dict).to_csv(current_post_file, index=False)