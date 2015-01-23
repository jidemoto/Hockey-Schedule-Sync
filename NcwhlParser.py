from datetime import datetime
from BeautifulSoup import BeautifulSoup
import urllib

import pytz
from pytz import timezone

utc = pytz.utc
local_tz = timezone('America/Los_Angeles')

rink_addresses = {
    'Belmont': '815 Old County Road, Belmont, CA 94002',
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
            home = cells[7].contents[0]
            away = cells[8].contents[0]
            rink = cells[5].contents[0]
            d = cells[3].contents[0]
            t = cells[4].contents[0]
            num = cells[1].contents[0]

            if home in teams or away in teams:
                dt = datetime.combine(datetime.strptime(d, '%d-%b-%y').date(),
                                      datetime.strptime(t, '%I:%M %p').time())
                converted_dt = local_tz.localize(dt).astimezone(utc)
                rink_address = ''
                if rink in rink_addresses:
                    rink_address = rink_address[rink]
                games.append(Game(num, converted_dt, rink, away, home, rink_address))

    print 'Found', len(games), 'games for', teams
    return games