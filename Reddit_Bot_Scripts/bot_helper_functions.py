import praw
import pandas as pd
import sys
import json
import string
import random
import datetime
import requests

MAX_COMMENT_LEN = 10000
# FIX THIS TO HAVE EMOJI MAP LOADED HERE TBH MAYBE?
# MAYBE ALSO SEND AN INITIAL MESSAGE TO MESSAGERS SO YOU DONT HAVE TO REPEATEDLY SEND MORE LINKS 

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

def link_reply(reply_object, emoji_map_probability):
    output_string = ""
    output_string += emoji_pasta_maker("Comment Emojify's ", emoji_map_probability)  + "username: "
    output_string += emoji_pasta_maker("\"u/Emojify_Creator\" on any post or reply, message ", emoji_map_probability) + "["
    output_string += emoji_pasta_maker("u/Emojify_Creator directly", emoji_map_probability)[:-1] + "](https://www.reddit.com/message/compose/?to=Emojify_Creator), "
    output_string += emoji_pasta_maker("or chat with the ", emoji_map_probability) + "["
    # Below remove a space off of the emojified text (as "Bot" always has an emoji and space after)
    output_string += emoji_pasta_maker("Emojify Facebook Messenger Bot", emoji_map_probability)[:-1] + "](https://www.messenger.com/t/104121844644171) "
    output_string += emoji_pasta_maker("to Generate Emoji Pastas Like This!", emoji_map_probability)
    reply_object.reply(output_string)

def get_reddit_object(login_info_location):
    info = {}
    with open(login_info_location) as f:
        for line in f:
            (key, val) = line.split()
            info[key] = val
    f.close()

    reddit = praw.Reddit(client_id = info['appid'],
                        client_secret = info['secret'],
                        user_agent = info['appname'],
                        username = info['username'],
                        password = info['password'])
    return reddit

def get_subreddit_object(login_info_location, subreddit_name):
    reddit = get_reddit_object(login_info_location)
    subreddit = reddit.subreddit(subreddit_name)
    return subreddit

def get_emoji_map():
    emoji_map_json = requests.get('https://emoji-map.s3.amazonaws.com/emoji_mapping.json').text
    emoji_map_probability = json.loads(emoji_map_json)
    return emoji_map_probability

# function that takes: text, initial reply object, if message vs post, and then sends requests for it

# is_comment vs is_message
def send_reply(text, initial_reply_object, is_comment, emoji_map_probability):
    content = text.split('\n')
    output = ""
    for idx, val in enumerate(content):
        output += emoji_pasta_maker(val, emoji_map_probability)
        if idx != len(content) - 1:
            output += '\n'
    if len(output) > MAX_COMMENT_LEN:
        starting_idx = 0
        prev_comment_object = initial_reply_object
        sent_initial_reply = False
        while starting_idx < len(output):
            comment_object = prev_comment_object.reply(output[starting_idx:starting_idx+MAX_COMMENT_LEN])
            if is_comment:
                prev_comment_object = comment_object
            if not sent_initial_reply and is_comment:
                link_reply(prev_comment_object, emoji_map_probability)
                sent_initial_reply = True
            starting_idx += MAX_COMMENT_LEN
    else:
        comment_object = initial_reply_object.reply(output)
        if is_comment:
            link_reply(comment_object, emoji_map_probability)

def pretty_print_id_time(object_input):
    initial_submission_time_pretty = datetime.datetime.fromtimestamp(
            int(object_input.created_utc)
        ).strftime('%Y-%m-%d %H:%M:%S')
    print(object_input.id + " " + initial_submission_time_pretty)

def write_object_to_file(file_path, object_to_write):
    with open(file_path, "w") as f:
        for post_id in object_to_write:
            f.write(post_id + "\n")