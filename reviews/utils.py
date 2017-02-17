import requests
from django.core.cache import cache


class SteamException(Exception):
    pass


class SteamStore(object):
    l = None
    cc = None

    def __init__(self, language='en', country='jp'):
        self.l = language
        self.cc = country

    def appdetails(self, app_id: int) -> dict:
        url = 'http://store.steampowered.com/api/appdetails'
        cache_key = 'appdetails_{:d}'.format(app_id)
        app_id_str = str(app_id)

        j = cache.get(cache_key)

        if not j:

            r = requests.get(url=url, params={'l': self.l, 'cc': self.cc, 'appids': app_id})

            if r.status_code != 200:
                raise SteamException('Steam API returned non-200 status')

            j = r.json()

            if app_id_str not in j or not j[app_id_str]['success']:
                raise SteamException('Steam API returned unexpected error')

            cache.set(cache_key, j, 1209600)

        return j[app_id_str]['data']

    @staticmethod
    def is_support_japanese(data: dict) -> bool:
        k = 'supported_languages'
        return k in data and 'Japanese' in data[k]

    @staticmethod
    def name(data: dict) -> str:
        return data['name']
