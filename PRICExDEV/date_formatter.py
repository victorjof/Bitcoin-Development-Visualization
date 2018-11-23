#seleção das criptomoedas com os maiores capital de mercado baseado na coluna 'ranknow'
#PARA EXECUTAR: python3 date_formatter.py [ranknow] [week|month|day|year]
#exemplo: python3 date_formatter.py 5 week

import pandas as pd
import datetime
import time
import sys
import copy

class Utils:
    def __init__(self):
        self.format_type = None
        self.df = None
        self.rank = None

        self.aux_var_year = '0'
        self.aux_var_week = '0'

    def filter_by_rank(self):
        list = [str(x) for x in range(1, int(rank) + 1)]
        x = copy.deepcopy(self.df)
        self.df = x[x['ranknow'].isin(list)]

    def remove_duplicates(self):
        self.df.drop_duplicates(subset=['key', 'date'], keep='first', inplace=True)

    def format_date(self):
        # if self.format_type == 'day' or self.format_type == 'month' or self.format_type == 'year' or self.format_type == 'week': #or self.format_type == 'quarter'
        self.df['date'] = self.df['date'].apply(self.date_formatter)
        # elif self.format_type == 'week':
        #     for index, row in self.df.iterrows():
        #         print (row['c1'], row['c2'])
        #     self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
        #     self.df['date'] = self.df['date'].dt.week

    def date_formatter(self, date_str):
        year, month, day = date_str.split("-")
        formatted_date = None
        if self.format_type == 'day':
            formatted_date = year + '{:02d}'.format(int(month)) + '{:02d}'.format(int(day))

        elif self.format_type == 'month':
            formatted_date = year + '-' + '{:02d}'.format(int(month))

        elif self.format_type == 'year':
            formatted_date = year

        elif self.format_type == 'week':
            week = datetime.date(int(year), int(month), int(day)).isocalendar()[1]
            #month = datetime.date(int(year), int(month), int(day)).strftime("%W")
            correct_year = year
            correct_week = week
            if int(self.aux_var_year) == int(year) - 1 and int(self.aux_var_week) == int(week):
                correct_year = self.aux_var_year
            elif int(self.aux_var_year) == int(year) and int(self.aux_var_week) > int(week):
                correct_year = str(int(year) + 1)
            elif int(self.aux_var_year) == int(year) + 1 and int(self.aux_var_week) == int(week) and int(week) == 1:
                correct_year = self.aux_var_year
            formatted_date = correct_year + "w" + '{:02d}'.format(int(week))
            self.aux_var_year = correct_year
            self.aux_var_week = correct_week
        # elif format_type == 'quarter':
        return formatted_date

if __name__ == '__main__':
    df=pd.read_csv('contribution_history_edited.csv')
    rank = sys.argv[1]
    format_type = sys.argv[2]

    utils = Utils()
    utils.df = df
    utils.format_type = format_type
    utils.rank = rank

    #utils.filter_by_rank()
    utils.format_date()
    utils.remove_duplicates()
        
    utils.df.to_csv('gapminder_1.csv', index=False)

    #df['date'] = pd.to_datetime(df['date'], errors='coerce')
    #df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m'))

    # df.to_csv('filtered_market_20_SEMI_FINAL.csv', index=False)
    # df=pd.read_csv('filtered_market_20_SEMI_FINAL.csv')
    #df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m'))
    #df['date'] = df['date'].apply(date_formatter)

# def main():
#     df=pd.read_csv('crypto-markets.csv')
#     list=[str(x) for x in range(1,int(input("Insert how many of the top projects you want\n")))]
#     df=df[df['ranknow'].isin(list)]
#     df['date'] = pd.to_datetime(df['date'], errors='coerce')
#     df=df[(df['date'].dt.day==1) | (df['date'].dt.day==8) | (df['date'].dt.day==15) | (df['date'].dt.day==22)]
#     #df=df[df['date'].dt.day==1]
#     df.to_csv('filtered_markets_2.csv')
# main()
