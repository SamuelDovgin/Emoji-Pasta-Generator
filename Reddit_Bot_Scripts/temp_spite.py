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

# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\temp_spite.py ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\bot_helper_functions.py ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\stored_info\objects_replied_to.pickle ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\Reddit_Bot_Scripts\stored_info\info2.txt ec2-user@ec2-35-171-88-15.compute-1.amazonaws.com:/home/ec2-user

PROCESSED_OBJECTS_SET = "stored_info/objects_replied_to.pickle"
REDDIT_CREDENTIALS_FILE = "stored_info/info2.txt"
BOT_SUBREDDIT = "copypasta"
REPLY_USER = "Fuck_Emojify_Creator"

FIRST_MSG = "Hello, just a friendly reminder that you did the same thing as Cummy and didn't get banned for it, you should be ashamed.".lower()
SECOND_MSG = "Hello, just a friendly reminder that nobody will ever forget what you've done to Cummy.".lower()
THRID_MSG = "Hello, just a friendly reminder that you committed several crimes against humanity, you have no rights to speak.".lower()
FOURTH_MSG = "Hello, just a friendly reminder that you're as useless as a broken white crayon and nobody likes you.".lower()

FOURTH_REPLY = "If you want to inform me of something (like how it sounds in your reply), just shoot me a message. Otherwise you should replace *you're as* with *Emojify_Creator is as* to make more sense. Because you are speaking to Redditors who will read your reply on a public form you should direct what you say towards that audience. Right not it doesn't make sense and has bad grammar. Cheers!"
FIRST_REPLY = "I don't need a reminder, and if you want to tell me something, message or chat directly. If you are trying to inform Redditors of something I \"did\" you should refer to me as Emojify_Creator in your statement. e.g., \"reminder that **Emojify_Creator** did the same ... **Emojify_Creator** should be ashamed.\" Otherwise the grammar doesn't really make sense. Cheers!"
SECOND_REPLY = "If you want to inform me of something (like how it sounds in your reply), just shoot me a message. Otherwise you should replace *you've done* with *Emojify_Creator did* to make more sense. Because you are speaking to Redditors who will read your reply on a public form you should direct what you say towards that audience. Right not it doesn't make sense and has bad grammar. Cheers!"
THRID_REPLY = "Send me a message if you want to let me know something. Otherwise refer to me as **Emojify_Creator** so this way you are letting Redditors know something rather than me being the audience of what you said (currently the wording is confusing). Additionally the commonly accepted phrase is \"you have no **right** to speak/talk,\" using *rights* is bad grammar. Cheers!"

def process_rude_comment(comment, objects_replied_to, emoji_map_probability):
    if comment.id not in objects_replied_to:
        bot.pretty_print_id_time(comment)
        print(comment.body)
        if FIRST_MSG in comment.body.lower():
            bot.send_reply(FIRST_REPLY, comment, True, emoji_map_probability)
            objects_replied_to.add(comment.id)
            bot.append_object_to_file(PROCESSED_OBJECTS_SET, objects_replied_to)
        elif SECOND_MSG in comment.body.lower():
            bot.send_reply(SECOND_REPLY, comment, True, emoji_map_probability)
            objects_replied_to.add(comment.id)
            bot.append_object_to_file(PROCESSED_OBJECTS_SET, objects_replied_to)
        elif THRID_MSG in comment.body.lower():
            bot.send_reply(THRID_REPLY, comment, True, emoji_map_probability)
            objects_replied_to.add(comment.id)
            bot.append_object_to_file(PROCESSED_OBJECTS_SET, objects_replied_to)
        elif FOURTH_MSG in comment.body.lower():
            bot.send_reply(THRID_REPLY, comment, True, emoji_map_probability)
            objects_replied_to.add(comment.id)
            bot.append_object_to_file(PROCESSED_OBJECTS_SET, objects_replied_to)
                

def main():
    subreddit = bot.get_subreddit_object(REDDIT_CREDENTIALS_FILE, BOT_SUBREDDIT)

    emoji_map_probability = bot.get_emoji_map()

    object_replied_set = bot.load_object_from_file(PROCESSED_OBJECTS_SET)

    for comment in subreddit.stream.comments():
        print(comment.body)
        if comment.author.name == REPLY_USER:
            process_rude_comment(comment, object_replied_set, emoji_map_probability)

if __name__ == "__main__":
    main()