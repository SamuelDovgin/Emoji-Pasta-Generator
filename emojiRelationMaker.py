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
import requests
import stop_words

# python emojiRelationMaker.py

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
# maybe think about limiting the number of pairings you can achieve with just one post. to prevent it from swaying results too drastically
def emoji_mapping(emoji_dict, input_string, max_emoji_len):
    norm_emoji_list = emoji_word_normalizer(input_string, max_emoji_len)
    for i in range(0,len(norm_emoji_list)-1):
        #cleaned_word = norm_emoji_list[i]
        cleaned_word = re.sub('[\W_]+', '', norm_emoji_list[i])
        if not check_emoji_chars(cleaned_word) and check_emoji_chars(norm_emoji_list[i+1]) and cleaned_word != "":
            if cleaned_word in emoji_dict.keys():
                if norm_emoji_list[i+1] in emoji_dict[cleaned_word].keys():
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
    related_words = {}
    for i in input_dictionary.keys():
        current_word_forms = get_word_forms(i)
        for parts_of_speech in current_word_forms.keys():
            for word_form in current_word_forms[parts_of_speech]:
                if word_form not in input_dictionary.keys():
                    secondary_input_dictionary[word_form] = {}
                    #maybe map it to a set with all the words that have a certain word as a word from
                    #then in the next step all that has to be done is find any emojis in the other word forms from the original and add the 
                    #pairings to the emojis and stuff
                    #related_words[word_form] = 
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

def clapping_emoji_remover(input_dictionary):
    clapping_removed_dictionary = copy.deepcopy(input_dictionary)
    for i in clapping_removed_dictionary:
        if "clap" not in i and "applause" not in i:
            for j in clapping_removed_dictionary[i]:
                if "👏" in j:
                    clapping_removed_dictionary[i][j] = 0
    return clapping_removed_dictionary

# select from secondary
# still remove the false from initial mapping and add points to the true ones too?
def emoji_map_editor(input_dictionary, edit_dictionary):
    edited_emoji_map = copy.deepcopy(input_dictionary)
    for i in edit_dictionary.keys():
        #print(i)
        if i in edited_emoji_map.keys():
            for j in edit_dictionary[i].keys():
                # if edit dictionary has false for a certain word emoji pairing set the count value to 0
                if j in edited_emoji_map[i].keys() and not edit_dictionary[i][j]:
                    #print(j)
                    #print(edited_emoji_map[i][j])
                    edited_emoji_map[i][j] = 0
                    #print(edited_emoji_map[i][j])
                # IF IT IS THERE MAYBE ADD SOME POINTS FOR THE TRUE EMOJI BECAUSE IT WAS HUMAN REVIEWED
                # Since this is done twice somehow only do it once?
                # add a param that adds points and only do it on the second run after the nlp adds words?
    return edited_emoji_map

def emoji_probability_maker(input_dictionary, minimum_likelihood, remove_stopwords, minimum_emojis, maximum_emojis, my_stop_words):
    emoji_mapping_dictionary = {}
    for i in input_dictionary.keys():
        emoji_mapping_dictionary[i] = {}
        emojis_to_add = set()
        running_count = 0
        for j in input_dictionary[i].keys():
            running_count += input_dictionary[i][j]
        if running_count == 0:
            continue
        for j in input_dictionary[i].keys():
            if input_dictionary[i][j]/running_count >= minimum_likelihood:
                emojis_to_add.add(j)
                
        #its possible only the stuff below this is necessary? because we can just rely on the top minimum for each word which will be better possibly
        #if it is less than the min then the others in order from most to least can be used?
        if len(emojis_to_add) <=  minimum_emojis:
            if len(input_dictionary[i].keys()) <=  minimum_emojis:
                for j in input_dictionary[i].keys():
                    emojis_to_add.add(j)
            else:
                temp_dictionary = input_dictionary[i]
                temp_dictionary = {k: v for k, v in sorted(temp_dictionary.items(), reverse = True, key=lambda item: item[1])}
                for x in range(0, min(len(temp_dictionary.keys()), minimum_emojis)):
                    emojis_to_add.add(list(temp_dictionary.keys())[x])
        
        temp_add_set = set()
        for emoji_group in emojis_to_add:
            if len(emoji_group) == 1:
                for k in input_dictionary[i].keys():
                    if emoji_group in k and emoji_group+'‍' not in k and '‍'+emoji_group not in k:
                        temp_add_set.add(k)

        emojis_to_add = emojis_to_add | temp_add_set

        new_running_total = 0
        for j in emojis_to_add:
            new_running_total += input_dictionary[i][j]
        for j in emojis_to_add:
            emoji_mapping_dictionary[i][j] = input_dictionary[i][j]/new_running_total

    if remove_stopwords:
        stopwords_no_apost = my_stop_words
        for i in range(0,len(stopwords_no_apost)):
            stopwords_no_apost[i] = stopwords_no_apost[i].replace("\'","")
        for i in stopwords_no_apost:
            if i in emoji_mapping_dictionary.keys():
                emoji_mapping_dictionary[i] = {}
    return emoji_mapping_dictionary

def main():
    #POSTS_DIRECTORY = "reddit_posts/posts/"
    #COMMENTS_DIRECTORY = "reddit_posts/comments/"
    #COMMENT_BODY_ATTRIBUTE_NAME = "comment_body"
    POSTS_DIRECTORY = "push_shift_reddit_posts/posts/"
    COMMENTS_DIRECTORY = "push_shift_reddit_posts/comments/"
    COMMENT_BODY_ATTRIBUTE_NAME = "body"

    my_stop_words = stop_words.my_stop_words

    emoji_map = {}
    max_grouped_emojis = 3
    #prev on .10
    emoji_probability = 0.1
    # if there are none above 5% chance probability
    minimum_emojis = 2
    maximum_emoji = 5
    remove_stopwords = True
    # run through all comments and add to emoji_mapping

    completed_comments = []
    completed_submissions = []

    word_to_check = "snipe"

    directory = os.fsencode(POSTS_DIRECTORY)
    # run the following through a loop
    for file_cur in os.listdir(directory):
        file_name = os.fsdecode(file_cur)
        print(file_name)
        df = pd.read_csv(POSTS_DIRECTORY + file_name)
        df = df.fillna("")
        for idx, i in df.iterrows():
            if i['id'] not in completed_submissions:
                emoji_mapping(emoji_map, i['title'], max_grouped_emojis)
                emoji_mapping(emoji_map, i['body'], max_grouped_emojis)
                completed_submissions.append(i['id'])
        if word_to_check in emoji_map.keys():
            print(emoji_map[word_to_check], str(len(emoji_map.keys())))

    # run the following through a loop
    directory = os.fsencode(COMMENTS_DIRECTORY)
    # run the following through a loop
    for file_cur in os.listdir(directory):
        file_name = os.fsdecode(file_cur)
        print(file_name)
        df = pd.read_csv(COMMENTS_DIRECTORY + file_name)
        df = df.fillna("")
        for idx, i in df.iterrows():
            if i['id'] not in completed_comments:
                emoji_mapping(emoji_map, i[COMMENT_BODY_ATTRIBUTE_NAME], max_grouped_emojis)
                completed_comments.append(i['id'])
        if word_to_check in emoji_map.keys():
            print(emoji_map[word_to_check], str(len(emoji_map.keys())))
    # run prev through a loop

    with open('emoji_mapping_initial.json','w') as fp:
        json.dump(emoji_map, fp)

    emoji_edits_json = requests.get('https://emoji-map-edits.s3.amazonaws.com/emoji_edits.json').text
    emoji_edits = json.loads(emoji_edits_json)
    edited_emoji_map = emoji_map_editor(emoji_map, emoji_edits)

    print(edited_emoji_map[word_to_check], str(len(edited_emoji_map.keys())))

    with open('edited_emoji_mapping.json','w') as fp:
        json.dump(edited_emoji_map, fp)

    # add counts to similar words
    updated_emoji_map = nltk_word_forms_dictionary_refiner(edited_emoji_map)
    print(updated_emoji_map[word_to_check], str(len(updated_emoji_map.keys())))

    removed_clapping = clapping_emoji_remover(updated_emoji_map)
    print(removed_clapping[word_to_check], str(len(removed_clapping.keys())))

    edited_emoji_map2 = emoji_map_editor(removed_clapping, emoji_edits)
    print(edited_emoji_map2[word_to_check], str(len(edited_emoji_map2.keys())))

    with open('emoji_mapping_secondary.json','w') as fp:
        json.dump(edited_emoji_map2, fp)

    #probably save the following as a csv or somehow
    emoji_map_probability = emoji_probability_maker(edited_emoji_map2, emoji_probability, remove_stopwords, minimum_emojis, maximum_emoji, my_stop_words)
    print(emoji_map_probability[word_to_check], str(len(emoji_map_probability.keys())))

    with open('emoji_mapping.json','w') as fp:
        json.dump(emoji_map_probability, fp)

if __name__ == "__main__":
    main()