"""data for individual songs
"""

from typing import Dict, Self, List
from datetime import datetime, timedelta
from tqdm import tqdm

from instance import Instance
from tf import TF

class Song:
    """Data for each unique song listened to"""

    ALL_SONGS: Dict[str, Self] = {}

    @classmethod
    def parse_data(cls, json: List[Dict[str, int | bool | None]]) -> None:
        """Parses JSON object

        Args:
            raw_data (List[Dict[str, int | bool | None]]): _description_
        """

        for i in tqdm(json):
            if i.uri not in cls.ALL_SONGS:
                cls.ALL_SONGS[i.uri] = Song(i)
            cls.ALL_SONGS[i.uri].listen(i)

    @classmethod
    def print_songs(cls) -> None:
        """Prints all songs"""
        for song in cls.ALL_SONGS.values():
            print(f'{song}')

        print(cls.unique_songs())

    @classmethod
    def full_list(cls) -> List[Self]:
        """Returns a list of every Song"""
        return cls.ALL_SONGS.values()

    @classmethod
    def unique_songs(cls) -> int:
        """Returns the amount of unique songs listened to"""
        return len(cls.full_list())

    def __init__(self, i: Instance) -> None:
        self._uri: str = i.uri
        self._title: str = i.title
        self._artist: str = i.artist
        self._album: str = i.album

        self._plays: List[datetime] = []            # list of timestamps
        self._durations: List[int] = []             # list of time played
        self._start_reasons: Dict[str, int] = {}    # dict of start reasons
        self._end_reasons: Dict[str, int] = {}      # dict of end reasons
        self._shuffles: TF = TF()                   # shuffle true/falses
        self._incognitos: TF = TF()                 # incognito true/falses
        self._offlines: TF = TF()                   # offline true/falses

    def __str__(self) -> str:
        return f'{self.title} by {self.artist}'

    def __repr__(self) -> str:
        return f'{self.uri} : {self.title} by {self.artist}\n'

    def listen(self, instance: Instance) -> None:
        """Records one Instance of a Song

        Args:
            instance (Instance): Instance of the song to listen to
        """

        # failsafe in case the wrong song is listened to
        if instance.uri != self.uri:
            return

        self._plays.append(instance.timestamp)
        self._durations.append(instance.playtime)

        if instance.reason_start not in self._start_reasons:
            self._start_reasons[instance.reason_start] = 0
        self._start_reasons[instance.reason_start] += 1

        if instance.reason_end not in self._end_reasons:
            self._end_reasons[instance.reason_end] = 0
        self._end_reasons[instance.reason_end] += 1


        if instance.shuffle:
            self._shuffles.incr_t()
        else:
            self._shuffles.incr_f()

        if instance.incognito:
            self._incognitos.incr_t()
        else:
            self._incognitos.incr_f()

        if instance.offline:
            self._offlines.incr_t()
        else:
            self._offlines.incr_f()

    @property
    def uri(self) -> str:
        """Returns a song's spotify URI"""
        return self._uri

    @property
    def title(self) -> str:
        """Returns a song's title"""
        return self._title

    @property
    def artist(self) -> str:
        """Returns a song's artist"""
        return self._artist

    @property
    def album(self) -> str:
        """Returns a song's album"""
        return self._album

    @property
    def plays_list(self) -> List[datetime]:
        """Returns a list of every time the song was played"""
        return self._plays

    @property
    def durations(self) -> List[int]:
        """Returns a list of how long the song was listened to each time"""
        return self._durations

    @property
    def start_reasons(self) -> Dict[str, int]:
        """Returns a collection of why the song was started and how many times each"""
        return self._start_reasons

    @property
    def end_reasons(self) -> Dict[str, int]:
        """Returns a collection of why the song ended and how many times each"""
        return self._end_reasons

    def total_time_played(self) -> timedelta:
        """Returns the total playtime for the Song"""
        return sum(self.durations)

    def plays(self) -> int:
        """Returns the amount of times the song was played"""
        return len(self.plays_list)

    def total_time_played_past_year(self) -> timedelta:
        """Returns the total playtime for the Song in the past year"""
        total: int = 0
        days_and_durations = zip(self.plays_list, self.durations)

        for date, duration in days_and_durations:
            if Instance.ONE_YEAR_AGO < date:
                total += duration

        return total

    def plays_past_year(self) -> int:
        """Returns the amount of times the song was played in the past year"""
        return len([x for x in self.plays_list if x > Instance.ONE_YEAR_AGO])

    def avg_time_played(self) -> timedelta:
        """Returns the average duration the song was played for"""
        return self.total_time_played() / self.plays()

    def first_play(self) -> datetime:
        """Returns the first time the song was played"""
        return min(self.plays_list)

    def last_play(self) -> datetime:
        """Returns the most recent time the song was played"""
        return max(self.plays_list)
