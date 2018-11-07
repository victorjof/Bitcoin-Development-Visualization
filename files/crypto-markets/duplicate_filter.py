#remover duplicatas na coluna 'data': considerar a primeira instância para cada semana

import pandas as pd

def main():
    df=pd.read_csv('filtered_market_20_SEMI_FINAL.csv')
    #df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m'))
    #df['date'] = df['date'].apply(date_formatter)
    df.drop_duplicates(subset=['name', 'date'], keep='first', inplace=True)
    df.to_csv('filtered_market_20_FINAL.csv', index=False)

main()