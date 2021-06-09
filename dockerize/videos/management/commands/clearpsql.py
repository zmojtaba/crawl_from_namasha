from django.core.management.base import BaseCommand
from ...models import Video, Category, Channel

class Command(BaseCommand):
    help = 'crawl videos from namasha web server'

    def handle(self, *args, **kwargs):
        channels = Channel.objects.all()

        for i,chann in enumerate(channels):
            print(chann.last_crawl)
            if chann.last_crawl is None :
                print(i)
                
            else:
                Channel.objects.filter(link=chann.link).update(last_crawl=None)
                print(f'{i} , {chann.title} is cleared!!')
                