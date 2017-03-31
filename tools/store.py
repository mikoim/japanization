import time
from copy import deepcopy
from datetime import datetime
from itertools import count
from random import randint
import json
import requests
from elasticsearch import Elasticsearch
from logging import getLogger
import logging
import redis

logging.basicConfig(level=logging.DEBUG)
logger = getLogger(__name__)


def is_success(body: dict) -> bool:
    return body[list(body.keys())[0]]['success']


def extract_data(body: dict) -> dict:
    return body[list(body.keys())[0]]['data']


def add_timestamp(body: dict) -> dict:
    t = deepcopy(body)
    t['timestamp'] = datetime.now()
    return t


def parse_data(body: dict) -> dict:
    return add_timestamp(extract_data(body))


def ownedgames() -> list:
    with open('me.json') as fp:
        data = json.load(fp)
        return [g['appid'] for g in data['response']['games']]


def diff():
    es = Elasticsearch()

    index = 'appdetails_new'

    test = es.search(index=index, doc_type='raw', body={
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "type": "game"
                        }
                    },
                    {
                        "match": {
                            "supported_languages": "Japanese"
                        }
                    }
                ],
                "must_not": [
                    {"match": {"genres.description": "Utilities"}}
                ]
            }
        },
        "_source": [
            "steam_appid",
            "name"
        ],
        "sort": [
            {
                "timestamp": "desc"
            }
        ],
        "size": 10000
    })

    da = list(set([x['_source']['steam_appid'] for x in test['hits']['hits']]))

    with open('jp.json') as ff:
        a = json.load(ff)
        b = [x['steam_app_id'] for x in a['results']]
        un = [x for x in da if x in b]
        print(un)
        print(len(un))
        print(len(da))


def is_registered(appid: int) -> bool:
    es = Elasticsearch()

    index = 'appdetails_new'

    test = es.search(index=index, doc_type='raw', body={
        "query": {
            "term": {
                "steam_appid": appid
            }
        },
        "size": 0
    })

    return test['hits']['total'] >= 1


if __name__ == '__main__':
    es = Elasticsearch()
    rs = redis.StrictRedis()

    index = 'appdetails_new'
    # es.indices.delete(index)
    # es.indices.create(index=index, ignore=400)

    games = []

    for appid in ownedgames():  # range(1223, 2000):
        key_skip = f'appdetails_{appid}_skip'

        if is_registered(appid) or rs.get(key_skip):
            logger.debug(f"appid:{appid} / skipped")
            continue

        time.sleep(4)

        r = requests.get('http://store.steampowered.com/api/appdetails', {
            'l': 'en', 'cc': 'jp', 'appids': appid
        })

        data = r.json()

        if r.status_code != 200 or data is None or not is_success(data):
            logger.error(f"appid:{appid} status_code:{r.status_code} / Can't fetch app data from Steam Store.")
            rs.setex(key_skip, 2592000, True)
            continue

        es.index(index=index, doc_type='raw', body=parse_data(data))
