# Sharks Ice Schedule Sync Tool

A quick and dirty sync tool that will pull in all the games scheduled for your hockey teams at Sharks Ice San Jose,
Sharks Ice Fremont, and the NCWHL and add them to a Google calendar.

## Dependencies / Setup

Requires python 2.x and [pip](https://pypi.python.org/pypi/pip)

Run the following command (may need to use sudo depending on your system).
> pip install -r requirements.txt

Open the _config.cfg_ file and edit the teams property for your particular rink (comma separated, as they appear on the stat page)

## Running

You'll need to obtain client credentials for the app -- [follow the instructions provided by Google](https://github.com/googleapis/google-api-python-client/blob/master/docs/oauth-installed.md#creating-application-credentials)
and put the credentials (renamed to client_secret.json) in the root of the project.  Account access and app configuration has moved over to Google Cloud, so the process is slightly more complicated than it used to be.  Don't forget to configure your oauth consent screen to allow the `https://www.googleapis.com/auth/calendar` scope (scope reduction is an open TODO).

Then just run
> python ScheduleRipper.py --noauth_local_webserver

The first run will prompt you for authorization to your google account and ask which calendar you'd like to sync the
events to.  Every run afterwards will use the stored credentials and settings to run without intervention (making it
usable for cron jobs)

## To do:

- Add a connector for Ice Oasis' Google Calendar
