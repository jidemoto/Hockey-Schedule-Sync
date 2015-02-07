import ConfigParser
import time
from datetime import datetime
from datetime import timedelta

from oauth2client.file import Storage
from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets

import os
import argparse
import httplib2
from apiclient import discovery
import pytz
from pytz import timezone
import NcwhlParser
import SharksIceParser

utc = pytz.utc


class Game:
    def __init__(self, gameid, game_time, rink, away, home, address, event_id=None):
        self.gameid = gameid
        self.date = game_time
        self.rink = rink
        self.address = address
        self.away = away
        self.home = home

        self.event_id = event_id

    def __str__(self):
        return 'Game %s at %s - %s. %s @ %s' % \
               (self.gameid,
                self.date.strftime('%a %b %d, %Y %I:%M%p'),
                self.rink, self.away, self.home)

    def __eq__(self, other):
        return (self.gameid == other.gameid and self.date == other.date and self.rink == other.rink and
                self.away == other.away and self.home == other.home and self.address == other.address)

    def __ne__(self, other):
        return not __eq__(self, other)


def convert_date_time(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S.000Z')


class CalendarManager:
    def __init__(self, service, reminder_minutes=45):
        self.service = service
        self.reminder_minutes = reminder_minutes

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
        if len(games) == 0:
            return

        # Sort the games by date so we can query for games on a range from today to the end of the listed game
        games = sorted(games, key=lambda g: g.date.timetuple())
        last_game_datetime = games[len(games) - 1].date
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
                        pass
                    else:
                        # Update the calendar entry
                        print 'Updating game', game.gameid
                        self.__update_game(current_game, game, calendar_name)

                    # Remove the game from the dictionary so we can check for unprocessed games
                    del current_games[game.gameid]
                else:
                    # Add game to the calendar
                    print 'Adding game', game.gameid
                    self.__create_game(game, calendar_name)
                    # print '\t',game
            else:
                # ignore game and delete from the dictionary
                print 'Ignoring game ' + str(game)
                if game.gameid in current_games:
                    del current_games[game.gameid]

        for game_id, game in current_games.iteritems():
            # Delete the game from the calendar
            print 'Deleting game', game.gameid
            self.__delete_game(game, calendar_name)

    def date_range_search(self, cal, start, end, text='Game#'):
        current_games = dict()
        page_token = None
        cal_tz = timezone(self.get_cal_timezone(cal))

        while True:
            events = self.service.events().list(calendarId=cal,
                                                pageToken=page_token,
                                                q=text,
                                                timeMin=convert_date_time(start),
                                                timeMax=convert_date_time(end)).execute()
            for event in events['items']:
                content = event.get('description')
                if 'description' in event and content.startswith('Game#') and 'summary' in event and 'start' in event:
                    start = event.get('start').get('dateTime')
                    title = event.get('summary')
                    print '\t%s: %s (%s)' % (title, content, start)
                    where = event.get('location', '')
                    game_number = content[content.find('#') + 1:]
                    sep = title.find('@')
                    sep2 = title.rfind(' at ')
                    away = title[:sep].strip()
                    home = title[sep + 1:sep2].strip()
                    rink = title[sep2 + 4:].strip()

                    if '+' in start:
                        plus = start.rfind('+')
                        start = start[:plus]
                    elif '-' in start:
                        minus = start.rfind('-')
                        start = start[:minus]
                    game_time = cal_tz.localize(datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')).astimezone(utc)
                    new_game = Game(game_number, game_time, rink, away, home, where, event)
                    current_games[game_number] = new_game

            page_token = events.get('nextPageToken')
            if not page_token:
                break

        return current_games

    def get_cal_timezone(self, calendar_id):
        calendar = self.service.calendars().get(calendarId=calendar_id).execute()
        return calendar['timeZone']

    # Credit to mattcaffeine for initial reminder and address code
    def __create_game(self, game, cal):
        title_text = game.away + ' @ ' + game.home + ' at ' + game.rink
        content_text = 'Game#' + game.gameid
        start_time = convert_date_time(game.date)
        end_time = convert_date_time(game.date + timedelta(hours=1, minutes=15))

        event = {
            'summary': title_text,
            'location': game.address,
            'description': content_text,
            'start': {
                'dateTime': start_time
            },
            'end': {
                'dateTime': end_time
            }
        }

        if self.reminder_minutes > 0:
            event['reminders'] = {
                'useDefault': 'false',
                'overrides': [
                    {
                        'method': 'popup',
                        'minutes': self.reminder_minutes
                    }
                ]
            }

        created_event = self.service.events().insert(calendarId=cal, body=event).execute()

        print 'Added event: %s' % (created_event['id'],)

        return created_event

    def __update_game(self, existing_game, new_game, cal):
        print 'Update game', existing_game
        self.__delete_game(existing_game, cal)
        self.__create_game(new_game, cal)

    def __delete_game(self, game, cal):
        self.service.events().delete(calendarId=cal, eventId=game.event_id['id']).execute()


def main():
    script_location = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(script_location, 'config.cfg')
    config = ConfigParser.ConfigParser(allow_no_value=True)
    config.read(config_file)

    iceurl = config.get('Sharks Ice San Jose', 'url')
    iceteams = config.get('Sharks Ice San Jose', 'teams')

    fremonticeurl = config.get('Sharks Ice Fremont', 'url')
    fremonticeteams = config.get('Sharks Ice Fremont', 'teams')

    ncwhl_url = config.get('NCWHL', 'url')
    ncwhl_teams = config.get('NCWHL', 'teams')

    games = []

    if len(iceteams) > 0:
        games.extend(SharksIceParser.parse_main_schedule(iceurl, [team.strip() for team in iceteams.split(',')]))

    if len(fremonticeteams) > 0:
        games.extend(SharksIceParser.parse_main_schedule(fremonticeurl,
                                                         [team.strip() for team in fremonticeteams.split(',')]))

    if len(ncwhl_teams) > 0:
        games.extend(NcwhlParser.rip_schedule(ncwhl_url, [team.strip() for team in ncwhl_teams.split(',')]))

    for game in sorted(games, key=lambda g: g.date):
        print game

    secrets_location = config.get('General', 'secrets_location')
    flow = flow_from_clientsecrets(os.path.join(script_location, secrets_location),
                                   scope='https://www.googleapis.com/auth/calendar',
                                   redirect_uri='urn:ietf:wg:oauth:2.0:oob')
    storage = Storage(os.path.join(script_location, 'credentials.dat'))
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        parser = argparse.ArgumentParser(parents=[tools.argparser])
        flags = parser.parse_args()
        credentials = tools.run_flow(flow, storage, flags)

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = discovery.build(serviceName='calendar', version='v3', http=http, developerKey='')
    manager = CalendarManager(service, config.getint('General', 'reminder_minutes'))

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


if __name__ == '__main__':
    main()
