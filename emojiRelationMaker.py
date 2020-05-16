# Rules
# use up to 3 (non repeating) emojis after a word


# only use top 1/3 of results as chances to end up as emojis after the word

import pandas as pd
from emoji import UNICODE_EMOJI
import nltk
from nltk.corpus import stopwords
import string
import random
import json

"""df = pd.read_csv('topEmojiPasta.csv')
 f = open("output.txt", "wb")
f.write(str(df.loc[0:10]).encode('UTF-8', 'ignore'))
f.close() """

def check_emoji_chars(input_string):
    for i in input_string:
        if i not in UNICODE_EMOJI:
            return False
    return True

# return list of strings that have all words seperate from emojis. If two emoji strings are in a row that is fine.
# this should also remove all punctuation
def emoji_list_split(input_string):
    final_string = ""
    # removes all punctuation
    input_string = input_string.translate(str.maketrans('', '', string.punctuation)).lower()
    for i in range(0,len(input_string)):
        if input_string[i] in UNICODE_EMOJI:
                final_string += " " + input_string[i] + " "
        else:
            final_string += input_string[i]
    return final_string.split()

# take in list of strings. If two strings in a row are only emojis then merge them in new list to return.
def emoji_list_merge(input_list):
    final_list = []
    building_emoji_string = False
    temporary_string = ""
    for i in input_list:
        if check_emoji_chars(i):
            temporary_string += i
            building_emoji_string = True
        else:
            if building_emoji_string:
                final_list.append(temporary_string)
                building_emoji_string = False
                temporary_string = ""
            final_list.append(i)
    if building_emoji_string:
        final_list.append(temporary_string)
    return final_list

# take in single emoji string and return the first max_emojis_count most common emojis in the input as a string.
def restrict_emoji(input_string, max_emojis_count):
    #restict len if above take three most common diff
    count_dict = {}
    for i in input_string:
        if i not in count_dict.keys():
            count_dict[i] = 1
        else:
            count_dict[i] += 1
    most_common_list = []
    for i in count_dict.keys():
        most_common_list.append((i,count_dict[i]))
    most_common_list = sorted(most_common_list,key=lambda x:x[1],reverse=True)
    if max_emojis_count < len(most_common_list):
        most_common_list = most_common_list[0:max_emojis_count]
    
    restricted_emoji_string = ""

    for i in most_common_list:
        restricted_emoji_string += i[0]
        
    return restricted_emoji_string

# This puts everything together and limits emojis to max lengths
def emoji_word_normalizer(input_string, max_emoji_len):
    split_emoji_string = emoji_list_split(input_string)
    #print(split_emoji_string)
    merged_emoji_string = emoji_list_merge(split_emoji_string)
    #print(merged_emoji_string)
    for i in range(0,len(merged_emoji_string)):
        if check_emoji_chars(merged_emoji_string[i]):
            merged_emoji_string[i] = restrict_emoji(merged_emoji_string[i], max_emoji_len)
    return merged_emoji_string

# returns dictionary with words associated with emojis afterwards (this can be improved with more robust algos)
def emoji_mapping(emoji_dict, input_string, max_emoji_len):
    norm_emoji_list = emoji_word_normalizer(input_string, max_emoji_len)
    for i in range(0,len(norm_emoji_list)-1):
        if not check_emoji_chars(norm_emoji_list[i]) and check_emoji_chars(norm_emoji_list[i+1]):
            if norm_emoji_list[i] in emoji_dict.keys():
                if norm_emoji_list[i+1] in emoji_dict[norm_emoji_list[i]].keys():
                    emoji_dict[norm_emoji_list[i]][norm_emoji_list[i+1]] += 1
                else:
                    emoji_dict[norm_emoji_list[i]][norm_emoji_list[i+1]] = 1
            else:
                emoji_dict[norm_emoji_list[i]] = {norm_emoji_list[i+1]:1}
    return True

def emoji_probability_maker(input_dictionary, minimum_likelihood, remove_stopwords):
    emoji_mapping_dictionary = {}
    for i in input_dictionary.keys():
        emoji_mapping_dictionary[i] = {}
        running_count = 0
        for j in input_dictionary[i].keys():
            running_count += input_dictionary[i][j]
        # now remove emojis below threshold
        new_running_count = 0
        for j in input_dictionary[i].keys():
            if input_dictionary[i][j]/running_count >= minimum_likelihood:
                new_running_count += input_dictionary[i][j]
        for j in input_dictionary[i].keys():
            if input_dictionary[i][j]/running_count >= minimum_likelihood:
                emoji_mapping_dictionary[i][j] = input_dictionary[i][j]/new_running_count
    if remove_stopwords:
        stopwords_no_apost = stopwords.words('english')
        for i in range(0,len(stopwords_no_apost)):
            stopwords_no_apost[i] = stopwords_no_apost[i].replace("\'","")
        for i in stopwords_no_apost:
            if i in emoji_mapping_dictionary.keys():
                emoji_mapping_dictionary[i] = {}
    return emoji_mapping_dictionary

""" temp = {}
f = open("output.txt", "wb")
f.write(emoji_string_split("Heas.df.asd!L@Lo😂😂😂😂😂my😂name😂is😂sam😂hello").encode('UTF-8', 'ignore'))
f.close() """

emoji_map = {}
max_grouped_emojis = 3
#prev on .10
emoji_probability = .05
# run through all comments and add to emoji_mapping

completed_comments = []
completed_submissions = []

# run the following through a loop
for i in ['topEmojiPasta5000.csv', 'hotEmojiPasta5000.csv', 'newEmojiPasta5000.csv', 'controversialEmojiPasta5000.csv']:
    df = pd.read_csv(i)
    df = df.fillna("")
    for idx, i in df.iterrows():
        if i['id'] not in completed_submissions:
            emoji_mapping(emoji_map, i['title'], max_grouped_emojis)
            emoji_mapping(emoji_map, i['body'], max_grouped_emojis)
            completed_submissions.append(i['id'])

# run the following through a loop
for i in ['topEmojiPastaComments5000.csv', 'hotEmojiPastaComments5000.csv', 'newEmojiPastaComments5000.csv', 'controversialEmojiPastaComments5000.csv']:
    df = pd.read_csv(i)
    df = df.fillna("")
    for idx, i in df.iterrows():
        if i['id'] not in completed_comments:
            emoji_mapping(emoji_map, i['comment_body'], max_grouped_emojis)
            completed_comments.append(i['id'])
# run prev through a loop

#probably save the following as a csv or somehow
emoji_map_probability = emoji_probability_maker(emoji_map, emoji_probability, True)

with open('emoji_mapping.json','w') as fp:
    json.dump(emoji_map_probability, fp)

"""
test_string = "hello i am a cool bee what is my name"
f = open("output.txt", "wb")
f.write(emoji_pasta_maker(test_string,emoji_map_probability).encode('UTF-8', 'ignore')) #.encode('UTF-8', 'ignore') ---- maybe add this back later

f.close()"""