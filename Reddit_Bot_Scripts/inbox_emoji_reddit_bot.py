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
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\stored_info\objects_replied_to.txt ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\stored_info\info2.txt ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user

def process_user_mention(message, objects_replied_to, emoji_map_probability):
    if message.id not in objects_replied_to:
        bot.pretty_print_id_time(message)
        
        parent_object_type = message.parent_id[:2]
        parent = message.parent()
        
        # below if runs if the object is a submission
        if parent_object_type == "t3":
            if parent.selftext != "":
                bot.send_reply(parent.selftext, message, True, emoji_map_probability)
            elif parent.title != "":
                bot.send_reply(parent.title, message, True, emoji_map_probability)
            objects_replied_to.append(message.id)
            bot.write_object_to_file("stored_info/objects_replied_to.txt", objects_replied_to)
        
        # below if runs if the object is a comment
        elif parent_object_type == "t1":
            if(parent.body != ""):
                bot.send_reply(parent.body, message, True, emoji_map_probability)
            objects_replied_to.append(message.id)
            bot.write_object_to_file("stored_info/objects_replied_to.txt", objects_replied_to)

def process_message(message, objects_replied_to, emoji_map_probability):
    if message.id not in objects_replied_to:
        bot.pretty_print_id_time(message)
        if(message.body != ""):
            bot.send_reply(message.body, message, False, emoji_map_probability)
        objects_replied_to.append(message.id)
        bot.write_object_to_file("stored_info/objects_replied_to.txt", objects_replied_to)

def main():
    reddit = bot.get_reddit_object("stored_info/info2.txt")

    emoji_map_probability = bot.get_emoji_map()

    with open("stored_info/objects_replied_to.txt", "r") as f:
        objects_replied_to = f.read()
        objects_replied_to = objects_replied_to.split("\n")
        objects_replied_to = list(filter(None, objects_replied_to))

    for message in reddit.inbox.stream():
        if(not message.was_comment):
            process_message(message, objects_replied_to, emoji_map_probability)
        elif message.was_comment and message.type == "username_mention":
            process_user_mention(message, objects_replied_to, emoji_map_probability)

if __name__ == "__main__":
    main()