from datetime import datetime
from BeautifulSoup import BeautifulSoup
import urllib

import pytz
from tzlocal import get_localzone

utc = pytz.utc
local_tz = get_localzone()


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
                games.append(Game(num, converted_dt, rink, away, home))

    print 'Found', len(games), 'games for', teams
    return games

def main():
    for game in rip_schedule('http://ncwhl.com/static/schedules/Winter201415FullSchedule.html', ['R5']):
        print game

if __name__ == '__main__':
    main()