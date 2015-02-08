from datetime import datetime
import re
import urllib
from BeautifulSoup import BeautifulSoup
import pytz
from pytz import timezone
from ParserUtilities import get_text_content

utc = pytz.utc
local_tz = timezone('America/Los_Angeles')

rink_addresses = {
    'San Jose North': '1500 South 10th Street, San Jose, CA 95112',
    'San Jose South': '1500 South 10th Street, San Jose, CA 95112',
    'San Jose East': '1500 South 10th Street, San Jose, CA 95112',
    'San Jose Center': '1500 South 10th Street, San Jose, CA 95112',
    'SAP Center': '525 West Santa Clara Street, San Jose, CA 95113',
    'Fremont': '44388 Old Warm Springs Boulevard, Fremont, CA 94538'
}


def parse_main_schedule(page, teams):
    raw = urllib.urlopen(page)
    doc = BeautifulSoup(raw.read())

    context = page[:page.rfind('/')]

    games = []

    for team in teams:
        anchor = doc.find('a', text=re.compile(team)).parent['href']
        print team, 'page:', anchor
        games.extend(__parse_team_schedule(context + '/' + anchor))

    return games


def __parse_team_schedule(anchor):
    from ScheduleRipper import Game

    games = []
    current_year = str(datetime.now().year)
    roll_year = False

    raw = urllib.urlopen(anchor)
    doc = BeautifulSoup(raw.read())

    game_rows = doc.find('table').findAll('tr')[2:]
    for game in game_rows:
        info = game.findAll('td')
        if len(info) > 0:
            # print info[0]
            game_num = get_text_content(info[0])

            starpos = game_num.find('*')
            if starpos >= 0:
                continue  # This will skip the processing of games that have already occured
            # gameNum = gameNum[:starpos]

            home_team = get_text_content(info[8])
            away_team = get_text_content(info[6])

            # This date is going to be set to 1900
            d = datetime.strptime(
                info[1].contents[0].replace('&nbsp;', '').strip() + ' ' + current_year + ' ' + info[2].contents[
                    0].replace('&nbsp;', '').strip(), '%a %b %d %Y %I:%M %p')
            if not roll_year and d.month == 1 and datetime.now().month > 6:
                roll_year = True

            if roll_year:
                d = d.replace(year=d.year + 1)

            d = local_tz.localize(d).astimezone(utc)
            rink = info[3].contents[0].replace('&nbsp;', '').strip()
            rink_address = rink_addresses.get(rink, '')
            games.append(Game(game_num, d, rink, away_team, home_team, rink_address))

    return games
