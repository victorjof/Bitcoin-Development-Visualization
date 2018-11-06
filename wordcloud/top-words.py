import nltk,re,os
import pandas as pd
from collections import Counter

stopwords = nltk.corpus.stopwords.words('english')
os.chdir('../files/control_repos/')


def tokenize(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            if(token not in stopwords):
                filtered_tokens.append(token)
    return filtered_tokens





def top_k_words(repo,artefact,k=30):

    df=pd.read_csv('{}-{}.csv'.format(repo,artefact).replace('/','-'))
    df=df[df['body'].str.contains('Merge #')==False]


    text_commits=df['body'].to_string()
    full_text=[]
    for index,row in df.iterrows():
        text_commits=row['body']  
        full_text.extend(tokenize(text_commits))

    count=Counter(full_text)
    return([x[0] for x in count.most_common(k)])

for artefact in ['issues','commits','pulls']:
    top1=top_k_words('vuejs/vue',artefact)
    top2=top_k_words('freeCodeCamp/freeCodeCamp',artefact)
    top=[value for value in top1 if value if value in top2]
    print(top)
