#seleção das criptomoedas com os maiores capital de mercado baseado na coluna 'ranknow'
#PARA EXECUTAR: python3 date_formatter.py [ranknow] [week|month|day]

import pandas as pd
import datetime
import time
import sys

# def main():
#     df=pd.read_csv('crypto-markets.csv')
#     list=[str(x) for x in range(1,int(input("Insert how many of the top projects you want\n")))]
#     df=df[df['ranknow'].isin(list)]
#     df['date'] = pd.to_datetime(df['date'], errors='coerce')

#     df=df[(df['date'].dt.day==1) | (df['date'].dt.day==8) | (df['date'].dt.day==15) | (df['date'].dt.day==22)]
#     #df=df[df['date'].dt.day==1]
#     df.to_csv('filtered_markets_2.csv')

# main()

def date_formatter(date_str, format_type):
    year, month, day = date_str.split("-")
    if format_type == 'day':


    elif format_type == 'month':
        month = datetime.date(int(year), int(month), int(day)).isocalendar()[1]
        #month = datetime.date(int(year), int(month), int(day)).strftime("%W")
        formatted_date = year + "w" + '{:02d}'.format(int(month))

    elif format_type == 'year':

    elif format_type == 'week':

    return formatted_date

def main():
    df=pd.read_csv('crypto-markets.csv')
    list=[str(x) for x in range(1,int(sys.argv[1]) + 1)]
    df=df[df['ranknow'].isin(list)] 

    format_date = sys.argv[2]
    #df['date'] = pd.to_datetime(df['date'], errors='coerce')
    #df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m'))
    df['date'] = df['date'].apply(date_formatter, format_date)
    # df.to_csv('filtered_market_20_SEMI_FINAL.csv', index=False)

    # df=pd.read_csv('filtered_market_20_SEMI_FINAL.csv')
    #df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m'))
    #df['date'] = df['date'].apply(date_formatter)
    df.drop_duplicates(subset=['name', 'date'], keep='first', inplace=True)
    df.to_csv('filtered_market_final.csv', index=False)

main()