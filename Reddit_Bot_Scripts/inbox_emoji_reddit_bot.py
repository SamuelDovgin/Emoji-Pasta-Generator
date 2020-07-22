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

# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\inbox_emoji_reddit_bot.py ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\bot_helper_functions.py ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\stored_info\objects_replied_to.pickle ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\stored_info\info2.txt ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user

PROCESSED_OBJECTS_SET = "stored_info/objects_replied_to.pickle"
REDDIT_CREDENTIALS_FILE = "stored_info/info2.txt"
BOT_SUBREDDIT = "copypasta"
USERNAME = "u/emojify_creator"

def process_user_mention(message, objects_replied_to, emoji_map_probability):
    if message.id not in objects_replied_to and not bot.check_banned_muted(message.subreddit):
        print("user_mention: ", end="")
        bot.pretty_print_id_time(message)
        
        parent_object_type = message.parent_id[:2]
        parent = message.parent()
        
        # below if runs if the object is a submission
        if parent_object_type == "t3":
            if parent.selftext != "":
                bot.send_reply(parent.selftext, message, True, emoji_map_probability)
            elif parent.title != "":
                bot.send_reply(parent.title, message, True, emoji_map_probability)
            objects_replied_to.add(message.id)
            bot.append_object_to_file(PROCESSED_OBJECTS_SET, objects_replied_to)
        
        # below if runs if the object is a comment
        elif parent_object_type == "t1":
            if(parent.body != ""):
                bot.send_reply(parent.body, message, True, emoji_map_probability)
            objects_replied_to.add(message.id)
            bot.append_object_to_file(PROCESSED_OBJECTS_SET, objects_replied_to)

def process_message(message, objects_replied_to, emoji_map_probability):
    if message.id not in objects_replied_to:
        if message.subreddit != None:
            if bot.check_banned_muted(message.subreddit):
                return
        print("direct message: ", end="")
        bot.pretty_print_id_time(message)
        if(message.body != ""):
            bot.send_reply(message.body, message, False, emoji_map_probability)
        objects_replied_to.add(message.id)
        bot.append_object_to_file(PROCESSED_OBJECTS_SET, objects_replied_to)

def main():
    reddit = bot.get_reddit_object(REDDIT_CREDENTIALS_FILE)

    emoji_map_probability = bot.get_emoji_map()

    object_replied_set = bot.load_object_from_file(PROCESSED_OBJECTS_SET)

    for message in reddit.inbox.stream():
        if(not message.was_comment):
            process_message(message, object_replied_set, emoji_map_probability)
        elif message.type == "username_mention":
            process_user_mention(message, object_replied_set, emoji_map_probability)
        elif message.type == "comment_reply":
            #maybe here a parent parent could be done?
            if USERNAME in message.body.lower():
                process_user_mention(message, object_replied_set, emoji_map_probability)

if __name__ == "__main__":
    main()