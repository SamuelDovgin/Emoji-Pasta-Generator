import praw
import pandas as pd
import sys
import json
import string
import random
import datetime
import requests

# python emoji_reddit_bot.py

# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\emoji_reddit_bot.py ec2-user@ec2-3-90-147-253.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\posts_replied_to.txt ec2-user@ec2-3-90-147-253.compute-1.amazonaws.com:/home/ec2-user
# scp -i C:\Users\Temp\Documents\test_key_pair.pem C:\Users\Temp\Developer\Emoji-Pasta-Generator\info2.txt ec2-user@ec2-3-90-147-253.compute-1.amazonaws.com:/home/ec2-user

info = {}
with open("info2.txt") as f:
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

def find_punct_ending_index(input_string):
    punctuation_start = -1
    punctuation_adj = False
    for i in range(0,len(input_string)):
        if input_string[i] in string.punctuation and input_string[i] != "\'":
            if not punctuation_adj:
                punctuation_start = i
            punctuation_adj = True
        else:
            punctuation_start = -1
            punctuation_adj = False
    if punctuation_adj:
        return punctuation_start
    else:
        return None

def emoji_prob_picker(input_string, emoji_map):
    total_prob_counter = 0
    rand_value = random.random()
    if input_string in emoji_map.keys():
        for i in emoji_map[input_string]:
            total_prob_counter += emoji_map[input_string][i]
            if rand_value <= total_prob_counter:
                return i
    return ""

def emoji_pasta_maker(raw_string, emoji_prob_map):
    raw_string_split = raw_string.split()
    normalized_string_list = []
    emoji_list = []
    final_emoji_pasta = ""
    for i in range(0,len(raw_string_split)):
        normalized_string = raw_string_split[i].translate(str.maketrans('', '', string.punctuation)).lower()
        normalized_string_list.append(normalized_string)
    for i in normalized_string_list:
        emoji_list.append(emoji_prob_picker(i,emoji_prob_map))
    for i in range(0,len(raw_string_split)):
        if emoji_list[i] != "":
            punct_starting_index = find_punct_ending_index(raw_string_split[i])
            if punct_starting_index:
                final_emoji_pasta += raw_string_split[i][:punct_starting_index] + " " + emoji_list[i] + raw_string_split[i][punct_starting_index:] + " "
            else:    
                final_emoji_pasta += raw_string_split[i] + " " + emoji_list[i] + " "
        else:
            final_emoji_pasta += raw_string_split[i] + " "
    return final_emoji_pasta

emoji_map_json = requests.get('https://emoji-map.s3.amazonaws.com/emoji_mapping.json').text
emoji_map_probability = json.loads(emoji_map_json)

with open("posts_replied_to.txt", "r") as f:
    posts_replied_to = f.read()
    posts_replied_to = posts_replied_to.split("\n")
    posts_replied_to = list(filter(None, posts_replied_to))

def process_submission(submission):
    if submission.id not in posts_replied_to:
        initial_submission_time_pretty = datetime.datetime.fromtimestamp(
                int(submission.created_utc)
            ).strftime('%Y-%m-%d %H:%M:%S')
        print(submission.id + " " + initial_submission_time_pretty)
        if(submission.selftext != ""):
            content = submission.selftext.split('\n')
            output = ""
            for i in content:
                output += emoji_pasta_maker(i,emoji_map_probability)
                output += '\n'
            if(len(output) > 9800):
                output = output[:9800]
                output += '\n\n'
            else:
                output += '\n'
            output += emoji_pasta_maker("Message the", emoji_map_probability) + "["
            # Below remove a space off of the emojified text (as "Bot" always has an emoji and space after)
            output += emoji_pasta_maker("Emojify Facebook Messenger Bot", emoji_map_probability)[:-1] + "](https://www.messenger.com/t/104121844644171) "
            output += emoji_pasta_maker("to Generate Emoji Pastas Like This!", emoji_map_probability)
            submission.reply(output)
        posts_replied_to.append(submission.id)
        with open("posts_replied_to.txt", "w") as f:
            for post_id in posts_replied_to:
                f.write(post_id + "\n")
        

for submission in subreddit.stream.submissions():
    process_submission(submission)






