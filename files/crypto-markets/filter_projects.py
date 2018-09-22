import pandas as pd


def main():
    df=pd.read_csv('crypto-markets.csv')
    list=[str(x) for x in range(1,int(input("Insert how many of the top projects you want\n")))]
    df=df[df['ranknow'].isin(list)]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df=df[df['date'].dt.day==1] 
    df.to_csv('filtered_markets.csv')    


main()