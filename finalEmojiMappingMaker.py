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
import emojiRelationMaker

def main():
    my_stop_words = stop_words.my_stop_words

    word_to_investigate = "food"

    edited_emoji_map2 = {}
    with open('emoji_mapping_secondary.json','r', encoding="utf8") as fp:
        edited_emoji_map2 = json.load(fp)
    fp.close()

    #print(edited_emoji_map2["bitch"], str(len(edited_emoji_map2.keys())))

    emoji_probability = 0.1
    minimum_emojis = 2
    maximum_emoji = 5
    remove_stopwords = True

    emoji_map_probability = emojiRelationMaker.emoji_probability_maker(edited_emoji_map2, emoji_probability, remove_stopwords, minimum_emojis, maximum_emoji, my_stop_words)
    print(emoji_map_probability[word_to_investigate], str(len(emoji_map_probability.keys())))

    with open('emoji_mapping.json','w') as fp:
        json.dump(emoji_map_probability, fp)

if __name__ == "__main__":
    main()