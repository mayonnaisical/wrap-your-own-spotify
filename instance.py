"""listen instance data
"""

from typing import Self, List, Dict
from datetime import datetime, timedelta
from tqdm import tqdm

class Instance:
    """Contains data pertaining to each listening of a song"""

    SONG_LIST: List[Self] = []

    NOW: datetime = datetime(1,1,1)
    ONE_YEAR = timedelta(365)
    ONE_YEAR_AGO = datetime.now() - ONE_YEAR
    ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

    @classmethod
    def parse_data(cls, raw_data: List[Dict[str, int | bool | None]]) -> None:
        """Converts JSON song data into list of song Instance objects

        Args:
            raw_data (List[Dict[str, int | bool | None]]): List of JSON song data

        Returns:
            List[Song]: List of Song objects
        """

        for song_data in tqdm(raw_data):
            song: Instance = Instance(song_data)

            cls.SONG_LIST.append(song) # add to list

            if song.timestamp > cls.NOW: # check if its the latest one
                cls.NOW = song.timestamp

        cls.ONE_YEAR_AGO = cls.NOW - cls.ONE_YEAR

        cls.sort_list()

    @classmethod
    def sort_list(cls) -> None:
        """Sorts Instance.SONGLIST"""
        cls.SONG_LIST.sort(key=lambda s: s.timestamp, reverse=True)

    def __init__(self, raw) -> None:
        self._timestamp: datetime = datetime.strptime(raw["ts"][:-1],Instance.ISO_DATE_FORMAT)
        self._time_played: int = raw["ms_played"]
        self._title: str = raw["master_metadata_track_name"]
        self._artist: str = raw["master_metadata_album_artist_name"]
        self._album: str = raw["master_metadata_album_album_name"]
        self._uri: str = raw["spotify_track_uri"]
        self._start_reason: str = raw["reason_start"]
        self._end_reason: str = raw["reason_end"]
        self._shuffle: bool = raw["shuffle"]
        self._offline: bool = raw["offline"]
        self._offline_timestamp: int = raw["offline_timestamp"]
        self._incognito: bool = raw["incognito_mode"]

    def __repr__(self) -> str:
        return f'{self.title} by {self.artist}\nplayed at {self.timestamp} for {self.playtime} ms'

    def __str__(self) -> str:
        return f'{self.title} by {self.artist}\nplayed at {self.timestamp}'

    @property
    def uri(self) -> str:
        """Returns song URI"""
        return self._uri

    @property
    def timestamp(self) -> datetime:
        """Returns timestamp at which the song was played"""
        return self._timestamp

    @property
    def playtime(self) -> int:
        """Returns the length of time the song was played for in milliseconds"""
        return self._time_played

    @property
    def title(self) -> str:
        """Returns the title of the song"""
        return self._title

    @property
    def artist(self) -> str:
        """Returns the artist of the album on which the song appears"""
        return self._artist

    @property
    def album(self) -> str:
        """Returns the album on which the song appears"""
        return self._album

    @property
    def reason_start(self) -> str:
        """Returns the reason the song began playing"""
        return self._start_reason

    @property
    def reason_end(self) -> str:
        """Returns the reason the song ended playing"""
        return self._end_reason

    @property
    def shuffle(self) -> bool:
        """Returns whether or not the song was played on shuffle"""
        return self._shuffle

    @property
    def offline(self) -> bool:
        """Returns whether or not the song was played in offline mode"""
        return self._offline

    @property
    def incognito(self) -> bool:
        """Returns whether or not the song was played in private/incognito mode"""
        return self._incognito

    def this_year(self) -> bool:
        """Returns whether or not the song was played within
        a year of the most recently played song in the dataset"""
        return self._timestamp > Instance.ONE_YEAR_AGO
