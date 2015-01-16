import ConfigParser
import urllib
import re
import time
from datetime import datetime
from datetime import timedelta

import BeautifulSoup as bs
from BeautifulSoup import BeautifulSoup

from oauth2client.file import Storage
from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets

import argparse
import httplib2
from apiclient import discovery
import pytz
from tzlocal import get_localzone

utc = pytz.utc
local_tz = get_localzone()


class Game:
    def __init__(self, gameid, game_time, rink, away, home, event_id=None):
        self.gameid = gameid
        self.date = game_time
        self.rink = rink
        self.away = away
        self.home = home

        self.event_id = event_id

    def getDateTime(self):
        return self.date

    def getRink(self):
        return self.rink

    def getAway(self):
        return self.away

    def getHome(self):
        return self.home

    def set_event_id(self, event):
        self.event_id = event

    def get_event_id(self):
        return self.event_id

    def __str__(self):
        return 'Game %s at %s - %s. %s @ %s' % \
               (self.gameid,
                self.date.astimezone(local_tz).strftime('%a %b %d, %Y %I:%M%p'),
                self.rink, self.away, self.home)

    def __eq__(self, other):
        return self.gameid == other.gameid and self.date == other.date and self.rink == other.rink \
               and self.away == other.away and self.home == other.home

    def __ne__(self, other):
        return not __eq__(self, other)


class ScheduleRipper:
    def ripSharksIceMainSchedule(self, page, teams):
        raw = urllib.urlopen(page)
        doc = BeautifulSoup(raw.read())

        context = page[:page.rfind('/')]

        games = []

        for team in teams:
            anchor = doc.find('a', text=re.compile(team)).parent['href']
            print team, 'page:', anchor
            games.extend(self.ripSharksIceTeamSchedule(context + '/' + anchor))

        return games

    def ripSharksIceTeamSchedule(self, anchor):

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
                game_num = info[0].contents[0]
                if type(game_num) == bs.Tag and game_num.name == 'a':
                    game_num = game_num.contents[0]

                starpos = game_num.find('*')
                if starpos >= 0:
                    continue  # This will skip the processing of games that have already occured
                # gameNum = gameNum[:starpos]

                home_team = ''.join([self._get_text_content(x) for x in info[8].contents]).replace('&nbsp;', '').strip()
                away_team = ''.join([self._get_text_content(x) for x in info[6].contents]).replace('&nbsp;', '').strip()

                # This date is going to be set to 1900
                d = datetime.strptime(
                    info[1].contents[0].replace('&nbsp;', '').strip() + ' ' + current_year + ' ' + info[2].contents[
                        0].replace('&nbsp;', '').strip(), '%a %b %d %Y %I:%M %p')
                if not roll_year and d.month == 1 and datetime.now().month > 6:
                    roll_year = True

                if roll_year:
                    d = d.replace(year=d.year + 1)

                d = local_tz.localize(d).astimezone(utc)
                games.append(Game(game_num, d, info[3].contents[0].replace('&nbsp;', '').strip(), away_team, home_team))

        return games

    def _get_text_content(self, soupnode):
        if len(soupnode) > 1:
            return ''.join([self._get_text_content(child) for child in soupnode])
        else:
            if type(soupnode) == bs.Tag:
                return ''.join([self._get_text_content(content) for content in soupnode.contents])
            else:
                return soupnode


def convert_date_time(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S.000Z')


class CalendarManager:
    def __init__(self, service, timezone='America/Los_Angeles'):
        self.service = service
        self.timezone = timezone

    def get_calendars(self):
        page_token = None
        calendars = []
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                access_role_ = calendar_list_entry['accessRole']
                if access_role_ == 'owner' or access_role_ == 'writer':
                    calendars.append({'id': calendar_list_entry['id'], 'summary': calendar_list_entry['summary']})
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

        return calendars

    def sync(self, games, calendar_name):
        # perform sync here

        # Sort the games by date so we can query for games on a range from today to the end of the listed game
        games = sorted(games, key=lambda g: g.date.timetuple())
        last_game_datetime = games[len(games) - 1].getDateTime()
        last_game = (last_game_datetime + timedelta(days=5))
        today = datetime.now()  # TypeError: argument must be 9-item sequence, not float

        current_games = self.date_range_search(calendar_name, today, last_game)

        # Compare games:
        # If game not found: add it to the calendar and remove from dictionary
        # If game found and equal: Remove from dictionary and continue
        # If game in calendar but not found in game list: delete from calendar
        print "\n-- Summary of changes applied --"
        for game in games:
            if game.date.timetuple() >= time.localtime():
                if game.gameid in current_games:
                    current_game = current_games[game.gameid]
                    if current_game == game:
                        print 'Passing on game', game.gameid, '(Already exists)'
                        # print '\t',game
                        pass
                    else:
                        # Update the calendar entry
                        print 'Updating game', game.gameid
                        self._updateGame(current_game, game, calendar_name)
                    # print '\t',game

                    # Remove the game from the dictionary so we can check for unprocessed games
                    del current_games[game.gameid]
                else:
                    # Add game to the calendar
                    print 'Adding game', game.gameid
                    self._createGame(game, calendar_name)
                    # print '\t',game
            else:
                # ignore game and delete from the dictionary
                print 'Ignoring game ' + str(game)
                if game.gameid in current_games:
                    del current_games[game.gameid]

        for game_id, game in current_games.iteritems():
            # Delete the game from the calendar
            print 'Deleting game', game.gameid
            self._deleteGame(game, calendar_name)
        # print '\t',game
        return None

    def date_range_search(self, cal, start, end, text='Game#'):
        current_games = dict()
        page_token = None

        while True:
            events = self.service.events().list(calendarId=cal,
                                                pageToken=page_token,
                                                q=text,
                                                timeMin=convert_date_time(start),
                                                timeMax=convert_date_time(end)).execute()
            for event in events['items']:
                print '\t%s: %s (%s)' % (event['summary'], event['description'], event['start']['dateTime'])
                title = event['summary']
                content = event['description']
                game_number = content[content.find('#') + 1:]
                where = event['location']
                sep = title.find('@')
                away = title[:sep].strip()
                home = title[sep + 1:].strip()
                start = event['start']['dateTime']
                if '+' in start:
                    plus = start.rfind('+')
                    start = start[:plus]
                elif '-' in start:
                    minus = start.rfind('-')
                    start = start[:minus]
                game_time = local_tz.localize(datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')).astimezone(utc)
                new_game = Game(game_number, game_time, where, away, home, event)
                current_games[game_number] = new_game

            page_token = events.get('nextPageToken')
            if not page_token:
                break

        return current_games

    def _createGame(self, game, cal):
        title_text = game.away + ' @ ' + game.home
        content_text = 'Game#' + game.gameid
        start_time = convert_date_time(game.getDateTime())
        end_time = convert_date_time(game.getDateTime() + timedelta(hours=1, minutes=15))

        event = {
            'summary': title_text,
            'location': game.rink,
            'description': content_text,
            'start': {
                'dateTime': start_time,
                'timeZone': self.timezone
            },
            'end': {
                'dateTime': end_time,
                'timeZone': self.timezone
            }
        }

        created_event = self.service.events().insert(calendarId=cal, body=event).execute()

        print 'Added event: %s' % (created_event['id'],)

        return created_event

    def _updateGame(self, existing_game, new_game, cal):
        print 'Update game', existing_game
        self._deleteGame(existing_game, cal)
        self._createGame(new_game, cal)


    def _deleteGame(self, game, cal):
        self.service.events().delete(calendarId=cal, eventId=game.get_event_id()['id']).execute()


def main():
    config_file = 'config.cfg'
    config = ConfigParser.ConfigParser(allow_no_value=True)
    config.read(config_file)

    iceurl = config.get('Sharks Ice San Jose', 'url')
    iceteams = config.get('Sharks Ice San Jose', 'teams')

    fremonticeurl = config.get('Sharks Ice Fremont', 'url')
    fremonticeteams = config.get('Sharks Ice Fremont', 'teams')

    ripper = ScheduleRipper()

    games = []

    if len(iceteams) > 0:
        games.extend(ripper.ripSharksIceMainSchedule(iceurl, iceteams.split(',')))

    if len(fremonticeteams) > 0:
        games.extend(ripper.ripSharksIceMainSchedule(fremonticeurl, fremonticeteams.split(',')))

    for game in sorted(games, key=lambda game: game.date):
        print game

    try:
        flow = flow_from_clientsecrets('client_secret.json',
                                       scope='https://www.googleapis.com/auth/calendar',
                                       redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        storage = Storage('credentials.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            parser = argparse.ArgumentParser(parents=[tools.argparser])
            flags = parser.parse_args()
            credentials = tools.run_flow(flow, storage, flags)

        http = httplib2.Http()
        http = credentials.authorize(http)

        service = discovery.build(serviceName='calendar', version='v3', http=http, developerKey='')
        manager = CalendarManager(service)

        cal = config.get('Google Calendar', 'calendarid')
        if len(cal) == 0:
            print 'A calendar must be specified:'
            cals = manager.get_calendars()
            for i in range(len(cals)):
                print (i + 1), ': ', cals[i]['summary']
            while len(cal) == 0:
                temp = input('Select calendar to import events to: ')
                try:
                    temp = int(temp) - 1
                    if 0 <= temp < len(cals):
                        cal = cals[temp]['id']
                        config.set('Google Calendar', 'calendarid', cal)
                        with open(config_file, 'wb') as configfile:
                            config.write(configfile)
                except ValueError:
                    print 'Invalid selection'

        manager.sync(games, cal)
    finally:
        print 'wat'


if __name__ == '__main__':
    main()
