import praw
import pandas as pd
import sys
import json
import string
import random
import datetime
import requests

import bot_helper_functions as bot

# python emoji_reddit_bot.py

# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\emoji_reddit_bot.py ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\bot_helper_functions.py ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\stored_info\objects_replied_to.pickle ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\stored_info\info2.txt ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user

PROCESSED_OBJECTS_SET = "stored_info/objects_replied_to.pickle"
REDDIT_CREDENTIALS_FILE = "stored_info/info2.txt"
BOT_SUBREDDIT = 'copypasta'

def process_submission(submission, objects_replied_to, emoji_map_probability):
    if submission.id not in objects_replied_to:
        bot.pretty_print_id_time(submission)
        if submission.selftext != "":
            bot.send_reply(submission.selftext, submission, True, emoji_map_probability)
        elif submission.title != "":
            bot.send_reply(submission.title, submission, True, emoji_map_probability)
        objects_replied_to.add(submission.id)
        bot.append_object_to_file(PROCESSED_OBJECTS_SET, objects_replied_to)

def main():
    emoji_map_probability = bot.get_emoji_map()

    subreddit = bot.get_subreddit_object(REDDIT_CREDENTIALS_FILE, BOT_SUBREDDIT)

    object_replied_set = bot.load_object_from_file(PROCESSED_OBJECTS_SET)

    for submission in subreddit.stream.submissions():
        process_submission(submission, object_replied_set, emoji_map_probability)

if __name__ == "__main__":
    main()





