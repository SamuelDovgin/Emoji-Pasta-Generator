import praw
import pandas as pd
import sys
import json
import string
import random
import datetime
import requests

import bot_helper_functions as bot

# python inbox_emoji_reddit_bot.py

# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\command_emoji_reddit_bot.py ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\bot_helper_functions.py ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\stored_info\objects_replied_to.pickle ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\stored_info\info2.txt ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user

PROCESSED_OBJECTS_SET = "stored_info/objects_replied_to.pickle"
REDDIT_CREDENTIALS_FILE = "stored_info/info2.txt"
BOT_SUBREDDIT = "all"
COMMAND = "!emojify"
BOT_NAME = "Emojify_Creator"

def process_user_mention(message, emoji_map_probability):
    objects_replied_to = bot.load_object_from_file(PROCESSED_OBJECTS_SET)
    parent_object_type = message.parent_id[:2]
    parent = message.parent()
    print("message.id not in objects_replied_to:", message.id not in objects_replied_to)
    print("parent.id not in objects_replied_to:", parent.id not in objects_replied_to)
    if message.id not in objects_replied_to and parent.id not in objects_replied_to and not bot.check_banned_muted(message.subreddit):
        bot.pretty_print_id_time(message)

        emojified_id_set = None
        
        # below if runs if the object is a submission
        if parent_object_type == "t3":
            if parent.selftext != "":
                emojified_id_set = bot.send_reply(parent.selftext, message, True, emoji_map_probability)
            elif parent.title != "":
                emojified_id_set = bot.send_reply(parent.title, message, True, emoji_map_probability)
        
        # below if runs if the object is a comment
        elif parent_object_type == "t1":
            if(parent.body != ""):
                emojified_id_set = bot.send_reply(parent.body, message, True, emoji_map_probability)
        
        objects_replied_to.add(message.id)
        objects_replied_to.add(parent.id)
        new_objects_replied_to = objects_replied_to | emojified_id_set
        bot.append_object_to_file(PROCESSED_OBJECTS_SET, new_objects_replied_to)

def main():
    reddit = bot.get_reddit_object(REDDIT_CREDENTIALS_FILE)
    subreddit = bot.get_subreddit_object(REDDIT_CREDENTIALS_FILE, BOT_SUBREDDIT)

    emoji_map_probability = bot.get_emoji_map()

    for comment in subreddit.stream.comments():
        if COMMAND in comment.body.lower() and not comment.author.name == BOT_NAME:
            print("found !emojify in comment")
            reddit.redditor("Emojify_Creator").message("!emojify Mentions", comment.permalink)
            process_user_mention(comment, emoji_map_probability)

if __name__ == "__main__":
    main()