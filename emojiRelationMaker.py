# Rules
# use up to 3 (non repeating) emojis after a word


# only use top 1/3 of results as chances to end up as emojis after the word

# clone and install this repo
from word_forms.word_forms import get_word_forms
# nltk.download('wordnet')
import pandas as pd
from emoji import UNICODE_EMOJI
import nltk
import re
from nltk.corpus import stopwords
import string
import random
import json
import copy
import os

my_stop_words = ['me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', "you're", "you've", "you'll", 
"you'd", 'yours', 'yourself', 'yourselves', 
'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 
'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 
'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 
'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 
'to', 'from', 'in', 'out', 'on', 'off', 'further', 'would', 'could' ,
'then', 'once', 'here', 'there', 'where', 'how', 'any', 'both', 'each', 'few', 'more', 'most', 
'other', 'some', 'such', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 's', 't', 'can', 
'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 
"aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', 
"haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 
'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', 'wouldn']

"""df = pd.read_csv('topEmojiPasta.csv')
 f = open("output.txt", "wb")
f.write(str(df.loc[0:10]).encode('UTF-8', 'ignore'))
f.close() """

def emoji_list_split(input_string):
    final_string = ""
    # removes all punctuation
    input_string = re.sub(u'\u201c','',input_string)
    input_string = re.sub(u'\u201d','',input_string)
    input_string = re.sub(u'\u201e','',input_string)
    input_string = re.sub(u'\u201f','',input_string)
    input_string = input_string.translate(str.maketrans('', '', string.punctuation)).lower()
    #input_string = re.sub('[\W_]+', '', input_string)
    i = 0
    while i < len(input_string):
        # first make sure we are not repeating i
        # cannot go one by one because that misses emojis that contain more than one
        if input_string[i] in UNICODE_EMOJI:
            #print("INNER loop recognize:" + input_string[i])
            prev_i = i
            # also make sure not to extend past len of string
            for j in range(1,8)[::-1]:
                current_test_end_index = min(i + j, len(input_string))
                #print(current_test_end_index)
                if input_string[i:current_test_end_index] in UNICODE_EMOJI:
                    prev_i = i
                    i = current_test_end_index
                    break
            final_string += " " + input_string[prev_i:i] + " "
            #print("INNER loop add to string:" + input_string[prev_i:i])
        else:
            final_string += input_string[i]
            #print(input_string[i])
            i += 1
    return final_string.split()

def check_emoji_chars(input_string):
    if input_string in UNICODE_EMOJI:
        return True
    for i in emoji_list_split(input_string):
        if i not in UNICODE_EMOJI:
            return False
    return True

def emoji_list_merge(input_list):
    final_list = []
    building_emoji_string = False
    temporary_string = ""
    input_list = list(filter(('️').__ne__, input_list))
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

def restrict_emoji(input_string, max_emojis_count):
    #restict len if above take three most common diff
    count_dict = {}
    for i in emoji_list_split(input_string):
        #print(emoji_list_split(input_string))
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

def emoji_word_normalizer(input_string, max_emoji_len):
    split_emoji_string = emoji_list_split(input_string)
    #print(split_emoji_string)
    merged_emoji_string = emoji_list_merge(split_emoji_string)
    #print(merged_emoji_string)
    for i in range(0,len(merged_emoji_string)):
        if merged_emoji_string[i] != "":
            if check_emoji_chars(merged_emoji_string[i]):
                #print("here!")
                #print(merged_emoji_string[i])
                merged_emoji_string[i] = restrict_emoji(merged_emoji_string[i], max_emoji_len)
    return merged_emoji_string

# returns dictionary with words associated with emojis afterwards (this can be improved with more robust algos)
def emoji_mapping(emoji_dict, input_string, max_emoji_len):
    norm_emoji_list = emoji_word_normalizer(input_string, max_emoji_len)
    for i in range(0,len(norm_emoji_list)-1):
        #cleaned_word = norm_emoji_list[i]
        cleaned_word = re.sub('[\W_]+', '', norm_emoji_list[i])
        if not check_emoji_chars(norm_emoji_list[i]) and check_emoji_chars(norm_emoji_list[i+1]) and cleaned_word != "":
            if norm_emoji_list[i] in emoji_dict.keys():
                if norm_emoji_list[i+1] in emoji_dict[norm_emoji_list[i]].keys():
                    emoji_dict[cleaned_word][norm_emoji_list[i+1]] += 1
                else:
                    emoji_dict[cleaned_word][norm_emoji_list[i+1]] = 1
            else:
                emoji_dict[cleaned_word] = {norm_emoji_list[i+1]:1}
            # all the stuff below can be removed. just adds s to words over length 4 and adds the same emoji to dictionary
            '''
            cleaned_word2 = re.sub('[\W_]+', '', norm_emoji_list[i]+"s")
            if len(cleaned_word2) >= 3:
                if norm_emoji_list[i]+"s" in emoji_dict.keys():
                    if norm_emoji_list[i+1] in emoji_dict[norm_emoji_list[i]+"s"].keys():
                        emoji_dict[cleaned_word2][norm_emoji_list[i+1]] += 1
                    else:
                        emoji_dict[cleaned_word2][norm_emoji_list[i+1]] = 1
                else:
                    emoji_dict[cleaned_word2] = {norm_emoji_list[i+1]:1}
                    '''
    return True

def nltk_word_forms_dictionary_refiner(input_dictionary):
    secondary_input_dictionary = copy.deepcopy(input_dictionary)
    for i in input_dictionary.keys():
        current_word_forms = get_word_forms(i)
        for parts_of_speech in current_word_forms.keys():
            for word_form in current_word_forms[parts_of_speech]:
                if word_form not in input_dictionary.keys():
                    secondary_input_dictionary[word_form] = {}
    update_input_dictionary = copy.deepcopy(secondary_input_dictionary)
    for i in update_input_dictionary.keys():
        current_word_forms = get_word_forms(i)
        for parts_of_speech in current_word_forms:
            catch_repeated_words = [i]
            for word_form in current_word_forms[parts_of_speech]:
                # this is a for loop through all the related words
                if word_form in secondary_input_dictionary.keys() and word_form not in catch_repeated_words:
                    catch_repeated_words.append(word_form)
                    for k in secondary_input_dictionary[word_form].keys():
                        # this forces the keys into a list each time
                        if k in list(update_input_dictionary[i].keys()):
                            update_input_dictionary[i][k] += secondary_input_dictionary[word_form][k]
                        else:
                            update_input_dictionary[i][k] = secondary_input_dictionary[word_form][k]
    return update_input_dictionary


def emoji_probability_maker(input_dictionary, minimum_likelihood, remove_stopwords, minimum_emojis, maximum_emojis):
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
        if len(emoji_mapping_dictionary[i].keys()) == 0:
            if len(input_dictionary[i].keys()) <=  minimum_emojis:
                for j in input_dictionary[i].keys():
                    emoji_mapping_dictionary[i][j] = input_dictionary[i][j]/new_running_count
            else:
                temp_new_running_count = 0
                temp_dictionary = input_dictionary[i]
                temp_dictionary = {k: v for k, v in sorted(temp_dictionary.items(), reverse = True, key=lambda item: item[1])}
                for x in range(0, min(len(temp_dictionary.keys()), minimum_emojis)):
                    temp_new_running_count += temp_dictionary[list(temp_dictionary.keys())[x]]
                for x in range(0, min(len(temp_dictionary.keys()), minimum_emojis)):
                    emoji_mapping_dictionary[i][list(temp_dictionary.keys())[x]] = temp_dictionary[list(temp_dictionary.keys())[x]]/temp_new_running_count

    if remove_stopwords:
        stopwords_no_apost = my_stop_words
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
emoji_probability = 0.15
# if there are none above 5% chance probability
minimum_emojis = 2
maximum_emoji = 5
remove_stopwords = True
# run through all comments and add to emoji_mapping

completed_comments = []
completed_submissions = []

directory = os.fsencode("reddit_posts/posts/")
# run the following through a loop
for file_cur in os.listdir(directory):
    file_name = os.fsdecode(file_cur)
    print(file_name)
    df = pd.read_csv("reddit_posts/posts/" + file_name)
    df = df.fillna("")
    for idx, i in df.iterrows():
        if i['id'] not in completed_submissions:
            emoji_mapping(emoji_map, i['title'], max_grouped_emojis)
            emoji_mapping(emoji_map, i['body'], max_grouped_emojis)
            completed_submissions.append(i['id'])

# run the following through a loop
directory = os.fsencode("reddit_posts/comments/")
# run the following through a loop
for file_cur in os.listdir(directory):
    file_name = os.fsdecode(file_cur)
    print(file_name)
    df = pd.read_csv("reddit_posts/comments/" + file_name)
    df = df.fillna("")
    for idx, i in df.iterrows():
        if i['id'] not in completed_comments:
            emoji_mapping(emoji_map, i['comment_body'], max_grouped_emojis)
            completed_comments.append(i['id'])
# run prev through a loop

with open('emoji_mapping_initial.json','w') as fp:
    json.dump(emoji_map, fp)

# add counts to similar words
updated_emoji_map = nltk_word_forms_dictionary_refiner(emoji_map)

with open('emoji_mapping_secondary.json','w') as fp:
    json.dump(updated_emoji_map, fp)

#probably save the following as a csv or somehow
emoji_map_probability = emoji_probability_maker(updated_emoji_map, emoji_probability, remove_stopwords, minimum_emojis, maximum_emoji)

with open('emoji_mapping.json','w') as fp:
    json.dump(emoji_map_probability, fp)

"""
test_string = "hello i am a cool bee what is my name"
f = open("output.txt", "wb")
f.write(emoji_pasta_maker(test_string,emoji_map_probability).encode('UTF-8', 'ignore')) #.encode('UTF-8', 'ignore') ---- maybe add this back later

f.close()"""