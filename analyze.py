"""Contains code to analyze data"""

from typing import List
from dataclasses import dataclass

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from song import Song
from instance import Instance

colorama_init()

@dataclass
class Options:
    """Stores options for data analysis"""
    results: int = 10
    show_values: bool = True

def most_listens(opts: Options = Options()) -> None:
    """Returns or prints a list of the most listened to songs"""

    top_n: List[Song] = []

    lowest_play_count: int = -1

    for track in Song.full_list():

        # if the list isn't full
        if len(top_n) < opts.results:
            top_n.append(track)
            top_n.sort(key=lambda s: s.plays(), reverse=True)
            lowest_play_count = top_n[-1].plays()
            continue

        if track.plays() > lowest_play_count:
            top_n.pop()
            top_n.append(track)
            top_n.sort(key=lambda s: s.plays(), reverse=True)
            lowest_play_count = top_n[-1].plays()
            continue

    print(f'{Fore.CYAN}{Style.BRIGHT}Most listened to songs of all time are :')
    for i, track in enumerate(top_n):
        print(f'{Fore.YELLOW}{(i + 1):>3}{Fore.RESET} : {Fore.CYAN}{Style.NORMAL}{track.plays():>3}{Fore.RESET} -> {Fore.LIGHTGREEN_EX}{track.title}{Fore.RESET} by {Fore.MAGENTA}{track.artist}{Style.RESET_ALL}')

def most_listens_past_year(opts: Options = Options()) -> None:
    """Returns or prints a list of the most listened to songs in the past year"""

    top_n: List[Song] = []

    lowest_play_count: int = -1

    for track in Song.full_list():

        # if the list isn't full
        if len(top_n) < opts.results:
            top_n.append(track)
            top_n.sort(key=lambda s: s.plays_past_year(), reverse=True)
            lowest_play_count = top_n[-1].plays_past_year()
            continue

        if track.plays_past_year() > lowest_play_count:
            top_n.pop()
            top_n.append(track)
            top_n.sort(key=lambda s: s.plays_past_year(), reverse=True)
            lowest_play_count = top_n[-1].plays_past_year()
            continue

    print(f'{Fore.CYAN}{Style.BRIGHT}Most listened to songs of the past year (since {Instance.ONE_YEAR_AGO}) are :')
    for i, track in enumerate(top_n):
        print(f'{Fore.YELLOW}{(i + 1):>3}{Fore.RESET} : {Fore.CYAN}{Style.NORMAL}{track.plays_past_year():>3}{Fore.RESET} -> {Fore.LIGHTGREEN_EX}{track.title}{Fore.RESET} by {Fore.MAGENTA}{track.artist}{Style.RESET_ALL}')

def get_total_listen_time(opts: Options = Options()) -> None:
    """Returns the total amount of time listening to Spotify"""
    total: int = 0
    for song in Instance.SONG_LIST:
        total += song.playtime

    print(f"{Fore.CYAN}{Style.BRIGHT}You've listened to spotify for {total/1000} seconds ever{Style.RESET_ALL}")

def get_total_listen_time_past_year(opts: Options = Options()) -> None:
    """Returns the total amount of time listening to Spotify"""
    total: int = 0
    for song in Instance.SONG_LIST:
        if song.this_year():
            total += song.playtime

    print(f"{Fore.CYAN}{Style.BRIGHT}You've listened to spotify for {total/1000} seconds this year{Style.RESET_ALL}")
