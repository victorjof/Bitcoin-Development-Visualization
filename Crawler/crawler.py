import socket,json,requests,datetime,time

count=0

def request(url):
    sleep_time=10
    while True:
        try:
            r=requests.get(url, auth=('','Insert your key here'))
	    #https://github.com/settings/tokens
            try:
                if(r.status_code != 200):
                    error=r.json()
                    error['url_erro']=url
                    error=str(error)
                    with open('erro.txt', 'a') as outfile:  
                        outfile.write(str(error))
                    print('error logged in file')
                    if('diff' in error):
                        return r
                    else:
                        time.sleep(sleep_time)
                        return request(url)
            except:
                with open('erro.txt', 'a') as outfile:  
                        outfile.write('ERROR 500 '+url+str(r.status_code))
                print("SERVER ERROR 500 WAIT 60 seconds",url)
                time.sleep(60)
                return request(url)
        except ConnectionError as e:
            print ("Wait ",sleep_time," seconds for ConnectionError: ")
            print(e)
            time.sleep(sleep_time) 
            continue 
        except socket.error as s:
            print ("Wait ",sleep_time," seconds for SocketError: ")
            print(s) 
            time.sleep(sleep_time) 
            continue 
        else:
            break
        sleep_time+=5
    
    
    print(url)
    rate_limit(r.headers)
    return r


def rate_limit(headers):
    num_remaining_request=int(headers['x-ratelimit-remaining'])
    reset_time=int(headers['x-ratelimit-reset'])
    datetime_format = '%Y-%m-%d %H:%M:%S'
    datetime_reset = datetime.datetime.fromtimestamp(reset_time).strftime(datetime_format)
    datetime_now = datetime.datetime.now().strftime(datetime_format)
    if(num_remaining_request<10):
        print(num_remaining_request,' left')
        while(datetime_reset > datetime_now):
                print ("Zzzzzz...")
                print ("The limit will reset on: ",datetime_reset)
                datetime_now = datetime.datetime.now().strftime(datetime_format)
                time.sleep(30)



def get_files_changed(pullAPIUrl):
    filesChanged=request(pullAPIUrl+"/files")

    if(not(filesChanged.ok)):
        return None
    filesChanged=filesChanged.json()
    fileNames=[]
    for file in filesChanged:
       fileNames.append(file['filename'])
    return fileNames
        

def check_pull_artefact(pull_artefact):
    if(pull_artefact.ok):
        return pull_artefact.json()
    else:
        return []


def extra_info(artefact_list,type):
    global count
    size_artefacts=len(artefact_list)
    jump_pull=0

    artefacts=[]

    if(type=='commits'):
        for idx in range(size_artefacts):
            artefact_list[idx]['files']=request(artefact_list[idx]['url']).json()
            artefacts.append(artefact_list[idx])

    elif(type=='issues'):
        for idx in range(size_artefacts):
            if('pull_request' in artefact_list[idx]):
                jump_pull+=1
                continue
            artefact_list[idx]['commentaries']=request(artefact_list[idx]['comments_url']).json()
            artefacts.append(artefact_list[idx])
    
    elif(type=='pulls'):
        for idx in range(size_artefacts):
            files_changed=request(artefact_list[idx]['url']+'/files')
            artefact_list[idx]['files']=check_pull_artefact(files_changed)
            
            commentaries=request(artefact_list[idx]['issue_url']+'/comments')
            commentaries_review=request(artefact_list[idx]['url']+'/comments')
            
            artefact_list[idx]['commentaries']=check_pull_artefact(commentaries)
            artefact_list[idx]['commentaries_review']=check_pull_artefact(commentaries_review)
            artefacts.append(artefact_list[idx])

    count+=(size_artefacts-jump_pull)

    print(count,' {} acquired'.format(type))
    return(artefacts)

            


def get_artefact(repo_name,artefact_type):
    url = 'https://api.github.com/repos/{}/{}?state=all&per_page=100'.format(repo_name,artefact_type)
    artefacts=[]
    r = request(url)
    artefacts.extend(extra_info(r.json(),artefact_type))




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
            artefacts.extend(extra_info(r.json(),artefact_type))
            if pages['next'] == pages['last']:
                break

    with open("data_json/"+"{}-{}.json".format(repo_name.replace('/','-'),artefact_type), "w") as write_file:
        json.dump(artefacts, write_file,indent=4)


def get_repository(repo,opts=['issues','commits','pulls']):
    for opt in opts:
        get_artefact(repo,opt)

