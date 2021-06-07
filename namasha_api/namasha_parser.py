import datetime
import convert_numbers
from lxml.etree import ParserError
from requests import NullHandler


class NamashaParser:
    def create_view_count(view_count):
        return int(convert_numbers.persian_to_english(view_count))

    def parser_publish_data(published_date):
        published_date = published_date.strip()

        if 'اندکی' in published_date:
            published_date = str(datetime.datetime.now())

        elif 'لحظاتی' in published_date:
            published_date = str(datetime.datetime.now())

        elif 'دقیقه' in published_date:
            published_date = str(datetime.datetime.now())

        elif 'ساعت' in published_date:
            published_date = str(datetime.datetime.now())

        elif 'دیروز' in published_date:
            published_date = str(datetime.datetime.now()-datetime.timedelta(1))
        elif 'روز' in published_date:
            day = int(convert_numbers.persian_to_english(
                published_date.split('روز پیش')[0]))
            published_date = str(datetime.datetime.now() -
                                 datetime.timedelta(day))
        elif 'ماه' in published_date:
            month = int(convert_numbers.persian_to_english(
                published_date.split('ماه پیش')[0]))
            published_date = str(datetime.datetime.now() -
                                 datetime.timedelta(month*30))

        elif 'پارسال' in published_date:
            published_date = str(datetime.datetime.now() -
                                 datetime.timedelta(365))

        elif 'سال' in published_date:
            year = int(convert_numbers.persian_to_english(
                published_date.split('سال پیش')[0]))
            published_date = str(datetime.datetime.now() -
                                 datetime.timedelta(year*365))

        else:
            published_date = 'there is some things else'

        return published_date

    def parser_duration(duration):
        total_duration = duration.split(':')
        if len(total_duration) == 2:
            duration = int(convert_numbers.persian_to_english(
                total_duration[0]))*60 + int(convert_numbers.persian_to_english(total_duration[1]))
        elif len(total_duration) == 3:
            duration = int(convert_numbers.persian_to_english(total_duration[0]))*3600 + int(
                convert_numbers.persian_to_english(total_duration[1]))*60 + int(convert_numbers.persian_to_english(total_duration[2]))

        return duration

    def create_result(title, thumbnail, video_link, channel_name, channel_link, duration, view_count, published_date, position):

        result = {"title": title,
                  "thumbnail": thumbnail,
                  "video_link": video_link,
                  "channel_name": channel_name,
                  "channel_link": channel_link,
                  "duration": duration,
                  "view_count": view_count,
                  "publish_date": published_date,
                  "position": position}

        return result

    def create_channel_result(title, thumbnail, video_link, duration, view_count, published_date, position):

        result = {"title": title,
                  "thumbnail": thumbnail,
                  "video_link": video_link,
                  "duration": duration,
                  "view_count": view_count,
                  "publish_date": published_date,
                  "position": position}

        return result


def get_elements(html_dom):
    try:
        video_results = html_dom.xpath(
            '//body//div[contains(@class, "thumbnail full-width")]')

        last_id = html_dom.xpath(
            '//body//button[contains(@id,"load-more-btn")]/@data-lid')

        results = []

        for index, video in enumerate(video_results):
            thumbnail = video.xpath(
                '//img[contains(@class, "thumbnail-image")]//@src')[index]

            title = video.xpath(
                '//h3[contains(@class, "thumbnail-video-title")]//text()')[index]

            video_link = video.xpath(
                '//a[contains(@class,"thumbnail-title")]//@href')[index]

            try:
                channel_name = video.xpath(
                    '//span[contains(@class,"thumbnail-channel-title")]//text()')[index]

                channel_link = video.xpath(
                    '//a[contains(@class,"clamp-text")]/@href')[index]
            except:
                pass
            duration = video.xpath(
                '//span[contains(@class,"time-stamp")]//text()')[index]

            view_date = video.xpath(
                '//span[contains(@class,"d-inline font-size-xs font-weight-light font-weight-lg-medium text-dynamic-half-dark")]//text()')

            view_count = NamashaParser.create_view_count(view_date[2*index])

            published_date = view_date[(2*index)+1]

            position = index

            published_date = NamashaParser.parser_publish_data(published_date)

            duration = NamashaParser.parser_duration(duration)

            result = NamashaParser.create_result(title,
                                                 thumbnail,
                                                 video_link,
                                                 channel_name,
                                                 channel_link,
                                                 duration,
                                                 view_count,
                                                 published_date,
                                                 position)

            results.append(result)
        return {'results': results, 'last_id': last_id}
    except ParserError as e:
        print(e)


def get_channel_elements(html_dom):
    try:
        video_results = html_dom.xpath(
            '//body//div[contains(@class, "thumbnail full-width")]')

        last_id = html_dom.xpath(
            '//body//button[contains(@id,"load-more-btn")]/@data-lid')

        results = []

        for index, video in enumerate(video_results):
            thumbnail = video.xpath(
                '//img[contains(@class, "thumbnail-image")]//@src')[index]

            title = video.xpath(
                '//h3[contains(@class, "thumbnail-video-title")]//text()')[index]

            video_link = video.xpath(
                '//a[contains(@class,"thumbnail-title")]//@href')[index]

            duration = video.xpath(
                '//span[contains(@class,"time-stamp")]//text()')[index]

            view_date = video.xpath(
                '//span[contains(@class,"d-inline font-size-xs font-weight-light font-weight-lg-medium text-dynamic-half-dark")]//text()')

            view_count = NamashaParser.create_view_count(view_date[2*index])

            published_date = view_date[(2*index)+1]

            position = index

            published_date = NamashaParser.parser_publish_data(published_date)

            duration = NamashaParser.parser_duration(duration)

            result = NamashaParser.create_channel_result(title,
                                                         thumbnail,
                                                         video_link,
                                                         duration,
                                                         view_count,
                                                         published_date,
                                                         position)

            results.append(result)
        return {'results': results, 'last_id': last_id}
    except ParserError as e:
        print(e)
