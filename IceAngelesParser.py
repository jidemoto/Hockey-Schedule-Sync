from datetime import datetime
import urllib
import re
from BeautifulSoup import BeautifulSoup
import pytz
from pytz import timezone
import hashlib
from ParserUtilities import get_text_content

utc = pytz.utc
local_tz = timezone('America/Los_Angeles')


def parse_main_schedule(page, teams):
    raw = urllib.urlopen(page)
    doc = BeautifulSoup(raw.read())

    context = page[:page.rfind('/')]

    league_links = [anchor['href'] for anchor in doc.find(id='middle').findAll('a')]
    games = []
    for league_link in league_links:
        games.extend(__parse_league_schedule(context + '/' + league_link, teams))

    return games


def __make_regex_str(teams):
    return '(' + '|'.join(teams) + ')' + '\s*(\(.*\))?'


def __parse_league_schedule(anchor, teams):
    from ScheduleRipper import Game

    games = []

    raw = urllib.urlopen(anchor)
    doc = BeautifulSoup(raw.read())
    team_matcher = re.compile(__make_regex_str(teams))

    game_rows = doc.find(id='middle').find('table').findAll('tr')
    current_game_number = 1
    for row in game_rows:
        info = row.findAll('td')
        # We'll ignore a row if the time cell is empty (Can't have a datetime for a game without a time!)
        if len(info) > 0 and len(get_text_content(info[2])) > 0:
            home_team = get_text_content(info[3])
            away_team = get_text_content(info[4])

            # Figure out which team we're matching against and skip if neither team is one we're looking for
            matched = team_matcher.match(home_team)
            if not matched:
                matched = team_matcher.match(away_team)
            if matched:
                matched_team = matched.group(0)
                # Generate a "unique" ID that we can use against existing entries for the game id
                # This will help us differentiate between games for two different teams
                game_number = hashlib.md5(matched_team + str(current_game_number)).hexdigest()

                parsed_date = datetime.strptime(get_text_content(info[1]), '%m/%d/%Y').date()
                parsed_time = datetime.strptime(get_text_content(info[2]), '%I:%M%p').time()
                d = datetime.combine(parsed_date, parsed_time)
                d = local_tz.localize(d).astimezone(utc)
                games.append(Game(game_number, d, 'Ice Angeles', away_team, home_team,
                                  '23770 Western Ave, Harbor City, California'))
                current_game_number += 1

    return games

