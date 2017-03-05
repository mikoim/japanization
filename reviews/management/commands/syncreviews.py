import re

import requests
from bs4 import BeautifulSoup
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from reviews.models import Review

STATUS_TABLE = {
    '有志日本語化': [False, True],
    '公式日本語化': [True, False],
    '実は日本語対応済': [True, False],
    '公式パッチ利用': [True, False],
    '公式対応': [True, False],
    '公式訳利用': [False, False],
    '注意喚起': [False, False],
}


class Command(BaseCommand):
    help = 'Sync remote reviews to local database'

    def add_arguments(self, parser):
        parser.add_argument('group_name', nargs='+', type=str)

    def handle(self, *args, **options):
        regex_app_id = re.compile('app/([0-9]+)/')

        for group_name in options['group_name']:
            start = 0

            while True:
                url = 'http://steamcommunity.com/groups/{:s}/ajaxgetrecommendations/render/'.format(group_name)
                cache_key = 'ajaxgetrecommendations_{:s}_{:d}'.format(group_name, start)

                obj = cache.get(cache_key)

                if not obj:
                    res = requests.get(url, params={
                        'query': '',
                        'start': start
                    })

                    obj = res.json()

                    if not obj['success']:
                        self.stderr.write(self.style.ERROR(obj))
                        raise CommandError('Steam API returned unexpected error')

                    cache.set(cache_key, obj, 60 * 60)

                results_html = BeautifulSoup(obj['results_html'], 'lxml')

                for product in results_html.find_all(class_='curation_app_block'):
                    steam_app_id = int(
                        regex_app_id.search(product.find(class_='curation_app_block_content').a['href']).group(1)
                    )
                    review_summary = product.find(class_='curation_app_block_blurb').get_text().strip()

                    try:
                        review_detail_link = product.find(class_='highlighted_recommendation_link').a['href']
                    except Exception:  # If it doesn't have link, fills empty.
                        review_detail_link = ''

                    try:
                        Review.objects.create(
                            steam_app_id=steam_app_id,
                            review_detail_link=review_detail_link,
                            **self._parse_review(review_summary),
                        )
                    except IntegrityError as e:
                        self.stderr.write(self.style.ERROR(e))

                start += 10

                if start > obj['total_count']:
                    break

    @staticmethod
    def _parse_review(text: str) -> dict:
        review_summary = re.sub('^"|"$', '', text)

        localization_status = review_summary.split(']')[0].replace('[', '')
        localized_by_developer = False
        localized_by_community = False

        if localization_status in STATUS_TABLE:
            (localized_by_developer, localized_by_community) = STATUS_TABLE[localization_status]
            review_summary = review_summary.replace('[{:s}]'.format(localization_status), '')

        return {
            'localization_status': localization_status,
            'localized_by_developer': localized_by_developer,
            'localized_by_community': localized_by_community,
            'review_summary': review_summary,
        }
