import json
import sys
from functools import reduce


def parse(filename) -> list:
    with open(filename) as fp:
        r = json.load(fp)
        appids = [x['appid'] for x in r['response']['games']]

    return appids


def main():
    appids = list(set(reduce(lambda a, b: a + b, [parse(x) for x in sys.argv[1:]])))

    print(json.dumps(
        {
            "response": {
                "game_count": len(appids),
                "games": [{'appid': x} for x in appids]
            }
        }
    ))


if __name__ == '__main__':
    main()
