from datetime import datetime
from BeautifulSoup import BeautifulSoup
import urllib
from ParserUtilities import get_text_content

import pytz
from pytz import timezone

utc = pytz.utc
local_tz = timezone('America/Los_Angeles')

rink_addresses = {
    'Oakland': '519 18th St, Oakland, CA 94612',
    'Vallco': '10123 N Wolfe Rd, Cupertino, CA 95014',
    'Ice Oasis': '3140 Bay Road, Redwood City, CA 94063',
    'Fremont': '44388 Old Warm Springs Boulevard, Fremont, CA 94538'
}


def rip_schedule(page, teams):
    from ScheduleRipper import Game

    games = []
    raw = urllib.urlopen(page)
    doc = BeautifulSoup(raw.read())

    rows = doc.find('table').findAll('tr')
    print 'Found', len(rows), 'rows'
    for row in rows:
        cells = row.findAll('td')
        if len(cells) > 8 and len(cells[7]) > 0 and len(cells[8]) > 0:
            home = get_text_content(cells[7])
            away = get_text_content(cells[8])
            rink = get_text_content(cells[5])
            d = get_text_content(cells[3])
            t = get_text_content(cells[4])
            num = get_text_content(cells[1])

            if home in teams or away in teams:
                dt = datetime.combine(datetime.strptime(d, '%d-%b-%y').date(),
                                      datetime.strptime(t, '%I:%M %p').time())
                converted_dt = local_tz.localize(dt).astimezone(utc)
                rink_address = rink_addresses.get(rink, '')
                games.append(Game(num, converted_dt, rink, away, home, rink_address))

    print 'Found', len(games), 'games for', teams
    return games
