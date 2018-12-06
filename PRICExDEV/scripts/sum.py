import pandas as pd
import datetime
import time
import sys
import copy
import csv

def date_formatter(date_str):
    year, week = date_str.split("w")
    d = year + '-W' + week
    r = datetime.datetime.strptime(d + '-0', "%Y-W%W-%w")
    return r

sum_week = 0
globalID = ''
if __name__ == '__main__':
    with open('edit1.csv', 'r') as f:
        reader = csv.reader(f)
        mylist = list(reader)

    #soma os commits, etc. por semana
    globalID = mylist[1][0] + mylist[1][1]
    for row in mylist[1:]:
        glob = row[0] + row[1]
        if glob != globalID:
            sum_week = 0
            globalID = glob
        sum_week = sum_week + float(row[2])
        row[2] = sum_week
    filename = 'edit1.csv'

    with open(filename, "w") as outfile:
        for entries in mylist:
            outfile.write(str(entries[0]) + ',' + str(entries[1]) + ',' + str(entries[2]))
            outfile.write("\n")

    #tira duplicatas e formata as datas 
    df=pd.read_csv('edit1.csv')
    df.drop_duplicates(subset=['name', 'date'], keep='last', inplace=True)
    # df['date'] = df['date'].apply(date_formatter)

    df.to_csv('edit1.csv', index=False)