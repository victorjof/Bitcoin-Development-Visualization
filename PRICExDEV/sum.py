import pandas as pd
import datetime
import time
import sys
import copy
import csv

def date_formatter(date_str):
    year, week = date_str.split("w")
    r = datetime.datetime.strptime(year+'-'+week, "%Y-%w")
    print(year)

sum_week = 0
globalID = ''
if __name__ == '__main__':
    with open('week.csv', 'r') as f:
        reader = csv.reader(f)
        mylist = list(reader)

    #soma os commits, etc. por semana
    globalID = mylist[1][0] + mylist[1][1]
    for row in mylist[1:]:
        glob = row[0] + row[1]
        if glob != globalID:
            sum_week = 0
            globalID = glob
        sum_week = sum_week + int(row[2])
        row[2] = sum_week
    filename = 'sum_week.csv'

    with open(filename, "w") as outfile:
        for entries in mylist:
            outfile.write(str(entries[0]) + ',' + str(entries[1]) + ',' + str(entries[2]))
            outfile.write("\n")

    #tira duplicatas e formata as datas 
    df=pd.read_csv('sum_week.csv')
    df.drop_duplicates(subset=['name', 'date'], keep='last', inplace=True)
    # df['date'] = df['date'].apply(date_formatter)
    df.to_csv('sum_week.csv', index=False)