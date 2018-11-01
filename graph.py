


import csv
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


path='files/bitcoin-bitcoin/'


def detect_invalid_username(name):
    if(name=='ghost' or name==''):
        return True
    return False


def main():
    repo=sys.argv[1].replace('/','-')
    reader_issues = csv.DictReader(open(path+repo+'-issues.csv', 'r'))
    reader_pulls = csv.DictReader(open(path+repo+'-pulls.csv', 'r'))
    
    
    f=open('daniel_format.txt','w')
    dependences={}

    for issue in reader_issues:
        author=issue['author']
        print(issue['number'])
        if(detect_invalid_username(author) or not(issue['comments_authors'])):
            continue
        for commenter in ast.literal_eval(issue['comments_authors']):
            if(detect_invalid_username(commenter)):
                continue
            f.write('{},{}\n'.format(author,commenter))
    for issue in reader_pulls:
        author=issue['author']
        if(detect_invalid_username(author) or not(issue['comments_authors'])):
            continue
        for commenter in ast.literal_eval(issue['comments_authors']):
            if(detect_invalid_username(commenter)):
                continue
            f.write('{},{}\n'.format(author,commenter))
    f.close()




if __name__ == '__main__':
    main()
