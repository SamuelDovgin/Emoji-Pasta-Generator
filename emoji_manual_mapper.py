#print("hello, my name. is ! sam! ???".split())

from emoji import UNICODE_EMOJI
from nltk.corpus import stopwords


string = ""

remove_words = "(blood type) button for beginner Japanese of adult skin tone aerial baby index medium medium-light dark light medium-dark man woman Islands place acceptable application bargain charge not free open business grade service symbol Mrs. hand admission auto pointing person backhand bar face blond-haired with me heart in food hands closed lowered flag raised computer worker and stone double mark family boy girl mouth picture growing fingers decoration suit heavy sign ice symbols keycap large slider level love glass tilted loudly love-you left right ball getting position room finger way new no mobile oncoming up together playing taking wearing post postal hair right-facing soft without handle tear-off thumbs mode tipping digit passing vacancy here tray cap"  

remove_emoji_words = "mahjong steamy viewing no alternation letter "

remove_words = remove_words.split()

for i in UNICODE_EMOJI.keys():
    no_element_in_list_check = True
    temp = UNICODE_EMOJI[i].replace(":","").split("_")
    for x in temp:
        if x in remove_emoji_words.split():
            no_element_in_list_check = False
    for j in temp:
        if no_element_in_list_check:
            if j not in remove_words:
                string += j + " " + i + " "

print(stopwords.words('english'))

string += " halloween 🎃 pumpkin 🎃 mecca 🕋,"

f = open("output_test.txt", "wb")
#f.write(string)
f.write(string.encode('UTF-8', 'ignore'))
f.close()