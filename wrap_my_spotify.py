"""
Wraps your spotify, currently only implemented for complete data
"""

from typing import Dict, List
import glob
import json

from song import Song
from instance import Instance
from analyze import *

def load_file() -> List[Dict[str, int | bool | None]]:
    """Loads Spotify data from MyData\\endsong_#.json

    Returns:
        List[Dict[str, int | bool | None]]: Returns a list of JSON objects containing song data
    """

    songlist: List[Dict[str, int | bool | None]] = []

    for endsong_json in glob.glob('MyData/endsong_*.json'):
        with open(file=endsong_json, mode='r', encoding='utf-8') as endsong_file:
            songlist += (json.loads(endsong_file.read()))

    return songlist

def load() -> None:
    """Loads everything"""

    data: List[Dict[str, int | bool | None]]
    data = load_file()

    Instance.parse_data(data)
    Song.parse_data(Instance.SONG_LIST)

if __name__ == '__main__':

    load()

    opts: Options() = Options()

    opts.results = 50

    print()
    most_listens(opts=opts)
    print()
    most_listens_past_year(opts=opts)
    print()
    get_total_listen_time()
    print()
    get_total_listen_time_past_year()
