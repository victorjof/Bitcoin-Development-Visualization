import pandas as  pd
import numpy as np


path='../files/bitcoin-bitcoin/'
artefats=['commits','issues','pulls']
contribuition_history=pd.DataFrame()


def sum_antecessor(list_value):
    
    for idx in range(1,len(list_value)):
        list_value[idx]+=list_value[idx-1]
        
def accumulate(contribuition_history,correct_dates):

    correct_dates.set_index('date', inplace=True)
    correct_dates.update(contribuition_history.set_index('date'))
    values=[]
    for artefact in artefats:
        values=correct_dates['count_{}'.format(artefact)].values.astype('int32')
        sum_antecessor(values)
        correct_dates['count_{}'.format(artefact)]=values

    return correct_dates

def transform_cdf():
    first=contribuition_history.index[0]
    last=contribuition_history.index[-1]
    contribuition_history.fillna(0,inplace=True)
    data_start_issuetracker=0
    for idx,row in contribuition_history.iterrows():
        if((row['count_pulls']!=0) and (row['count_issues']!=0)):
            data_start_issuetracker=idx #date is the index, marks the appearance of issues and pull requests
            break
    

    contribuition_history.reset_index(level=df.index.names, inplace=True)
    calendar=(pd.date_range(start=data_start_issuetracker, end=last))
    correct_dates=pd.DataFrame({'date':calendar,'count_commits':np.zeros(calendar.shape[0]),'count_issues':np.zeros(calendar.shape[0]),'count_pulls':np.zeros(calendar.shape[0])},columns=['date','count_commits','count_issues','count_pulls'])
    correct_dates['date']=correct_dates['date'].apply(lambda x: str(x).split(' ')[0])
    return accumulate(contribuition_history,correct_dates)


for artefact in artefats:
    
    df=pd.read_csv(path+'bitcoin-bitcoin-{}.csv'.format(artefact))

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['date']=df['date'].apply(lambda x: str(x).split(' ')[0])
    
    df=df.sort_values(by='date')
    df=df[df['body'].str.contains('Merge #')==False]
    
    df=df.groupby('date').count()
    #print(df.index)
    df=df[['author']]
    df.columns=['count_{}'.format(artefact)]
    
    contribuition_history=df if contribuition_history.empty else contribuition_history.join(df)



contribuition_history=transform_cdf()
print(contribuition_history)
contribuition_history.to_csv('contribuition_history.csv')
