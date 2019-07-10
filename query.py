import requests
import json
# from urllib.parse import urlencode

URL = "https://api.clarivate.com/api/wos/"
WOS_KEY = json.load('config.json')['WOS_KEY']
BATCH_SIZE = 100


def query(last, first):
    # wos returns the most recent paper on top so it's alright to just grab 1 record
    url = 'https://api.clarivate.com/api/wos?databaseId=WOS&usrQuery=au={}%20{}&count=1&firstRecord=1'.format(last, first)

    response = requests.get(url, headers={'accept': 'application/json', 'X-ApiKey': WOS_KEY})
    addresses = response.json()['Data']['Records']['records']['REC'][0]

    return addresses
