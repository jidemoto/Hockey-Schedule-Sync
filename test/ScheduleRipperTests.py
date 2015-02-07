import unittest
from mock import Mock
from ScheduleRipper import CalendarManager
from datetime import datetime


class TestSearchResultParse(unittest.TestCase):
    def test_result_parse(self):
        # Tests:
        #   1. A normal entry (exists as expected)
        #   2. An entry that will be found based on the search and isn't something we're concerned with
        #   3. An entry missing its location entry (not just an empty string)
        #   4. An entry that's a game without a description
        #   5. An entry missing pretty much everything
        #   6. An entry missing a start time
        events = {
            u'items': [
                {
                    u'kind': 'calendar#event',
                    u'summary': u'Raptors @ Mermen at San Jose South',
                    u'description': u'Game#129699',
                    u'start': {
                        u'dateTime': u'2015-02-07T21:45:00-08:00',
                        u'timeZone': u'America/Los_Angeles'
                    },
                    u'location': u'1500 South 10th Street, San Jose, CA 95112'
                },

                {
                    u'kind': 'calendar#event',
                    u'summary': u'Board Game Night!',
                    u'description': u'Bring a game and have some fun!',
                    u'start': {
                        u'dateTime': u'2015-02-07T21:45:00-08:00',
                        u'timeZone': u'America/Los_Angeles'
                    },
                    u'location': u'Wherever'
                },
                {
                    u'kind': 'calendar#event',
                    u'summary': u'Board Game Night 2!',
                    u'description': u'Bring a game!',
                    u'start': {
                        u'dateTime': u'2015-02-07T21:45:00-08:00',
                        u'timeZone': u'America/Los_Angeles'
                    }
                },
                {
                    u'kind': 'calendar#event',
                    u'summary': u'Board Game Night 3!',
                    u'location': u'Wherever',
                    u'start': {
                        u'dateTime': u'2015-02-07T21:45:00-08:00',
                        u'timeZone': u'America/Los_Angeles'
                    }
                },
                {
                    u'kind': 'calendar#event',
                    u'summary': u'Board Game Night 3!'
                },
                {
                    u'kind': 'calendar#event',
                    u'summary': u'Office Softball Game!',
                    u'description': u'Game#1',
                    u'location': u''
                }
            ]
        }

        service = Mock()

        events_obj = Mock()
        list_mock = Mock()
        list_mock.execute = Mock(return_value=events)
        events_obj.list = Mock(return_value=list_mock)

        calendars = Mock()
        cal_exec_mock = Mock()
        cal_exec_mock.execute = Mock(return_value={
            u'timeZone': u'America/Los_Angeles'
        })
        calendars.get = Mock(return_value=cal_exec_mock)

        service.events = Mock(return_value=events_obj)
        service.calendars = Mock(return_value=calendars)

        manager = CalendarManager(service)
        games = manager.date_range_search("somecal@calendars.google.com", datetime(2014, 1, 1), datetime.now())
        self.assertEqual(1, len(games))


if __name__ == '__main__':
    unittest.main()
