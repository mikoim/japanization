import json
import re

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError

from reviews.models import Review


class Command(BaseCommand):
    help = 'Sync remote reviews to local database'

    def add_arguments(self, parser):
        parser.add_argument('group_name', nargs='+', type=str)

    def handle(self, *args, **options):
        regex_app_id = re.compile('app/([0-9]+)/')

        for group_name in options['group_name']:
            start = 0

            while True:
                result = requests.get('http://steamcommunity.com/groups/{:s}/ajaxgetrecommendations/render/'
                                      .format(group_name),
                                      params={
                                          'query': '',
                                          'start': start
                                      })

                self.stderr.write(self.style.NOTICE(result.url))

                obj = json.loads(result.text)

                if not obj['success']:
                    self.stderr.write(self.style.ERROR(obj))
                    raise CommandError('Steam API returned unexpected error')

                results_html = BeautifulSoup(obj['results_html'], 'lxml')

                for product in results_html.find_all(class_='curation_app_block'):
                    steam_app_id = int(
                        regex_app_id.search(product.find(class_='curation_app_block_content').a['href']).group(1)
                    )
                    review_summary = product.find(class_='curation_app_block_blurb').get_text().strip()

                    try:
                        review_detail_link = product.find(class_='highlighted_recommendation_link').a['href']
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(e))
                        review_detail_link = ''

                    review = Review(
                        steam_app_id=steam_app_id,
                        review_summary=review_summary,
                        review_detail_link=review_detail_link,
                        localized_by_developer=False,
                        localized_by_community=False,
                        published=False
                    )
                    review.save()

                start += 10

                if start > obj['total_count']:
                    break
