import numpy as numpy
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import numpy as np

path='../files/bitcoin-bitcoin/'

stopwords = set(stopwords.words('english'))
stopwords.update(['issue','pull', "github", "bitcoin",'bitcoinqt','bitcoind','qt','merge']+['https', 'issue', 'error','reproduce', 'like', 'http']+
['fix', 'test', 'update', 'add', 'tests', 'remove', 'use', 'feat']+
['x', 'pr', 'branch', 'issue', 'https', 'change', 'one', 'feature', 'request', 'pull', 'fix', 'code', 'changes']+['would','seem','see','seems','th','i\'m'])



def word_cloud(*types):
    
    f, axarr = plt.subplots(3,1)
    mask = np.array(Image.open(("mask-cloud.png")))

    for type in types:
        print(type)
        df=pd.read_csv(path+'bitcoin-bitcoin-{}.csv'.format(type))
        df = df.replace(np.nan, '', regex=True)
        infos=['title','body','comments','comments_review']
        text=''
        for info in infos:
            try:
                print(df[info].to_string())
                text+=df[info].to_string()
            except:
                pass
        
    
        wordcloud = WordCloud(width=2000, height=1000,stopwords=stopwords,background_color="white",collocations=False,normalize_plurals=True,mask=mask).generate(text)
        fig=plt.figure( figsize=(20,10))

        type = type if(type!='pulls') else 'pull requests'

        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        fig.suptitle('{}'.format(type),fontsize=30)
        plt.savefig('wordcloud-{}.png'.format(type))
	
        #plt.show()



word_cloud('issues','pulls','commits')
