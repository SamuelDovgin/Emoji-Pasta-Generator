import json
import string
import random

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

emoji_map_probability = {}
with open('emoji_mapping.json','r', encoding="utf8") as fp:
    emoji_map_probability = json.load(fp)
fp.close()

content = []
with open("input.txt", encoding="utf8") as f:
    content = f.readlines()
f.close()

f = open("output.txt", "wb")
for i in content:
    f.write(emoji_pasta_maker(i,emoji_map_probability).encode('UTF-8', 'ignore')) #.encode('UTF-8', 'ignore') ---- maybe add this back later
    f.write('\n'.encode('UTF-8', 'ignore'))
f.close()