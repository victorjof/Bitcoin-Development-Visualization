#python3 main.py nameRepo
#ex. $python3 main.py bitcoin/bitcoin


import csv
from Graphs import DiGraph
import ast
from matplotlib import pyplot as plt
import requests
import sys
import csv

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


def get_rank_commits(repo):
    r=requests.get('https://api.github.com/repos/'+repo+'/stats/contributors')
    x=r.json()
    contribuitors=[]
    for cto in x:
        contribuitors.append((cto['author']['login'],cto['total']))
    return contribuitors[::-1]

def detect_invalid_username(name):
    if(name=='ghost' or name==''):
        return True
    return False

def plot_hist(x,y):
    plt.xticks(rotation='vertical')
    frame1 = plt.gca()
    frame1.axes.xaxis.set_ticklabels([])
    plt.bar(x[:100],y[:100])
    plt.title('Centralidade de intermediação (EOS)')
    plt.ylabel('Grau de centralidade')
    plt.xlabel('Usuários')
    plt.show() 


def main():
    G= DiGraph()
    repo=sys.argv[1].replace("/","-")
    reader_issues = csv.DictReader(open(repo+'-issues.csv', 'r'))
    reader_pulls = csv.DictReader(open(repo+'-pulls.csv', 'r'))
    
    
    f=open('daniel_format.txt','w')
    dependences={}

    for issue in reader_issues:
        author=issue['author']
        if(detect_invalid_username(author) and not(issue['comments_authors'])):
            continue
        for commenter in ast.literal_eval(issue['comments_authors']):
            if(detect_invalid_username(commenter)):
                continue
            G.addEdge(author,commenter)
            f.write('{},{}\n'.format(author,commenter))
    for issue in reader_pulls:
        author=issue['author']
        if(detect_invalid_username(author) and not(issue['comments_authors'])):
            continue
        for commenter in ast.literal_eval(issue['comments_authors']):
            if(detect_invalid_username(commenter)):
                continue
            G.addEdge(author,commenter)
            f.write('{},{}\n'.format(author,commenter))
    f.close()
    degree=G.betweennessCentrality()
    rank= sorted(degree.items(),key=lambda x:x[1],reverse=True)
    print(rank[0])
    x,y=zip(*rank)#comment network data
    print(y[:10])    
    contribuitors=get_rank_commits(sys.argv[1])

    x1,y1=zip(*contribuitors)#Commits analysis

    plot_hist(x,y)


if __name__ == '__main__':
    main()
