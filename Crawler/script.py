from crawler import get_repository
from meta_csv import convert_repo
from crawler import request
import requests

def main():
    repos=['bitcoin/bips','bitcoin/bitcoin']    
    for repo in repos:
        get_repository(repo)
        convert_repo(repo)


main()