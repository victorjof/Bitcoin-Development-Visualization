"""
Forked from: patrickfuller/github_issues_to_csv.py
"""
import argparse
import csv
from getpass import getpass
import time
import datetime
import requests
from requests.exceptions import ConnectionError
import socket 
import re
import ast
import shutil
import os
import sys
import pandas as pd
import json

auth = None
state = 'all'
count_requests=0


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


def request(url):
    sleep_time=10
    while True:
        try:
            r=requests.get(url, auth=('','COLOCAR API TOKEN/KEY AKI'))
            if(r.status_code==500):
                print("SERVER ERROR 500 WAIT",sleep_time,'seconds')
                time.sleep(sleep_time)
                return request(url)
            if(r.status_code != 200):
                error=r.json()
                error['url_erro']=url
                error=str(error)
                with open('data.txt', 'a') as outfile:  
                    outfile.write(str(error))
                print('error logged in file')
                if('diff' in error):
                    return r
                else:
                    time.sleep(sleep_time)
                    return request(url)
            rate_limit(r.headers)

        except ConnectionError as e:
            print ("Wait ",sleep_time," seconds for ConnectionError: ")
            print(e)
            time.sleep(sleep_time) 
            continue 
        except socket.error as s:
            print ("Wait ",sleep_time," seconds for SocketError: ")
            print(s) 
            continue 
        else:
            break
        sleep_time+=5
    print(url)
    return r



def request_pull(repo,pull_number):
    url='https://api.github.com/repos/'+repo+'/pulls/'+pull_number
    pull=request(url)
    if pull.ok:
        return pull.json()
    else:
        return None
    




def request_issue(repo,issue_number):
    url='https://api.github.com/repos/'+repo+'/issues/'+issue_number
    issue=request(url)
    if issue.ok:
        return issue.json()
    else:
        return None



def rate_limit(headers):
    num_remaining_request=int(headers['x-ratelimit-remaining'])
    reset_time=int(headers['x-ratelimit-reset'])
    datetime_format = '%Y-%m-%d %H:%M:%S'
    datetime_reset = datetime.datetime.fromtimestamp(reset_time).strftime(datetime_format)
    datetime_now = datetime.datetime.now().strftime(datetime_format)
    if(num_remaining_request<100):
         while(datetime_reset > datetime_now):
                print ("Zzzzzz...")
                print ("The limit will reset on: ",datetime_reset)
                datetime_now = datetime.datetime.now().strftime(datetime_format)
                time.sleep(120)




def sinc_solved_issues(filename):
    filename=re.sub('/','-',filename)
    filename_pull=filename+'-pulls.csv'
    filename_commit=filename+'-commits.csv'
    filename_issue=filename+'-issues.csv'
    with open('files/'+filename_pull, 'r') as file: 
        reader=csv.DictReader(file)
        dict={}
        for c in reader:
            if(c['issue']):
                print(c['number'])
                issues=ast.literal_eval(c['issue'])
                for issue in issues:
                    files=ast.literal_eval(c['files_changed']) if(c['files_changed']) else []
                    try:
                        dict[issue].extend(files)
                    except:
                        dict[issue]=files

    with open('files/'+filename_commit, 'r') as file: 
        reader=csv.DictReader(file)
        for c in reader:
            if(c['issue']):
                print(c['sha'])
                issues=ast.literal_eval(c['issue'])
                for issue in issues:
                    files=ast.literal_eval(c['files_changed']) if(c['files_changed']) else []
                    try:
                        dict[issue].extend(files)
                    except:
                        dict[issue]=files

    for key in dict.keys():
        files=dict[key]
        dict[key]=list(set(files))
    

    field=['author','number',	'labels',	'title',	'state',	'date',	'body',	'URL',	'closed_at','trace_links','files_changed','comments_authors','comments']
    with open('files/'+filename_issue, 'r') as orig, open('files/outputfile.csv', 'w') as tempfile:
        reader=csv.DictReader(orig,fieldnames=field) 
        writer=csv.DictWriter(tempfile,fieldnames=field)
        for row in reader:
            number=row['number']
            if(number in dict.keys()):
                row['files_changed']=dict[number]
            row={'author':row['author'],'number':row['number'],'labels':row['labels'],'title':row['title'],'state':row['state'],'date':row['date'],'body':row['body'],'URL':row['URL'],'closed_at':row['closed_at'],'trace_links':row['trace_links'],'files_changed':row['files_changed'],'comments_authors':row['comments_authors'],'comments':row['comments']}
            writer.writerow(row)
    shutil.move('files/outputfile.csv', 'files/'+filename_issue)


def order_by_date(filename):
    df= pd.read_csv('files/'+filename)
    if 'issues' in filename:
        df['date']=pd.to_datetime(df.closed_at)
        df=df.sort_values('closed_at',ascending=False)
    elif 'pulls' in filename:
        df['date']=pd.to_datetime(df.merged_at)
        df=df.sort_values('merged_at',ascending=False)
    elif 'commits' in filename:
        df['date']=pd.to_datetime(df.date)
        df=df.sort_values('date',ascending=False)

    df.to_csv('files/'+filename,index=False)


def artefact_references(text):
    res=re.findall(r"\s+#(\d+)",text)
    res.extend(re.findall(r"\[#(\d+)\]",text))
    references=set()
    for ref in res:
        references.add(ref)
    if(len(references)==0):
        return ''
    return list(references)


def get_comments_authors_issue(issue,comments):
    author_name=check_existing_name(issue,'user','login')
   
    names=[]
    for comment in comments:
        names.append(check_existing_name(issue,'user','login'))
    authors=list(set(set(names)-set([author_name])))
    return  (authors if (authors) else '')


def get_issue_tracelinks(bug):
    text=bug['body'] if bug['body']!=None else ''
    comments=request(bug['comments_url']).json()
    cmm=''
    for comment in comments:
        if(comment['body']!=None):
            cmm+=' '+comment['body']
    text+=cmm

    return artefact_references(text),cmm,get_comments_authors_issue(bug,comments)

def get_files_commit(commit):
    url=commit['url']
    c=request(url).json()
    list_files=[]
    for file in c['files']:
        list_files.append(file['filename'])
    return list_files


def modified_issues(text):
    text=text.lower() if text else ''
    res=re.findall(r"(close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved) #(\d+)",str(text))
    list=[]
    for ref in res:
        list.append(ref[1])
    return list


def get_comments_authors_pull(pull,comments_authors,comments_authors_review):
    author_name=check_existing_name(pull,'user','login')
    if(not(comments_authors.ok) and not(comments_authors_review.ok)):
        return None
    elif(not(comments_authors.ok) and comments_authors_review.ok):
        comments_authors=[]
        comments_authors_review=comments_authors_review.json()
    elif((comments_authors.ok) and not(comments_authors_review.ok)):
        comments_authors=comments_authors.json()
        comments_authors_review=[]
    else:
        comments_authors=comments_authors.json()
        comments_authors_review=comments_authors_review.json()

    names=[]
    for comment in comments_authors:
        names.append(check_existing_name(comment,'user','login'))
    for comment in comments_authors_review:
        names.append(check_existing_name(comment,'user','login'))
    authors=list(set(set(names)-set([author_name])))
    return authors if(authors)  else ''




def get_pull_comments(pull):
    comments0=request(pull['issue_url']+'/comments')
    comments_review0=request(pull['url']+'/comments')
    comments=''
    comments_review=''

    if(comments0.ok):
        for comment in comments0.json():
            comments+=comment['body']
    if(comments_review0.ok):
        for comment in comments_review0.json():
            comments_review+=comment['body']

    return comments,comments_review,get_comments_authors_pull(pull,comments0,comments_review0)


    

def get_files_changed(pullAPIUrl):
    filesChanged=request(pullAPIUrl+"/files")

    if(not(filesChanged.ok)):
        return None
    filesChanged=filesChanged.json()
    fileNames=[]
    for file in filesChanged:
       fileNames.append(file['filename'])
    return fileNames


def check_existing_name(artefact,key1,key2):
    try:
        return artefact[key1][key2]
    except:
        return ''

def write_commits(r, csvout):
    global count_requests
    """Parses JSON response and writes to CSV."""
    if r.status_code != 200:
        raise Exception(r.status_code)
    for commit in r.json():
        date = commit['commit']['committer']['date']
        text=commit['commit']['message']
        list_issues=modified_issues(text) if(modified_issues(text)) else ''
        list_commits=get_files_commit(commit) if(get_files_commit(commit)) else ''
        author=check_existing_name(commit,'author','login')
        committer=check_existing_name(commit,'committer','login')
        csvout.writerow([author,committer,commit['sha'],text,date,commit['url'],list_issues,list_commits])
        
        count_requests+=1
    print(count_requests," commits acquired!")


def write_issues(r, csvout):
    global count_requests
    """Parses JSON response and writes to CSV."""
    if r.status_code != 200:
        raise Exception(r.status_code)
    for issue in r.json():
        if 'pull_request' not in issue:
            labels = ', '.join([l['name'] for l in issue['labels']])
            date = issue['created_at'].split('T')[0]
            links,comments,comments_authors=get_issue_tracelinks(issue)
            author=check_existing_name(issue,'user','login')
            csvout.writerow([author,issue['number'],labels, issue['title'], issue['state'], date,issue['body'],
                                issue['html_url'],issue['closed_at'],links,'',comments_authors,comments])
            count_requests+=1
    print(count_requests," issues acquired!")



def write_pulls(r, csvout):
    global count_requests
    """Parses JSON response and writes to CSV."""
    if r.status_code != 200:
        raise Exception(r.status_code)
    for pull in r.json():
        filesChanged=get_files_changed(pull['url'])
        if(filesChanged==None):
            pass
        labels = ', '.join([l['name'] for l in pull['labels']])
        date = pull['created_at'].split('T')[0]
        author=check_existing_name(pull,'user','login')
        merged_at=pull['merged_at']
        list_issues=modified_issues(pull['body']) if(modified_issues(pull['body'])) else ''
        comments,comments_review,comments_authors=get_pull_comments(pull)
        csvout.writerow([author,pull['number'],labels, pull['title'], pull['state'],date,pull['body'],
                            pull['html_url'],filesChanged,merged_at,list_issues,comments_authors,comments,comments_review])
        count_requests+=1
    print(count_requests," pull request acquired!")


def get_commits(name):
    global count_requests
    count_requests=0
    url = 'https://api.github.com/repos/{}/commits?per_page=100'.format(name)
    r = request(url)
    csvfilename = '{}-commits.csv'.format(name.replace('/', '-'))
    with open('files/'+csvfilename, 'w', newline='') as csvfile:
        csvout = csv.writer(csvfile)
        csvout.writerow(['author','committer','sha','body','date','URL','issue','files_changed'])
        write_commits(r, csvout)

       # Multiple requests are required if response is paged
        if 'link' in r.headers:
            pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                     (link.split(';') for link in
                      r.headers['link'].split(','))}
            while 'last' in pages and 'next' in pages:
                pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                         (link.split(';') for link in
                          r.headers['link'].split(','))}
                r = request(pages['next']) #url of next page
                write_commits(r, csvout)
                if pages['next'] == pages['last']:
                    break
    order_by_date(csvfilename)



def get_issues(name):
    global count_requests
    count_requests=0
    url = 'https://api.github.com/repos/{}/issues?state={}&per_page=100'.format(name, state)
    r = request(url)
    csvfilename = '{}-issues.csv'.format(name.replace('/', '-'))
    with open('files/'+csvfilename, 'w', newline='') as csvfile:
        csvout = csv.writer(csvfile)
        csvout.writerow(['author','number','labels', 'title', 'state','date','body' ,'URL','closed_at','trace_links','files_changed','comments_authors','comments'])
        write_issues(r, csvout)

       # Multiple requests are required if response is paged
        if 'link' in r.headers:
            pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                     (link.split(';') for link in
                      r.headers['link'].split(','))}
            while 'last' in pages and 'next' in pages:
                pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                         (link.split(';') for link in
                          r.headers['link'].split(','))}
                r = request(pages['next']) #url of next page
                write_issues(r, csvout)
                if pages['next'] == pages['last']:
                    break
    order_by_date(csvfilename)



def get_pulls(name):
    global count_requests
    count_requests=0
    url = 'https://api.github.com/repos/{}/pulls?state={}&per_page=100'.format(name, state)
    r = request(url)
    csvfilename = '{}-pulls.csv'.format(name.replace('/', '-'))
    with open('files/'+csvfilename, 'w', newline='') as csvfile:
        csvout = csv.writer(csvfile)
        csvout.writerow(['author','number','labels', 'title', 'state','date','body' ,'URL','files_changed','merged_at','issue','comments_authors','comments','comments_review'])
        write_pulls(r, csvout)

       # Multiple request are required if response is paged
        if 'link' in r.headers:
            pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                     (link.split(';') for link in
                      r.headers['link'].split(','))}
            while 'last' in pages and 'next' in pages:
                pages = {rel[6:-1]: url[url.index('<')+1:-1] for url, rel in
                         (link.split(';') for link in
                          r.headers['link'].split(','))}
                r = request(pages['next']) #url of next page
                write_pulls(r, csvout)
                if pages['next'] == pages['last']:
                    break
    order_by_date(csvfilename)


def main():
    global state
    parser = argparse.ArgumentParser(description="Write GitHub repository pull requests "
                                                "to CSV file.")
    parser.add_argument('repositories', nargs='+', help="Repository names, "
                        "formatted as 'username/repo'")
    parser.add_argument('--closed', action='store_true', help="Returns both open only closed pulls")
    args = parser.parse_args()

    if args.closed:
        state = 'closed'
    for repository in args.repositories:
        get_pulls(repository)
        get_issues(repository)
        get_commits(repository)
        sinc_solved_issues(repository)

if __name__ == '__main__':
    main()
