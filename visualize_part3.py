import analyze_data_project_part3 as parent
import json, pandas as pd, numpy as np, matplotlib.pyplot as plt

with open('twitter_data_project_part3.json',encoding='utf-8') as fin:
  json_data = json.load(fin)

df = pd.json_normalize(json_data)


def func(pct, allvalues):
  absolute = int(pct / 100. * np.sum(allvalues))
  return "{:.1f}%".format(pct, absolute)

def plot_hashtags():
  fig, (ax1,ax2) = plt.subplots(1,2,figsize=(10,10))

  y = []
  l = []
  s, cnt = 0, 0
  for i in range(len(parent.revoccur)):
    if cnt < 5:
      y.append(parent.revoccur[i])
      l.append(f"#{parent.revhash[i]}")
    else:
      s = s + parent.revoccur[i]
    cnt = cnt + 1
  y.append(s)
  s, cnt = 0, 0
  y1 = []
  for j in range(len(y)):
    if cnt == 5:
      break
    s = s + y[j]
    cnt = cnt + 1

  y1.append(s)
  y1.append(y[5])
  label = ["Top 5 Hashtags", "Other Hashtags"]
  explode = [0.1, 0]
  ax1.pie(np.array(y1), labels = label, explode = explode, shadow = True, autopct = lambda pct: func(pct, y1))
  ax1.set_title("Top 5 X Others")

  y.pop()
  explode = [0, 0, 0, 0, 0]
  ax2.pie(np.array(y), labels = l, explode = explode, shadow = True, autopct = lambda pct: func(pct, y))
  ax2.set_title("Top 5 Hashtag's Ratio")
  plt.show()


def plot_tweettype():
  x = np.array(["retweeted", "replied_to", "quoted", "original"])
  y = np.array([len(parent.retweeted), len(parent.replied_to), len(parent.quoted), len(parent.original)])
  plt.bar(x, y, color="#4CAF50", edgecolor='black')
  plt.xlabel('Tweet Type', fontsize=12)
  plt.ylabel('Frequency', fontsize=12)
  plt.title('Tweet Type Plot', fontsize=18)
  plt.show()

# plot_hashtags()
# plot_tweettype()