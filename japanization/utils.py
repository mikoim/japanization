import requests
from bs4 import BeautifulSoup
from django.core.cache import cache


def privileged_members(group_name: str) -> list:
    key = 'privileged_members_{:s}'.format(group_name)
    members = cache.get(key)

    if not members:
        members = __privileged_members(group_name)
        cache.set(key, members, 60 * 60)

    return members


def __privileged_members(group_name: str) -> list:
    res = requests.get('http://steamcommunity.com/groups/{:s}/members'.format(group_name), {
        'content_only': True
    })

    if res.status_code is not 200:
        raise SteamScraperError('Can\'t retrieve group members page')

    members = parse_privileged_member_names(res.text)

    return [steam_id_by_name(m) for m in members]


def steam_id_by_name(name: str) -> list:
    key = 'steam_id_by_name_{:s}'.format(name)
    steam_id = cache.get(key)

    if not steam_id:
        steam_id = __steam_id_by_name(name)
        cache.set(key, steam_id, 60 * 60 * 24 * 30)

    return steam_id


def __steam_id_by_name(name: str) -> str:
    res = requests.get('http://steamcommunity.com/id/{:s}'.format(name), {
        'xml': 1
    })

    if res.status_code is not 200:
        raise SteamScraperError('Can\'t retrieve user profile')

    return parse_steam_id(res.text)


def parse_steam_id(xml: str) -> str:
    root = BeautifulSoup(xml, "lxml-xml")
    return str(root.find('steamID64').contents[0])


def parse_privileged_member_names(html: str) -> list:
    root = BeautifulSoup(html, 'lxml')
    members_child = root.find_all('div', class_='rank_icon')
    members = [m.parent.find('a', class_='linkFriend').get('href').split('/')[-1] for m in members_child]
    return members


class SteamScraperError(Exception):
    pass
