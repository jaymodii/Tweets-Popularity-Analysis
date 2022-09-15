#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: amethyst  <--- are you me?  remember to change the author!

Derive from this file for your code for Project Part 2.

(Demonstrates how to un-json-ify the data saved by twitter_gatherer_project_part_2.py
and convert it to a pandas data frame)
"""

#%% 
import json, pandas as pd, numpy as np

with open('twitter_data_project_part3.json',encoding='utf-8') as fin:
  json_data = json.load(fin)

df = pd.json_normalize(json_data)

hashset = set()
hashdict = {}
hashlist = []
hashtags = []
for i in range(0, len(df)):
  try:
    if pd.isna(df['entities.hashtags'][i]).any() != True:
      for j in range(0, len(df['entities.hashtags'][i])):
        hashlist.append(df['entities.hashtags'][i][j]['tag'])
        hashset.add(df['entities.hashtags'][i][j]['tag'])
  except:
    pass

for x in hashset:
  y = hashlist.count(x)
  hashdict[x] = y
hashdict = sorted(hashdict.items(), key=lambda kv: kv[1])
hashdict = {k: v for k, v in hashdict}
keysList = list(hashdict.keys())
valuesList = list(hashdict.values())
revsortdict = {}
cnt = 0
print("Top 5 Hashtags:")
for i in range(len(keysList)-1, -1, -1):
  opdict = {}
  opdict["hashtag"] = keysList[i]
  opdict["occurance"] = valuesList[i]
  hashtags.append(opdict)
  if cnt < 5:
    print(f"{keysList[i]} : {valuesList[i]}")
  cnt = cnt + 1
  revsortdict[keysList[i]] = valuesList[i]

revhash = list(revsortdict.keys())
revoccur = list(revsortdict.values())

hashdf = {"hashtag": keysList, "occurance": valuesList}


# ------------------------------------------------------------------------------------------


tweettype = []
retweeted = []
quoted = []
replied_to = []
original = []
tidlist = []
ttypelist = []
for i in range(0, len(df)):
  opdict = {}
  try:
    if pd.isna(df['referenced_tweets'][i]).any() != True:
      opdict["tweetid"] = df['referenced_tweets'][i][0]['id']
      opdict["tweettype"] = df['referenced_tweets'][i][0]['type']
      tidlist.append(df['referenced_tweets'][i][0]['id'])
      ttypelist.append(df['referenced_tweets'][i][0]['type'])
      tweettype.append(opdict)
      if df['referenced_tweets'][i][0]['type'] == "retweeted":
        retweeted.append(df['referenced_tweets'][i][0]['id'])
      elif df['referenced_tweets'][i][0]['type'] == "replied_to":
        replied_to.append(df['referenced_tweets'][i][0]['id'])
      elif df['referenced_tweets'][i][0]['type'] == "original":
        original.append(df['referenced_tweets'][i][0]['id'])
      elif df['referenced_tweets'][i][0]['type'] == "quoted":
        quoted.append(df['referenced_tweets'][i][0]['id'])
      else:
        pass
  except:
    pass

typedf = {"tweetid": tidlist, "tweettype": ttypelist}


# ------------------------------------------------------------------------------------------

# with open('top_hashtags.json', 'w',encoding='utf8') as out:
#     json.dump(hashtags,out,indent=4, ensure_ascii=False)
