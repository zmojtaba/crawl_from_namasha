from json import decoder
import requests
import json
from lxml.etree import ParserError


try:
    response = requests.get("http://127.0.0.1:4200/api/category/music")
    response = response.json()
    last_id = response['last_id']
    videos = response['videos']

    for i, video in enumerate(videos):
        pass
        # print('---------------------------')
        # print(i,'*',video['title'])

    j = 1
    last_id = response['last_id']
    while last_id:
        print('**', last_id)
        total = str(j*60)
        response = requests.get(
            f"http://127.0.0.1:4200/api/category/music?lastid={last_id}&total={total}")
        response = response.json()
        last_id = response['last_id']
        j= j+1

        



except ParserError as e:
    print(e)
