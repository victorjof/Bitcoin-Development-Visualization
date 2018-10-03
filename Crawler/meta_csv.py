
import json,csv,re,sys,shutil,ast
import pandas as pd


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





def sinc_solved_issues(filename):
    filename=filename.replace('/','-')
    filename_pull=filename+'-pulls.csv'
    filename_commit=filename+'-commits.csv'
    filename_issue=filename+'-issues.csv'

    with open('metadata_csv/'+filename_pull, 'r') as file: 
        reader=csv.DictReader(file)
        dict={}
        for c in reader:
            if(c['issue']):
                #print(c['number'])
                issues=ast.literal_eval(c['issue'])
                for issue in issues:
                    files=ast.literal_eval(c['files_changed']) if(c['files_changed']) else []
                    try:
                        dict[issue].extend(files)
                    except:
                        dict[issue]=files

    with open('metadata_csv/'+filename_commit, 'r') as file: 
        reader=csv.DictReader(file)
        for c in reader:
            if(c['issue']):
                #print(c['sha'])
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
    with open('metadata_csv/'+filename_issue, 'r') as orig, open('metadata_csv/outputfile.csv', 'w') as tempfile:
        reader=csv.DictReader((x.replace('\0', '') for x in orig),fieldnames=field) 
        writer=csv.DictWriter(tempfile,fieldnames=field)
        for row in reader:
            number=row['number']
            if(number in dict.keys()):
                row['files_changed']=dict[number]
            row={'author':row['author'],'number':row['number'],'labels':row['labels'],'title':row['title'],'state':row['state'],'date':row['date'],'body':row['body'],'URL':row['URL'],'closed_at':row['closed_at'],'trace_links':row['trace_links'],'files_changed':row['files_changed'],'comments_authors':row['comments_authors'],'comments':row['comments']}
            writer.writerow(row)
    shutil.move('metadata_csv/outputfile.csv', 'metadata_csv/'+filename_issue)




def artefact_references(text):
    res=re.findall(r"\s+#(\d+)",text)
    res.extend(re.findall(r"\[#(\d+)\]",text))
    references=set()
    for ref in res:
        references.add(ref)
    if(len(references)==0):
        return ''
    return list(references)


def modified_issues(text):
    text=text.lower() if text else ''
    res=re.findall(r"(close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)[^\n]*#(\d+)",str(text))
    list=[]
    for ref in res:
        list.append(ref[1])
    return list

def get_files_commit(c):
    list_files=[]
    for file in c['files']:
        list_files.append(file['filename'])
    return list_files


def get_comments_authors_issue(issue,comments):
    author_name=check_existing_name(issue,'user','login')
   
    names=[]
    for comment in comments:
        names.append(check_existing_name(comment,'user','login'))
    authors=list(set(set(names)-set([author_name])))
    return  (authors if (authors) else '')

def get_issue_tracelinks(bug):
    text=bug['body'] if bug['body']!=None else ''
    comments=bug['commentaries']
    cmm=''
    for comment in comments:
        if(comment['body']!=None):
            cmm+=' '+comment['body']
    text+=cmm
    
    return artefact_references(text),cmm,get_comments_authors_issue(bug,comments)

def get_comments_authors_pull(pull,comments_authors,comments_authors_review):
    author_name=check_existing_name(pull,'user','login')

    names=[]
    for comment in comments_authors:
        names.append(check_existing_name(comment,'user','login'))
    for comment in comments_authors_review:
        names.append(check_existing_name(comment,'user','login'))
    authors=list(set(set(names)-set([author_name])))
    return authors if(authors)  else ''



def get_pull_comments(pull):
    comments=''
    comments_review=''

    for cmt in pull['commentaries']:
        comments+=cmt['body']

    for cmt in pull['commentaries_review']:
        comments_review+=cmt['body']

    return comments,comments_review,get_comments_authors_pull(pull,pull['commentaries'],pull['commentaries_review'])
    
    

def get_files(artefact):
    list_files=[]
    for file in artefact['files']:
        list_files.append(file['filename'])
    return list_files



def check_existing_name(artefact,key1,key2):
    try:
        return artefact[key1][key2]
    except:
        return ''

    
def write_artefact(repo,type):
    csvfilename = '{}-{}.csv'.format(repo.replace('/', '-'),type)
    jsonfilename= '{}-{}.json'.format(repo.replace('/', '-'),type)



    with open('data_json/'+jsonfilename, "r") as read_file:
        data=json.load(read_file)
    
    with open('metadata_csv/'+csvfilename, 'w', newline='') as csvfile:
        csvout = csv.writer(csvfile)
        
        if(type=='commits'):
            csvout.writerow(['author','committer','sha','body','date','URL','issue','files_changed'])
            for commit in data:
                date = commit['commit']['committer']['date']
                text=commit['commit']['message']
                list_issues=modified_issues(text) if(modified_issues(text)) else ''
                list_commits=get_files(commit['files']) if(get_files(commit['files'])) else ''
                author=check_existing_name(commit,'author','login')
                committer=check_existing_name(commit,'committer','login')
                csvout.writerow([author,committer,commit['sha'],text,date,commit['html_url'],list_issues,list_commits])

        elif(type=='pulls'):
            csvout.writerow(['author','number','labels', 'title', 'state','date','body' ,'URL','files_changed','merged_at','issue','comments_authors','comments','comments_review'])
            
            for pull in data:

                filesChanged=get_files(pull)    
                if(filesChanged==[]):
                    pass
                labels = ', '.join([l['name'] for l in pull['labels']])
                date = pull['created_at'].split('T')[0]
                author=check_existing_name(pull,'user','login')
                merged_at=pull['merged_at']
                list_issues=modified_issues(pull['body']) if(modified_issues(pull['body'])) else ''
                comments,comments_review,comments_authors=get_pull_comments(pull)
                csvout.writerow([author,pull['number'],labels, pull['title'], pull['state'],date,pull['body'],
                                    pull['html_url'],filesChanged,merged_at,list_issues,comments_authors,comments,comments_review])



        elif(type=='issues'):
            csvout.writerow(['author','number','labels', 'title', 'state','date','body' ,'URL','closed_at','trace_links','files_changed','comments_authors','comments'])

            for issue in data:
                labels = ', '.join([l['name'] for l in issue['labels']])
                date = issue['created_at'].split('T')[0]
                links,comments,comments_authors=get_issue_tracelinks(issue)
                author=check_existing_name(issue,'user','login')
                csvout.writerow([author,issue['number'],labels, issue['title'], issue['state'], date,issue['body'],
                                    issue['html_url'],issue['closed_at'],links,'',comments_authors,comments])



def convert_repo(repo):
    print(repo)
    write_artefact(repo,'issues')
    write_artefact(repo,'pulls')
    write_artefact(repo,'commits')
    sinc_solved_issues(repo)

