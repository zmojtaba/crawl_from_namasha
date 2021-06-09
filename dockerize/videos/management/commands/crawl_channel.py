from django.core.management.base import BaseCommand
import requests
from datetime import datetime
from lxml.etree import ParserError
from ...models import Channel_Video, Channel



class Command(BaseCommand):
    help = "crawl videos from namasha member's channel"

    def handle(self, *args, **kwargs):

        all_channel = Channel.objects.all()
        for i, chann in enumerate(all_channel):
            if chann.last_crawl is None:
                channel_api_link = chann.link.split('.com/')[-1]
                Channel.objects.filter(link = chann.link).update(last_crawl=datetime.now())
                print('****',chann.last_crawl)
                    
                
                try:
                    NextPage = True
                    last_id = None
                    page = 1
                    while NextPage:
                        print(f'<----{channel_api_link} page {page} is crawled!!! ----> ')
                        if not last_id:
                            response = requests.get(
                                f"http://192.168.107.36:8010/api/channel/{channel_api_link}")
                        else:
                            response = requests.get(
                                f"http://192.168.107.36:8010/api/channel/{channel_api_link}?lastid={last_id}")
                        

                        video_results = response.json()
                        if video_results['last_id'] != []:
                            last_id = video_results['last_id'][0]
                        else:
                            NextPage = False
                            print(f'<---- {channel_api_link} crawl finished ---->')
                        print(video_results['last_id'])
                        videos = video_results['videos']
                        page += 1

                        for video in videos:
                            if video.get('title'):
                                
                                
                                Channel_Video.objects.update_or_create(link=video['video_link'], defaults={
                                    'title': video['title'],
                                    'thumbnail':video['thumbnail'],
                                    'channel': chann,
                                    'duration': video['duration'],
                                    'view_count': video['view_count'],
                                    'publish_data': video['publish_date'],
                                })
                    
                    # return json.dumps(videos, indent=2)
                except ParserError as e:
                    print(e)
