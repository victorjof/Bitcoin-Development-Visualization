import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from mpl_toolkits.mplot3d import Axes3D

sns.set()


num_users=30


path='files/bitcoin-bitcoin/'
df=pd.read_csv(path+'bitcoin-bitcoin-commits.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
print(df.shape)
df=df[df['body'].str.contains('Merge #')==False]
print(df.shape)


df=pd.read_csv(path+'bitcoin-bitcoin-commits.csv')
authors=df.groupby('author')
y=authors.size().sort_values(ascending=False).values.tolist()[:100]


plt.figure(figsize=(15,10))
plt.plot
plt.bar(list(range(50)),y[:50],width=1,color='b')
frame1 = plt.gca()
frame1.axes.xaxis.set_ticklabels([])
plt.xticks(rotation=0)
plt.xlabel("User")
plt.ylabel("Number of commits")
plt.show()

path='files/bitcoin-bitcoin/'
df=pd.read_csv(path+'bitcoin-bitcoin-commits.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df=df[df['body'].str.contains('Merge #')==False]


dfs=[]
years=[2011,2012,2013,2014,2015,2016,2017]
for year in years:
    dfs.append(df[(df['date']<pd.Timestamp(year+1,1,1)) & (df['date']>pd.Timestamp(year,1,1))])



y=[]


for df in dfs:
    authors=df.groupby('author')
    y.append(authors.size().sort_values(ascending=False).values.tolist()[:num_users])
    print(authors.size().sort_values(ascending=False).values.tolist()[0])

x=[list(range(1,num_users+1)) for x in range(len(years))]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for c, z,xs,ys in zip(['g']*len(years), years,x,y
):
    print(xs)
    ax.set_yticks(ys)
    #highlights top 3 contribuitors
    cs = [c] * len(xs)
    for idx in range(3): 
        cs[idx] = 'r'

    ax.bar(xs, ys, zs=z, zdir='y', color=cs, alpha=0.8,width=1.5)

ax.set_xlabel('Contribuition rank')
ax.set_ylabel('Year:2011 ⟶ 2017')
ax.set_zlabel('Number of Commits')

plt.show()


