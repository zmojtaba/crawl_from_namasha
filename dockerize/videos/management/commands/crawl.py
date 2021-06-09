from django.core.management.base import BaseCommand
import requests
from datetime import datetime 

from lxml.etree import ParserError
from ...models import Video, Category, Channel


class Command(BaseCommand):
    help = 'crawl videos from namasha web server'

    def handle(self, *args, **kwargs):
        catgories = ['sport', 'funny', 'animation', 'technology', 'vehicle',
                     'educational', 'music', 'news', '	animals', 'game', 'accidents', 'religious']# add متفرقه و تیزر تبلیغاتی to category

        
        for i, cat in enumerate(catgories):
                
            category = cat
            try:
                NextPage = True
                last_id = None
                page = 1
                while NextPage:
                    print(f'<----{category} page {page} is crawled!!! ----> ')
                    category_db = Category.objects.get(name=category)
                    if not last_id:
                        response = requests.get(
                            f"http://192.168.107.36:8010/api/category/{category}")
                    else:
                        response = requests.get(
                            f"http://192.168.107.36:8010/api/category/{category}?lastid={last_id}")

                    video_results = response.json()
                    if video_results['last_id'] != []:
                        last_id = video_results['last_id'][0]
                    else:
                        NextPage = False
                        print(f'<---- {category} crawl finished ---->')
                    videos = video_results['videos']
                    page += 1

                    for video in videos:
                        channel = Channel.objects.update_or_create(link=video['channel_link'], defaults={'title': video['channel_name']})[0]
                        if video.get('title'):
                            Video.objects.update_or_create(link=video['video_link'], defaults={
                                'title': video['title'],
                                'thumbnail':video['thumbnail'],
                                'category': category_db,
                                'channel': channel,
                                'duration': video['duration'],
                                'view_count': video['view_count'],
                                'publish_data': video['publish_date'],
                            })
                Category.objects.update_or_create(name=category, defaults= {
                    'last_crawl': datetime.now()
                })

                # return json.dumps(videos, indent=2)
            except ParserError as e:
                print(e)
