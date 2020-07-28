import pickle
import pandas as pd
import os

object_to_write = set()

directory = os.fsencode("posts/")
# run the following through a loop
for file_cur in os.listdir(directory):
    file_name = os.fsdecode(file_cur)
    print(file_name)
    df = pd.read_csv("posts/" + file_name)
    df = df.fillna("")
    for idx, i in df.iterrows():
        object_to_write.add((i['id'], i['score']))

with open("submission_ids.pickle", "wb") as f:
    pickle.dump(object_to_write, f, pickle.HIGHEST_PROTOCOL)


