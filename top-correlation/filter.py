import pandas as pd
from collections import OrderedDict
import ast
import numpy as np
path='../files/bitcoin-bitcoin/'

members=['Empact', 'MarcoFalke', 'MeshCollider', 'NicolasDorier', 'Sjors', 'achow101', 'btcdrak', 'eklitzke', 'fanquake', 'gmaxwell', 'harding', 'instagibbs', 'jamesob', 'jl2012', 'jnewbery', 'jonasschnelli', 'jtimon', 'kallewoof', 'ken2812221', 'laanwj', 'luke-jr', 'morcos', 'practicalswift', 'promag', 'sdaftuar', 'sipa', 'skeees', 'theuni']
artefacts=['issues','pulls','commits']
    

def detect_invalid_username(name):
    name=name.lower()
    if(name=='ghost' or name=='' or 'bot' in name or 'test' in name):
        return True
    return False


top_contribuitors={}


for artefact in artefacts:
    df=pd.read_csv(path+'bitcoin-bitcoin-{}.csv'.format(artefact))
    if(artefact=='pulls'):
        df=df[df['body'].str.contains('Merge #')==False]

    authors=df.groupby('author')
    top_cont=authors.size().sort_values(ascending=False)
    top_cont=zip(top_cont.index,top_cont)



    for commiter,num_contribuition in top_cont:
        if(not(detect_invalid_username(commiter))):
            if(commiter in top_contribuitors):
                top_contribuitors[commiter]['num_{}'.format(artefact)]=num_contribuition 
            else:
                top_contribuitors[commiter]={'num_{}'.format(artefact):num_contribuition}





for user in top_contribuitors.keys():
    for artefact in artefacts:
        if('num_{}'.format(artefact) not in top_contribuitors[user]):
            top_contribuitors[user]['num_{}'.format(artefact)]=0
    if(user in  members):
        top_contribuitors[user]['status']='member'
    else:
        top_contribuitors[user]['status']='non-member'





df=pd.DataFrame.from_dict(top_contribuitors,orient='index')
df.to_csv('teste.csv')