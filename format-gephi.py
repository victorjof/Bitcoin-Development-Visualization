


import csv
import ast
from matplotlib import pyplot as plt
import requests
import sys
import pandas as pd
import numpy as np
maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True


path='files/bitcoin-bitcoin/'
repo='bitcoin-bitcoin'

def detect_invalid_username(name):
    if(name=='ghost' or name==''):
        return True
    return False

def write_gephi_format(repo,type,time_filter=False): #time filter -> artefacts from at least 2016
    df=pd.read_csv(path+repo+'-{}.csv'.format(type))
    df = df.replace(np.nan, '', regex=True)

    if(time_filter):
        df['date'] = pd.to_datetime(df['date'], errors='coerce')        
        df[df['date']>pd.Timestamp(2016,1,1)]
    
    f=open('gephi-{}.txt'.format(repo),'a')
    for index,issue in df.iterrows():
        author=issue['author']
        if(detect_invalid_username(author) or not(issue['comments_authors'])):
            continue
        for commenter in ast.literal_eval(issue['comments_authors']):
            if(detect_invalid_username(commenter)):
                continue
            f.write('{},{}\n'.format(author,commenter))
    
    f.close()



def main():

    write_gephi_format(repo,type='issues')
    write_gephi_format(repo,type='pulls')




if __name__ == '__main__':
    main()
