
import nltk

from word_forms.word_forms import get_word_forms

cur_word = "talky"

print(get_word_forms(cur_word))

for i in get_word_forms(cur_word):
    for j in get_word_forms(cur_word)[i]:
        print(j)


