from typing import Optional
from fastapi import FastAPI
import requests
from lxml import etree
from lxml.etree import ParserError
from namasha_parser import get_elements, get_channel_elements

app = FastAPI()


@app.get('/api/category/{category}')
def crawl_category(category: str, lastid: Optional[str] = None):
    try:
        response = requests.get(
            f"https://www.namasha.com/playlist/{category}?lastid={lastid}")

        parser = etree.HTMLParser()
        html_dom = etree.HTML(response.text, parser)
        total_results = get_elements(html_dom)
        videos = total_results['results']
        last_id = total_results['last_id']
        return {'videos': videos, 'last_id': last_id}
    except ParserError as e:
        print(e)


@app.get('/api/channel/{channel}/')
def crawl_chanell(channel: str, lastid: Optional[str] = None):
    try:
        response = requests.get(
            f"https://www.namasha.com/{channel}?lastid={lastid}")
        parser = etree.HTMLParser()
        html_dom = etree.HTML(response.text, parser)
        total_results = get_channel_elements(html_dom)
        videos = total_results['results']
        last_id = total_results['last_id']
        return {'videos': videos, 'last_id': last_id}
    except ParserError as e:
        print(e)
