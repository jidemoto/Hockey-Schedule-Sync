import unittest
import SharksIceParser
import datetime


def dummy_open(url):
    if url == 'http://stats.liahl.org/display-stats.php?league=1':
        return DummyUrl(main_html)
    elif url == 'http://stats.liahl.org/display-schedule.php?team=2051&season=30&tlev=0&tseq=0&league=1':
        return DummyUrl(team_html)
    elif url == 'http://stats.liahl.org/display-schedule.php?team=2046&season=30&tlev=0&tseq=0&league=1':
        return DummyUrl(team_rollover_html)
    else:
        raise RuntimeError('The URL requested was not expected')


class SharksIceParserTests(unittest.TestCase):
    def runTest(self):
        SharksIceParser.urllib.urlopen = dummy_open
        games = SharksIceParser.parse_main_schedule('http://stats.liahl.org/display-stats.php?league=1', ['Mermen'])
        self.assertEqual(len(games), 3)
        self.assertEqual(games[0].rink, 'San Jose South')
        self.assertEqual(games[0].away, 'Raptors')
        self.assertEqual(games[0].home, 'Mermen')
        self.assertEqual(games[0].gameid, '129699')

        self.assertEqual(games[1].rink, 'San Jose East')
        self.assertEqual(games[1].away, 'Mermen')
        self.assertEqual(games[1].home, 'Red Dogs')
        self.assertEqual(games[1].gameid, '129748')

        self.assertEqual(games[2].rink, 'San Jose North')
        self.assertEqual(games[2].away, 'Mermen')
        self.assertEqual(games[2].home, 'Mavericks')
        self.assertEqual(games[2].gameid, '129760')


class SharksIceParserTestYearRollover(unittest.TestCase):
    def runTest(self):
        SharksIceParser.urllib.urlopen = dummy_open
        SharksIceParser.datetime = TestDateTime
        # datetime.datetime = TestDateTime
        games = SharksIceParser.parse_main_schedule('http://stats.liahl.org/display-stats.php?league=1',
                                                    ['Time Lords'])
        self.assertEqual(len(games), 2)
        self.assertEqual(games[0].date.year, 2010)
        self.assertEqual(games[0].date.day, 28)
        self.assertEqual(games[0].date.month, 12)
        self.assertEqual(games[0].date.hour, 1)
        self.assertEqual(games[0].date.minute, 15)
        self.assertEqual(games[1].date.year, 2011)
        self.assertEqual(games[1].date.month, 1)
        self.assertEqual(games[1].date.day, 5)
        self.assertEqual(games[1].date.hour, 7)
        self.assertEqual(games[1].date.minute, 15)


class TestDateTime(datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime.datetime(2010, 10, 31)


class DummyUrl:
    def __init__(self, text):
        self.text = text

    def read(self):
        return self.text

main_html = '''
<style type="text/css">
//<!--
body {  font-family: Arial, Helvetica, sans-serif; font-size: 10pt}
th   {  font-family: Arial, Helvetica, sans-serif; font-size: 10pt;
        font-weight: bold; background-color: #D3DCE3;}
td   {  font-family: Arial, Helvetica, sans-serif; font-size: 10pt;}
form   {  font-family: Arial, Helvetica, sans-serif; font-size: 10pt}
h1b   {  font-family: Verdana, Arial, Helvetica, sans-serif;
         font-size: 16pt; font-weight: bold}
A:link    {  font-family: Arial, Helvetica, sans-serif;
         font-size: 10pt; text-decoration: none; color: blue}
A:visited {  font-family: Arial, Helvetica, sans-serif;
         font-size: 10pt; text-decoration: none; color: blue}
A:hover   {  font-family: Arial, Helvetica, sans-serif;
         font-size: 10pt; text-decoration: underline; color: red}
A:link.nav {  font-family: Verdana, Arial, Helvetica, sans-serif;
         color: #000000}
A:visited.nav {  font-family: Verdana, Arial, Helvetica, sans-serif;
         color: #000000}
A:hover.nav {  font-family: Verdana, Arial, Helvetica, sans-serif; color: red;}
.nav {  font-family: Verdana, Arial, Helvetica, sans-serif; color: #000000}

//-->
</style>

<body text="#000000" vlink="#1111aa" link="#0000ff" bgcolor="ffffff">
<center><a href="http://siahl.org">SIAHL Captains Web Site</a></center><br><center><a href="display-archives.php?league=1">Archives</a></center><br><center><table border=0><TR><TH colspan=7>SIAHL@SJ</th></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=56>Senior A</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=56&season=30&conf=0">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=56&league=1&season=30&conf=0">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=323&season=30&tlev=0&tseq=0&league=1">Americans </a></td><td align=center>15</td><td align=center>11</td><td align=center>3</td><td align=center>1</td><td align=center>0</td><td align=center>23</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=310&season=30&tlev=0&tseq=0&league=1">Pager Flakes </a></td><td align=center>14</td><td align=center>11</td><td align=center>3</td><td align=center>0</td><td align=center>0</td><td align=center>22</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=1391&season=30&tlev=0&tseq=0&league=1">Zoom Imaging Solutions </a></td><td align=center>15</td><td align=center>4</td><td align=center>10</td><td align=center>1</td><td align=center>0</td><td align=center>9</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2272&season=30&tlev=0&tseq=0&league=1">Staches </a></td><td align=center>14</td><td align=center>2</td><td align=center>12</td><td align=center>0</td><td align=center>0</td><td align=center>4</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=1>Senior B</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=1&season=30&conf=0">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=1&league=1&season=30&conf=0">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2070&season=30&tlev=0&tseq=0&league=1">Blues </a></td><td align=center>15</td><td align=center>10</td><td align=center>3</td><td align=center>1</td><td align=center>1</td><td align=center>22</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=215&season=30&tlev=0&tseq=0&league=1">Dung Beetle </a></td><td align=center>15</td><td align=center>9</td><td align=center>3</td><td align=center>2</td><td align=center>1</td><td align=center>21</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=3069&season=30&tlev=0&tseq=0&league=1">Ghost Trees </a></td><td align=center>14</td><td align=center>6</td><td align=center>6</td><td align=center>2</td><td align=center>0</td><td align=center>14</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=667&season=30&tlev=0&tseq=0&league=1">Bums </a></td><td align=center>16</td><td align=center>5</td><td align=center>9</td><td align=center>1</td><td align=center>1</td><td align=center>12</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=1831&season=30&tlev=0&tseq=0&league=1">Shower Time </a></td><td align=center>16</td><td align=center>5</td><td align=center>10</td><td align=center>0</td><td align=center>1</td><td align=center>11</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=61>Senior BB</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=61&season=30&conf=0">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=61&league=1&season=30&conf=0">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2611&season=30&tlev=0&tseq=0&league=1">Samepage.io Collaborators  </a></td><td align=center>14</td><td align=center>12</td><td align=center>2</td><td align=center>0</td><td align=center>0</td><td align=center>24</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2711&season=30&tlev=0&tseq=0&league=1">Battalion </a></td><td align=center>13</td><td align=center>9</td><td align=center>2</td><td align=center>1</td><td align=center>1</td><td align=center>20</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=843&season=30&tlev=0&tseq=0&league=1">Diablos </a></td><td align=center>14</td><td align=center>8</td><td align=center>5</td><td align=center>1</td><td align=center>0</td><td align=center>17</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=17&season=30&tlev=0&tseq=0&league=1">SJ Disaster </a></td><td align=center>13</td><td align=center>7</td><td align=center>5</td><td align=center>1</td><td align=center>0</td><td align=center>15</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2603&season=30&tlev=0&tseq=0&league=1">SJ Moose </a></td><td align=center>13</td><td align=center>7</td><td align=center>5</td><td align=center>1</td><td align=center>0</td><td align=center>15</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=321&season=30&tlev=0&tseq=0&league=1">Scorpions </a></td><td align=center>14</td><td align=center>5</td><td align=center>6</td><td align=center>1</td><td align=center>2</td><td align=center>13</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=273&season=30&tlev=0&tseq=0&league=1">Palmer West </a></td><td align=center>12</td><td align=center>6</td><td align=center>6</td><td align=center>0</td><td align=center>0</td><td align=center>12</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2951&season=30&tlev=0&tseq=0&league=1">The Vallco Menace </a></td><td align=center>13</td><td align=center>5</td><td align=center>6</td><td align=center>2</td><td align=center>0</td><td align=center>12</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=799&season=30&tlev=0&tseq=0&league=1">Time to Score </a></td><td align=center>13</td><td align=center>5</td><td align=center>7</td><td align=center>1</td><td align=center>0</td><td align=center>11</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=210&season=30&tlev=0&tseq=0&league=1">Black Mambas </a></td><td align=center>14</td><td align=center>5</td><td align=center>8</td><td align=center>0</td><td align=center>1</td><td align=center>11</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=363&season=30&tlev=0&tseq=0&league=1">Puck Heads </a></td><td align=center>13</td><td align=center>5</td><td align=center>7</td><td align=center>1</td><td align=center>0</td><td align=center>11</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2719&season=30&tlev=0&tseq=0&league=1">The Others </a></td><td align=center>13</td><td align=center>5</td><td align=center>7</td><td align=center>0</td><td align=center>1</td><td align=center>11</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=443&season=30&tlev=0&tseq=0&league=1">Soldiers </a></td><td align=center>13</td><td align=center>5</td><td align=center>7</td><td align=center>1</td><td align=center>0</td><td align=center>11</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=2>Senior C</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=2&season=30&conf=0">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=2&league=1&season=30&conf=0">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=800&season=30&tlev=0&tseq=0&league=1">Norcal Leafs </a></td><td align=center>13</td><td align=center>11</td><td align=center>2</td><td align=center>0</td><td align=center>0</td><td align=center>22</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=296&season=30&tlev=0&tseq=0&league=1">Isotopes </a></td><td align=center>14</td><td align=center>5</td><td align=center>8</td><td align=center>0</td><td align=center>1</td><td align=center>11</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=1832&season=30&tlev=0&tseq=0&league=1">Reapers </a></td><td align=center>14</td><td align=center>5</td><td align=center>9</td><td align=center>0</td><td align=center>0</td><td align=center>10</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=199&season=30&tlev=0&tseq=0&league=1">Lost Eskimos </a></td><td align=center>13</td><td align=center>5</td><td align=center>8</td><td align=center>0</td><td align=center>0</td><td align=center>10</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2044&season=30&tlev=0&tseq=0&league=1">Buttered Muffins </a></td><td align=center>14</td><td align=center>5</td><td align=center>9</td><td align=center>0</td><td align=center>0</td><td align=center>10</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=3>Senior CC</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=3&season=30&conf=0">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=3&league=1&season=30&conf=0">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=3070&season=30&tlev=0&tseq=0&league=1">Sasquatch </a></td><td align=center>13</td><td align=center>10</td><td align=center>3</td><td align=center>0</td><td align=center>0</td><td align=center>20</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=38&season=30&tlev=0&tseq=0&league=1">OHC </a></td><td align=center>13</td><td align=center>9</td><td align=center>2</td><td align=center>1</td><td align=center>1</td><td align=center>20</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2613&season=30&tlev=0&tseq=0&league=1">Junkies </a></td><td align=center>13</td><td align=center>8</td><td align=center>3</td><td align=center>2</td><td align=center>0</td><td align=center>18</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2979&season=30&tlev=0&tseq=0&league=1">2 for Elmo-ing  </a></td><td align=center>13</td><td align=center>8</td><td align=center>4</td><td align=center>1</td><td align=center>0</td><td align=center>17</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=19&season=30&tlev=0&tseq=0&league=1">Bandits 2 </a></td><td align=center>14</td><td align=center>6</td><td align=center>8</td><td align=center>0</td><td align=center>0</td><td align=center>12</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=31&season=30&tlev=0&tseq=0&league=1">Cisco Metros </a></td><td align=center>13</td><td align=center>5</td><td align=center>6</td><td align=center>0</td><td align=center>2</td><td align=center>12</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=297&season=30&tlev=0&tseq=0&league=1">Grizzlies </a></td><td align=center>14</td><td align=center>5</td><td align=center>8</td><td align=center>0</td><td align=center>1</td><td align=center>11</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=841&season=30&tlev=0&tseq=0&league=1">Jets </a></td><td align=center>13</td><td align=center>5</td><td align=center>8</td><td align=center>0</td><td align=center>0</td><td align=center>10</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=633&season=30&tlev=0&tseq=0&league=1">Shocker </a></td><td align=center>13</td><td align=center>4</td><td align=center>7</td><td align=center>2</td><td align=center>0</td><td align=center>10</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=534&season=30&tlev=0&tseq=0&league=1">Blueline </a></td><td align=center>13</td><td align=center>3</td><td align=center>9</td><td align=center>0</td><td align=center>1</td><td align=center>7</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=4>Senior CCC</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=4&season=30&conf=0">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=4&league=1&season=30&conf=0">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2051&season=30&tlev=0&tseq=0&league=1">Mermen </a></td><td align=center>15</td><td align=center>12</td><td align=center>2</td><td align=center>1</td><td align=center>0</td><td align=center>25</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=64&season=30&tlev=0&tseq=0&league=1">Raptors </a></td><td align=center>15</td><td align=center>8</td><td align=center>6</td><td align=center>0</td><td align=center>1</td><td align=center>17</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2602&season=30&tlev=0&tseq=0&league=1">Mavericks </a></td><td align=center>15</td><td align=center>7</td><td align=center>6</td><td align=center>1</td><td align=center>1</td><td align=center>16</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=881&season=30&tlev=0&tseq=0&league=1">Charlie Browns </a></td><td align=center>14</td><td align=center>6</td><td align=center>6</td><td align=center>1</td><td align=center>1</td><td align=center>14</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=15&season=30&tlev=0&tseq=0&league=1">Red Dogs </a></td><td align=center>14</td><td align=center>6</td><td align=center>7</td><td align=center>0</td><td align=center>1</td><td align=center>13</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=325&season=30&tlev=0&tseq=0&league=1">Blackhawks </a></td><td align=center>15</td><td align=center>2</td><td align=center>10</td><td align=center>3</td><td align=center>0</td><td align=center>7</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=48>Senior CCCC</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=48&season=30&conf=0">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=48&league=1&season=30&conf=0">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=455&season=30&tlev=0&tseq=0&league=1">Southsiders </a></td><td align=center>14</td><td align=center>10</td><td align=center>3</td><td align=center>1</td><td align=center>0</td><td align=center>21</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=43&season=30&tlev=0&tseq=0&league=1">Rangers </a></td><td align=center>14</td><td align=center>9</td><td align=center>4</td><td align=center>1</td><td align=center>0</td><td align=center>19</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=21&season=30&tlev=0&tseq=0&league=1">Fighting Icecocks </a></td><td align=center>14</td><td align=center>8</td><td align=center>6</td><td align=center>0</td><td align=center>0</td><td align=center>16</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2712&season=30&tlev=0&tseq=0&league=1">Breaking Chad </a></td><td align=center>14</td><td align=center>7</td><td align=center>6</td><td align=center>0</td><td align=center>1</td><td align=center>15</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2709&season=30&tlev=0&tseq=0&league=1">Bad Moose </a></td><td align=center>14</td><td align=center>6</td><td align=center>6</td><td align=center>2</td><td align=center>0</td><td align=center>14</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=4&season=30&tlev=0&tseq=0&league=1">Senior Sharks </a></td><td align=center>14</td><td align=center>5</td><td align=center>8</td><td align=center>1</td><td align=center>0</td><td align=center>11</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2601&season=30&tlev=0&tseq=0&league=1">Norcal Crossover </a></td><td align=center>14</td><td align=center>5</td><td align=center>8</td><td align=center>0</td><td align=center>1</td><td align=center>11</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=22&season=30&tlev=0&tseq=0&league=1">Ice Dogs </a></td><td align=center>14</td><td align=center>2</td><td align=center>9</td><td align=center>3</td><td align=center>0</td><td align=center>7</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=5>Senior DD</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=5&season=30&conf=0">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=5&league=1&season=30&conf=0">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=804&season=30&tlev=0&tseq=0&league=1">Grinders </a></td><td align=center>12</td><td align=center>9</td><td align=center>3</td><td align=center>0</td><td align=center>0</td><td align=center>18</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=42&season=30&tlev=0&tseq=0&league=1">Usual Suspects </a></td><td align=center>12</td><td align=center>9</td><td align=center>3</td><td align=center>0</td><td align=center>0</td><td align=center>18</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=216&season=30&tlev=0&tseq=0&league=1">U.S.eh </a></td><td align=center>13</td><td align=center>8</td><td align=center>4</td><td align=center>1</td><td align=center>0</td><td align=center>17</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2257&season=30&tlev=0&tseq=0&league=1">French Toast </a></td><td align=center>13</td><td align=center>7</td><td align=center>5</td><td align=center>0</td><td align=center>1</td><td align=center>15</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=564&season=30&tlev=0&tseq=0&league=1">Double Secret Probation </a></td><td align=center>13</td><td align=center>7</td><td align=center>5</td><td align=center>0</td><td align=center>1</td><td align=center>15</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2036&season=30&tlev=0&tseq=0&league=1">Raccoons </a></td><td align=center>12</td><td align=center>6</td><td align=center>4</td><td align=center>1</td><td align=center>1</td><td align=center>14</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=340&season=30&tlev=0&tseq=0&league=1">NVIDIA </a></td><td align=center>13</td><td align=center>6</td><td align=center>6</td><td align=center>0</td><td align=center>1</td><td align=center>13</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=96&season=30&tlev=0&tseq=0&league=1">Chiefs </a></td><td align=center>12</td><td align=center>5</td><td align=center>5</td><td align=center>1</td><td align=center>1</td><td align=center>12</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=1225&season=30&tlev=0&tseq=0&league=1">Hooters Bay Area </a></td><td align=center>12</td><td align=center>5</td><td align=center>7</td><td align=center>0</td><td align=center>0</td><td align=center>10</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=1467&season=30&tlev=0&tseq=0&league=1">Sabres </a></td><td align=center>12</td><td align=center>4</td><td align=center>7</td><td align=center>1</td><td align=center>0</td><td align=center>9</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=28&season=30&tlev=0&tseq=0&league=1">Bandits 1 </a></td><td align=center>12</td><td align=center>3</td><td align=center>9</td><td align=center>0</td><td align=center>0</td><td align=center>6</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2293&season=30&tlev=0&tseq=0&league=1">LinkedIn </a></td><td align=center>12</td><td align=center>3</td><td align=center>9</td><td align=center>0</td><td align=center>0</td><td align=center>6</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=7>Senior DDD</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=7&season=30&conf=0">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=7&league=1&season=30&conf=0">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2953&season=30&tlev=0&tseq=0&league=1">Good Guys </a></td><td align=center>13</td><td align=center>11</td><td align=center>1</td><td align=center>0</td><td align=center>1</td><td align=center>23</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=306&season=30&tlev=0&tseq=0&league=1">Cereal Killers </a></td><td align=center>12</td><td align=center>10</td><td align=center>2</td><td align=center>0</td><td align=center>0</td><td align=center>20</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=206&season=30&tlev=0&tseq=0&league=1">Total Chaos </a></td><td align=center>12</td><td align=center>9</td><td align=center>3</td><td align=center>0</td><td align=center>0</td><td align=center>18</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2035&season=30&tlev=0&tseq=0&league=1">Flying Hellfish </a></td><td align=center>12</td><td align=center>7</td><td align=center>4</td><td align=center>1</td><td align=center>0</td><td align=center>15</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2033&season=30&tlev=0&tseq=0&league=1">Benchwarmers </a></td><td align=center>13</td><td align=center>7</td><td align=center>5</td><td align=center>1</td><td align=center>0</td><td align=center>15</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=1791&season=30&tlev=0&tseq=0&league=1">Green Horns </a></td><td align=center>13</td><td align=center>7</td><td align=center>6</td><td align=center>0</td><td align=center>0</td><td align=center>14</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=303&season=30&tlev=0&tseq=0&league=1">Code Blue </a></td><td align=center>13</td><td align=center>6</td><td align=center>6</td><td align=center>1</td><td align=center>0</td><td align=center>13</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2713&season=30&tlev=0&tseq=0&league=1">Norwin Tech </a></td><td align=center>12</td><td align=center>5</td><td align=center>6</td><td align=center>0</td><td align=center>1</td><td align=center>11</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=636&season=30&tlev=0&tseq=0&league=1">Hogzilla </a></td><td align=center>13</td><td align=center>5</td><td align=center>7</td><td align=center>1</td><td align=center>0</td><td align=center>11</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2954&season=30&tlev=0&tseq=0&league=1">Pork Chop Express </a></td><td align=center>13</td><td align=center>5</td><td align=center>8</td><td align=center>0</td><td align=center>0</td><td align=center>10</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2980&season=30&tlev=0&tseq=0&league=1">Cougars </a></td><td align=center>13</td><td align=center>5</td><td align=center>8</td><td align=center>0</td><td align=center>0</td><td align=center>10</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2977&season=30&tlev=0&tseq=0&league=1">Philosoraptors </a></td><td align=center>13</td><td align=center>4</td><td align=center>8</td><td align=center>0</td><td align=center>1</td><td align=center>9</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=34&season=30&tlev=0&tseq=0&league=1">Wolverines 1 </a></td><td align=center>12</td><td align=center>3</td><td align=center>9</td><td align=center>0</td><td align=center>0</td><td align=center>6</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=1380&season=30&tlev=0&tseq=0&league=1">Mooseknuckles </a></td><td align=center>12</td><td align=center>2</td><td align=center>10</td><td align=center>0</td><td align=center>0</td><td align=center>4</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=8>Senior DDDD East</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=8&season=30&conf=4">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=8&league=1&season=30&conf=4">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=880&season=30&tlev=0&tseq=0&league=1">Icequakes </a></td><td align=center>12</td><td align=center>9</td><td align=center>2</td><td align=center>1</td><td align=center>0</td><td align=center>19</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2062&season=30&tlev=0&tseq=0&league=1">Hooligans </a></td><td align=center>12</td><td align=center>8</td><td align=center>3</td><td align=center>0</td><td align=center>1</td><td align=center>17</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=811&season=30&tlev=0&tseq=0&league=1">Leftovers </a></td><td align=center>12</td><td align=center>7</td><td align=center>3</td><td align=center>1</td><td align=center>1</td><td align=center>16</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=84&season=30&tlev=0&tseq=0&league=1">Mighty Schmucks </a></td><td align=center>12</td><td align=center>7</td><td align=center>4</td><td align=center>0</td><td align=center>1</td><td align=center>15</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=567&season=30&tlev=0&tseq=0&league=1">Pacific Predators  </a></td><td align=center>12</td><td align=center>6</td><td align=center>4</td><td align=center>1</td><td align=center>1</td><td align=center>14</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2715&season=30&tlev=0&tseq=0&league=1">The Originals </a></td><td align=center>12</td><td align=center>5</td><td align=center>3</td><td align=center>3</td><td align=center>1</td><td align=center>14</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=53&season=30&tlev=0&tseq=0&league=1">Stampede </a></td><td align=center>12</td><td align=center>5</td><td align=center>5</td><td align=center>1</td><td align=center>1</td><td align=center>12</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=47&season=30&tlev=0&tseq=0&league=1">Bullfrogs </a></td><td align=center>12</td><td align=center>4</td><td align=center>7</td><td align=center>0</td><td align=center>1</td><td align=center>9</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2605&season=30&tlev=0&tseq=0&league=1">Panty Hosers </a></td><td align=center>12</td><td align=center>3</td><td align=center>8</td><td align=center>1</td><td align=center>0</td><td align=center>7</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=3066&season=30&tlev=0&tseq=0&league=1">Norcal Crossover Batalion </a></td><td align=center>12</td><td align=center>2</td><td align=center>9</td><td align=center>0</td><td align=center>1</td><td align=center>5</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=8>Senior DDDD West</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=8&season=30&conf=5">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=8&league=1&season=30&conf=5">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=789&season=30&tlev=0&tseq=0&league=1">Rampage  </a></td><td align=center>12</td><td align=center>12</td><td align=center>0</td><td align=center>0</td><td align=center>0</td><td align=center>24</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2046&season=30&tlev=0&tseq=0&league=1">Time Lords </a></td><td align=center>12</td><td align=center>9</td><td align=center>3</td><td align=center>0</td><td align=center>0</td><td align=center>18</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=46&season=30&tlev=0&tseq=0&league=1">Blade Runners </a></td><td align=center>12</td><td align=center>7</td><td align=center>4</td><td align=center>1</td><td align=center>0</td><td align=center>15</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=469&season=30&tlev=0&tseq=0&league=1">Margarita Madness </a></td><td align=center>12</td><td align=center>7</td><td align=center>5</td><td align=center>0</td><td align=center>0</td><td align=center>14</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2297&season=30&tlev=0&tseq=0&league=1">Team America </a></td><td align=center>12</td><td align=center>6</td><td align=center>5</td><td align=center>1</td><td align=center>0</td><td align=center>13</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=70&season=30&tlev=0&tseq=0&league=1">K-Wings </a></td><td align=center>12</td><td align=center>6</td><td align=center>5</td><td align=center>0</td><td align=center>1</td><td align=center>13</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2969&season=30&tlev=0&tseq=0&league=1">Natural Disasters </a></td><td align=center>12</td><td align=center>4</td><td align=center>5</td><td align=center>2</td><td align=center>1</td><td align=center>11</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2034&season=30&tlev=0&tseq=0&league=1">Wolves </a></td><td align=center>12</td><td align=center>4</td><td align=center>6</td><td align=center>0</td><td align=center>2</td><td align=center>10</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=946&season=30&tlev=0&tseq=0&league=1">The Rebellion </a></td><td align=center>12</td><td align=center>2</td><td align=center>10</td><td align=center>0</td><td align=center>0</td><td align=center>4</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2955&season=30&tlev=0&tseq=0&league=1">Money Shots </a></td><td align=center>12</td><td align=center>1</td><td align=center>11</td><td align=center>0</td><td align=center>0</td><td align=center>2</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=57>Senior DDDDD West</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=57&season=30&conf=5">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=57&league=1&season=30&conf=5">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=1796&season=30&tlev=0&tseq=0&league=1">Benders </a></td><td align=center>13</td><td align=center>9</td><td align=center>2</td><td align=center>2</td><td align=center>0</td><td align=center>20</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2270&season=30&tlev=0&tseq=0&league=1">Red Solo Cups </a></td><td align=center>13</td><td align=center>9</td><td align=center>4</td><td align=center>0</td><td align=center>0</td><td align=center>18</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=566&season=30&tlev=0&tseq=0&league=1">Dunder Mifflin </a></td><td align=center>13</td><td align=center>8</td><td align=center>3</td><td align=center>1</td><td align=center>1</td><td align=center>18</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=805&season=30&tlev=0&tseq=0&league=1">SJ Dragons </a></td><td align=center>13</td><td align=center>8</td><td align=center>3</td><td align=center>1</td><td align=center>1</td><td align=center>18</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2267&season=30&tlev=0&tseq=0&league=1">Raccoons 2 </a></td><td align=center>13</td><td align=center>7</td><td align=center>3</td><td align=center>2</td><td align=center>1</td><td align=center>17</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=87&season=30&tlev=0&tseq=0&league=1">CineLux Theatres </a></td><td align=center>13</td><td align=center>7</td><td align=center>5</td><td align=center>1</td><td align=center>0</td><td align=center>15</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=806&season=30&tlev=0&tseq=0&league=1">Chieftains </a></td><td align=center>13</td><td align=center>6</td><td align=center>7</td><td align=center>0</td><td align=center>0</td><td align=center>12</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=299&season=30&tlev=0&tseq=0&league=1">OHC 2 </a></td><td align=center>13</td><td align=center>4</td><td align=center>9</td><td align=center>0</td><td align=center>0</td><td align=center>8</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2974&season=30&tlev=0&tseq=0&league=1">Wolfpack </a></td><td align=center>13</td><td align=center>2</td><td align=center>8</td><td align=center>1</td><td align=center>2</td><td align=center>7</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=1798&season=30&tlev=0&tseq=0&league=1">Goombas </a></td><td align=center>13</td><td align=center>1</td><td align=center>11</td><td align=center>0</td><td align=center>1</td><td align=center>3</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=57>Senior DDDDD East</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=57&season=30&conf=4">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=57&league=1&season=30&conf=4">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=3063&season=30&tlev=0&tseq=0&league=1">Hooligans 2 </a></td><td align=center>14</td><td align=center>11</td><td align=center>2</td><td align=center>0</td><td align=center>1</td><td align=center>23</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2290&season=30&tlev=0&tseq=0&league=1">Rampage 2 </a></td><td align=center>13</td><td align=center>10</td><td align=center>3</td><td align=center>0</td><td align=center>0</td><td align=center>20</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=13&season=30&tlev=0&tseq=0&league=1">Team X </a></td><td align=center>13</td><td align=center>9</td><td align=center>4</td><td align=center>0</td><td align=center>0</td><td align=center>18</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2064&season=30&tlev=0&tseq=0&league=1">Jackalopes </a></td><td align=center>13</td><td align=center>8</td><td align=center>4</td><td align=center>0</td><td align=center>1</td><td align=center>17</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=1201&season=30&tlev=0&tseq=0&league=1">Angry Beavers </a></td><td align=center>13</td><td align=center>7</td><td align=center>6</td><td align=center>0</td><td align=center>0</td><td align=center>14</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2956&season=30&tlev=0&tseq=0&league=1">Total Chaos 2 </a></td><td align=center>13</td><td align=center>5</td><td align=center>7</td><td align=center>0</td><td align=center>1</td><td align=center>11</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=1372&season=30&tlev=0&tseq=0&league=1">Night Hawks </a></td><td align=center>13</td><td align=center>4</td><td align=center>9</td><td align=center>0</td><td align=center>0</td><td align=center>8</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2978&season=30&tlev=0&tseq=0&league=1">Tyrannosaurs </a></td><td align=center>13</td><td align=center>3</td><td align=center>10</td><td align=center>0</td><td align=center>0</td><td align=center>6</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2032&season=30&tlev=0&tseq=0&league=1">Buck Tooth Angry Dolphins </a></td><td align=center>13</td><td align=center>2</td><td align=center>11</td><td align=center>0</td><td align=center>0</td><td align=center>4</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=9>Senior E</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=9&season=30&conf=0">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=9&league=1&season=30&conf=0">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=1198&season=30&tlev=0&tseq=0&league=1">Red Bulls 2 </a></td><td align=center>12</td><td align=center>8</td><td align=center>3</td><td align=center>0</td><td align=center>1</td><td align=center>17</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2037&season=30&tlev=0&tseq=0&league=1">Army of Darkness </a></td><td align=center>12</td><td align=center>8</td><td align=center>3</td><td align=center>0</td><td align=center>1</td><td align=center>17</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2052&season=30&tlev=0&tseq=0&league=1">Peter North Stars </a></td><td align=center>12</td><td align=center>8</td><td align=center>3</td><td align=center>1</td><td align=center>0</td><td align=center>17</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2610&season=30&tlev=0&tseq=0&league=1">Irish Car Bombs </a></td><td align=center>12</td><td align=center>8</td><td align=center>4</td><td align=center>0</td><td align=center>0</td><td align=center>16</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2612&season=30&tlev=0&tseq=0&league=1">Happy Hour </a></td><td align=center>12</td><td align=center>7</td><td align=center>5</td><td align=center>0</td><td align=center>0</td><td align=center>14</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2291&season=30&tlev=0&tseq=0&league=1">Rampage 3 </a></td><td align=center>12</td><td align=center>6</td><td align=center>4</td><td align=center>1</td><td align=center>1</td><td align=center>14</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=79&season=30&tlev=0&tseq=0&league=1">Gang Green </a></td><td align=center>12</td><td align=center>5</td><td align=center>7</td><td align=center>0</td><td align=center>0</td><td align=center>10</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=639&season=30&tlev=0&tseq=0&league=1">Shenanigans </a></td><td align=center>12</td><td align=center>4</td><td align=center>7</td><td align=center>0</td><td align=center>1</td><td align=center>9</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=543&season=30&tlev=0&tseq=0&league=1">Beer </a></td><td align=center>12</td><td align=center>4</td><td align=center>8</td><td align=center>0</td><td align=center>0</td><td align=center>8</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2063&season=30&tlev=0&tseq=0&league=1">Ice Breakers </a></td><td align=center>12</td><td align=center>1</td><td align=center>11</td><td align=center>0</td><td align=center>0</td><td align=center>2</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=10>Senior EE East</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=10&season=30&conf=4">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=10&league=1&season=30&conf=4">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=638&season=30&tlev=0&tseq=0&league=1">Ice Force </a></td><td align=center>12</td><td align=center>8</td><td align=center>2</td><td align=center>0</td><td align=center>2</td><td align=center>18</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=1834&season=30&tlev=0&tseq=0&league=1">Red Dragons </a></td><td align=center>12</td><td align=center>8</td><td align=center>2</td><td align=center>1</td><td align=center>1</td><td align=center>18</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2041&season=30&tlev=0&tseq=0&league=1">Fighting Icecocks 2 </a></td><td align=center>12</td><td align=center>7</td><td align=center>4</td><td align=center>0</td><td align=center>1</td><td align=center>15</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=1199&season=30&tlev=0&tseq=0&league=1">Chieftains 2 </a></td><td align=center>12</td><td align=center>7</td><td align=center>5</td><td align=center>0</td><td align=center>0</td><td align=center>14</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2708&season=30&tlev=0&tseq=0&league=1">Irish Car Bombs 2 </a></td><td align=center>12</td><td align=center>7</td><td align=center>5</td><td align=center>0</td><td align=center>0</td><td align=center>14</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2963&season=30&tlev=0&tseq=0&league=1">Falcons </a></td><td align=center>12</td><td align=center>6</td><td align=center>4</td><td align=center>1</td><td align=center>1</td><td align=center>14</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2720&season=30&tlev=0&tseq=0&league=1">Honey Badgers </a></td><td align=center>12</td><td align=center>6</td><td align=center>5</td><td align=center>0</td><td align=center>1</td><td align=center>13</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2604&season=30&tlev=0&tseq=0&league=1">The Avengers </a></td><td align=center>12</td><td align=center>5</td><td align=center>6</td><td align=center>0</td><td align=center>1</td><td align=center>11</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2958&season=30&tlev=0&tseq=0&league=1">Black Knights </a></td><td align=center>12</td><td align=center>3</td><td align=center>9</td><td align=center>0</td><td align=center>0</td><td align=center>6</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=86&season=30&tlev=0&tseq=0&league=1">Tsunami </a></td><td align=center>12</td><td align=center>2</td><td align=center>10</td><td align=center>0</td><td align=center>0</td><td align=center>4</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=10>Senior EE West</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=10&season=30&conf=5">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=10&league=1&season=30&conf=5">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2967&season=30&tlev=0&tseq=0&league=1">Beerbears on Ice </a></td><td align=center>13</td><td align=center>9</td><td align=center>3</td><td align=center>0</td><td align=center>1</td><td align=center>19</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2971&season=30&tlev=0&tseq=0&league=1">FiveHoleNinjas </a></td><td align=center>12</td><td align=center>8</td><td align=center>4</td><td align=center>0</td><td align=center>0</td><td align=center>16</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=32&season=30&tlev=0&tseq=0&league=1">Habs </a></td><td align=center>12</td><td align=center>7</td><td align=center>4</td><td align=center>1</td><td align=center>0</td><td align=center>15</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2714&season=30&tlev=0&tseq=0&league=1">Red Hawks </a></td><td align=center>13</td><td align=center>6</td><td align=center>5</td><td align=center>2</td><td align=center>0</td><td align=center>14</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=879&season=30&tlev=0&tseq=0&league=1">Destroyers </a></td><td align=center>12</td><td align=center>6</td><td align=center>6</td><td align=center>0</td><td align=center>0</td><td align=center>12</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2039&season=30&tlev=0&tseq=0&league=1">3rd Line Scrubs </a></td><td align=center>12</td><td align=center>5</td><td align=center>5</td><td align=center>0</td><td align=center>2</td><td align=center>12</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=1196&season=30&tlev=0&tseq=0&league=1">Flying Pandas </a></td><td align=center>12</td><td align=center>5</td><td align=center>6</td><td align=center>1</td><td align=center>0</td><td align=center>11</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=202&season=30&tlev=0&tseq=0&league=1">Ice Monkeys </a></td><td align=center>12</td><td align=center>1</td><td align=center>11</td><td align=center>0</td><td align=center>0</td><td align=center>2</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=49>Senior EEE</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=49&season=30&conf=0">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=49&league=1&season=30&conf=0">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2965&season=30&tlev=0&tseq=0&league=1">Irish Car Bombs 3 </a></td><td align=center>12</td><td align=center>11</td><td align=center>1</td><td align=center>0</td><td align=center>0</td><td align=center>22</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2266&season=30&tlev=0&tseq=0&league=1">Night Hawks 2 </a></td><td align=center>12</td><td align=center>10</td><td align=center>1</td><td align=center>1</td><td align=center>0</td><td align=center>21</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2964&season=30&tlev=0&tseq=0&league=1">Los Tiburones </a></td><td align=center>12</td><td align=center>10</td><td align=center>2</td><td align=center>0</td><td align=center>0</td><td align=center>20</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2960&season=30&tlev=0&tseq=0&league=1">Swashpucklers </a></td><td align=center>12</td><td align=center>9</td><td align=center>3</td><td align=center>0</td><td align=center>0</td><td align=center>18</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2073&season=30&tlev=0&tseq=0&league=1">Buffalo Wings </a></td><td align=center>12</td><td align=center>8</td><td align=center>3</td><td align=center>1</td><td align=center>0</td><td align=center>17</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=341&season=30&tlev=0&tseq=0&league=1">Mug Shots </a></td><td align=center>12</td><td align=center>6</td><td align=center>6</td><td align=center>0</td><td align=center>0</td><td align=center>12</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=471&season=30&tlev=0&tseq=0&league=1">Ravens </a></td><td align=center>12</td><td align=center>5</td><td align=center>7</td><td align=center>0</td><td align=center>0</td><td align=center>10</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2962&season=30&tlev=0&tseq=0&league=1">Hectors Pool Service </a></td><td align=center>12</td><td align=center>4</td><td align=center>6</td><td align=center>1</td><td align=center>1</td><td align=center>10</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=218&season=30&tlev=0&tseq=0&league=1">Phase Matrix </a></td><td align=center>12</td><td align=center>2</td><td align=center>9</td><td align=center>1</td><td align=center>0</td><td align=center>5</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=3065&season=30&tlev=0&tseq=0&league=1">The Beekeepers 2 </a></td><td align=center>12</td><td align=center>2</td><td align=center>10</td><td align=center>0</td><td align=center>0</td><td align=center>4</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=93>Senior EEEE</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=93&season=30&conf=0">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=93&league=1&season=30&conf=0">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2606&season=30&tlev=0&tseq=0&league=1">Unhealthy Scratch </a></td><td align=center>12</td><td align=center>7</td><td align=center>4</td><td align=center>1</td><td align=center>0</td><td align=center>15</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2966&season=30&tlev=0&tseq=0&league=1">Stiflers Mom </a></td><td align=center>12</td><td align=center>6</td><td align=center>4</td><td align=center>1</td><td align=center>1</td><td align=center>14</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=797&season=30&tlev=0&tseq=0&league=1">Crown Royals </a></td><td align=center>12</td><td align=center>6</td><td align=center>6</td><td align=center>0</td><td align=center>0</td><td align=center>12</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=2970&season=30&tlev=0&tseq=0&league=1">Thresher Sharks </a></td><td align=center>12</td><td align=center>5</td><td align=center>5</td><td align=center>1</td><td align=center>1</td><td align=center>12</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=3067&season=30&tlev=0&tseq=0&league=1">Cant Stop Wont Stop </a></td><td align=center>12</td><td align=center>4</td><td align=center>4</td><td align=center>3</td><td align=center>1</td><td align=center>12</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=75&season=30&tlev=0&tseq=0&league=1">Rebels  </a></td><td align=center>12</td><td align=center>4</td><td align=center>4</td><td align=center>2</td><td align=center>2</td><td align=center>12</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=664&season=30&tlev=0&tseq=0&league=1">Absolute Zero </a></td><td align=center>12</td><td align=center>2</td><td align=center>9</td><td align=center>0</td><td align=center>1</td><td align=center>5</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=85&season=30&tlev=0&tseq=0&league=1">A-Team </a></td><td align=center>12</td><td align=center>1</td><td align=center>11</td><td align=center>0</td><td align=center>0</td><td align=center>2</td></tr>

<TR bgcolor="#00515a"><th colspan=7><a name=203>Senior EEEEE</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-league-stats.php?league=1&level=203&season=30&conf=0">Player Stats</a></th></tr>
<TR bgcolor="#00515a"><th colspan=7><a href="display-playoff.php?level=203&league=1&season=30&conf=0">Playoff Tree</a></th></tr>
<tr bgcolor="#00515a"><th>Team</th><th>GP</th><th>W</th><th>L</th><th>T</th><th>OTL</th><th>PTS</th></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=1838&season=30&tlev=0&tseq=0&league=1">Royals </a></td><td align=center>13</td><td align=center>10</td><td align=center>1</td><td align=center>1</td><td align=center>1</td><td align=center>22</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=3068&season=30&tlev=0&tseq=0&league=1">Stiflers Mom 2 </a></td><td align=center>14</td><td align=center>10</td><td align=center>2</td><td align=center>1</td><td align=center>1</td><td align=center>22</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=1792&season=30&tlev=0&tseq=0&league=1">Chieftains 3 </a></td><td align=center>13</td><td align=center>5</td><td align=center>6</td><td align=center>0</td><td align=center>2</td><td align=center>12</td></tr>
<tr bgcolor="#e4e4e4">
<td align=center><a href="display-schedule.php?team=301&season=30&tlev=0&tseq=0&league=1">A Team 2 </a></td><td align=center>13</td><td align=center>4</td><td align=center>8</td><td align=center>0</td><td align=center>1</td><td align=center>9</td></tr>
<tr bgcolor="#b4b4b4">
<td align=center><a href="display-schedule.php?team=2258&season=30&tlev=0&tseq=0&league=1">Night Hawks 3 </a></td><td align=center>13</td><td align=center>3</td><td align=center>9</td><td align=center>0</td><td align=center>1</td><td align=center>7</td></tr>
</table><br>&copy; Time to Score, Inc</center></body>



'''

team_html = '''
<style type="text/css">
//<!--
body {  font-family: Arial, Helvetica, sans-serif; font-size: 10pt}
th   {  font-family: Arial, Helvetica, sans-serif; font-size: 10pt;
        font-weight: bold; background-color: #D3DCE3;}
td   {  font-family: Arial, Helvetica, sans-serif; font-size: 10pt;}
form   {  font-family: Arial, Helvetica, sans-serif; font-size: 10pt}
h1b   {  font-family: Verdana, Arial, Helvetica, sans-serif;
         font-size: 16pt; font-weight: bold}
A:link    {  font-family: Arial, Helvetica, sans-serif;
         font-size: 10pt; text-decoration: none; color: blue}
A:visited {  font-family: Arial, Helvetica, sans-serif;
         font-size: 10pt; text-decoration: none; color: blue}
A:hover   {  font-family: Arial, Helvetica, sans-serif;
         font-size: 10pt; text-decoration: underline; color: red}
A:link.nav {  font-family: Verdana, Arial, Helvetica, sans-serif;
         color: #000000}
A:visited.nav {  font-family: Verdana, Arial, Helvetica, sans-serif;
         color: #000000}
A:hover.nav {  font-family: Verdana, Arial, Helvetica, sans-serif; color: red;}
.nav {  font-family: Verdana, Arial, Helvetica, sans-serif; color: #000000}

//-->
</style>

<body text="#000000" vlink="#1111aa" link="#0000ff" bgcolor="ffffff">
<SCRIPT TYPE="text/javascript">
<!--

  function outlook_confirm(link)
  {

    var confirmation = confirm("For Outlook, please save the file and then use the Import function on the File Menu to load the events, otherwise only the first event will be loaded\n");
    if (confirmation) { document.location = link; }

  }

//-->
</SCRIPT>







<br><br><center><table border=0><TR><th colspan=13>Game Results</th></tr><tr><th>Game</th><th>Date</th><th>Time</th><th>Rink</th><th>League</th><th>Level</th><th>Away</th><th>Goals</th><th>Home</th><th>Goals</th><th>Type</th><th>Scoresheet</th><th>Box Score</th></tr><tr bgcolor="#CCCCcc"><td><a href="oss-scoresheet?game_id=123438&mode=display">123438*</a></td><td>&nbsp;Thu Sep 4&nbsp;</td><td>&nbsp;9:45 PM&nbsp;</td><td>&nbsp;San Jose Center &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;Raptors  &nbsp;</td><td>&nbsp;0&nbsp;</td><td>&nbsp;<b>Mermen  </b>&nbsp;</td><td>&nbsp;<b>8</b>&nbsp;</td><td>&nbsp;Preseason&nbsp;</td><td><a href="generate-scorecard.php?game_id=123438">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#DDDDDD"><td><a href="oss-scoresheet?game_id=123756&mode=display">123756*</a></td><td>&nbsp;Sat Sep 13&nbsp;</td><td>&nbsp;5:15 PM&nbsp;</td><td>&nbsp;San Jose South &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;Mavericks  &nbsp;</td><td>&nbsp;3&nbsp;</td><td>&nbsp;<b>Mermen  </b>&nbsp;</td><td>&nbsp;<b>4</b>&nbsp;</td><td>&nbsp;Preseason&nbsp;</td><td><a href="generate-scorecard.php?game_id=123756">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#CCCCcc"><td><a href="oss-scoresheet?game_id=123813&mode=display">123813*</a></td><td>&nbsp;Fri Sep 19&nbsp;</td><td>&nbsp;11:15 PM&nbsp;</td><td>&nbsp;San Jose Center &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;<b>Mermen  </b>&nbsp;</td><td>&nbsp;<b>8</b>&nbsp;</td><td>&nbsp;Red Dogs  &nbsp;</td><td>&nbsp;0&nbsp;</td><td>&nbsp;Regular 1&nbsp;</td><td><a href="generate-scorecard.php?game_id=123813">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#DDDDDD"><td><a href="oss-scoresheet?game_id=124003&mode=display">124003*</a></td><td>&nbsp;Sat Sep 27&nbsp;</td><td>&nbsp;11:15 PM&nbsp;</td><td>&nbsp;San Jose South &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;<b>Mermen  </b>&nbsp;</td><td>&nbsp;<b>4</b>&nbsp;</td><td>&nbsp;Blackhawks  &nbsp;</td><td>&nbsp;0&nbsp;</td><td>&nbsp;Regular 2&nbsp;</td><td><a href="generate-scorecard.php?game_id=124003">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#CCCCcc"><td><a href="oss-scoresheet?game_id=124225&mode=display">124225*</a></td><td>&nbsp;Sat Oct 11&nbsp;</td><td>&nbsp;6:15 PM&nbsp;</td><td>&nbsp;San Jose East &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;Blackhawks  &nbsp;</td><td>&nbsp;6&nbsp;</td><td>&nbsp;Mermen  &nbsp;</td><td>&nbsp;6&nbsp;</td><td>&nbsp;Regular 3&nbsp;</td><td><a href="generate-scorecard.php?game_id=124225">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#DDDDDD"><td><a href="oss-scoresheet?game_id=124275&mode=display">124275*</a></td><td>&nbsp;Fri Oct 17&nbsp;</td><td>&nbsp;10:15 PM&nbsp;</td><td>&nbsp;San Jose North &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;Charlie Browns  &nbsp;</td><td>&nbsp;3&nbsp;</td><td>&nbsp;<b>Mermen  </b>&nbsp;</td><td>&nbsp;<b>8</b>&nbsp;</td><td>&nbsp;Regular 4&nbsp;</td><td><a href="generate-scorecard.php?game_id=124275">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#CCCCcc"><td><a href="oss-scoresheet?game_id=124796&mode=display">124796*</a></td><td>&nbsp;Sat Oct 25&nbsp;</td><td>&nbsp;10:00 PM&nbsp;</td><td>&nbsp;San Jose Center &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;<b>Mermen  </b>&nbsp;</td><td>&nbsp;<b>6</b>&nbsp;</td><td>&nbsp;Raptors  &nbsp;</td><td>&nbsp;0&nbsp;</td><td>&nbsp;Regular 5&nbsp;</td><td><a href="generate-scorecard.php?game_id=124796">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#DDDDDD"><td><a href="oss-scoresheet?game_id=124842&mode=display">124842*</a></td><td>&nbsp;Thu Oct 30&nbsp;</td><td>&nbsp;11:15 PM&nbsp;</td><td>&nbsp;San Jose South &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;<b>Mermen  </b>&nbsp;</td><td>&nbsp;<b>7</b>&nbsp;</td><td>&nbsp;Red Dogs  &nbsp;</td><td>&nbsp;2&nbsp;</td><td>&nbsp;Regular 6&nbsp;</td><td><a href="generate-scorecard.php?game_id=124842">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#CCCCcc"><td><a href="oss-scoresheet?game_id=125442&mode=display">125442*</a></td><td>&nbsp;Wed Nov 5&nbsp;</td><td>&nbsp;9:45 PM&nbsp;</td><td>&nbsp;San Jose Center &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;<b>Mermen  </b>&nbsp;</td><td>&nbsp;<b>4</b>&nbsp;</td><td>&nbsp;Mavericks  &nbsp;</td><td>&nbsp;2&nbsp;</td><td>&nbsp;Regular 7&nbsp;</td><td><a href="generate-scorecard.php?game_id=125442">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#DDDDDD"><td><a href="oss-scoresheet?game_id=125573&mode=display">125573*</a></td><td>&nbsp;Fri Nov 21&nbsp;</td><td>&nbsp;11:00 PM&nbsp;</td><td>&nbsp;San Jose East &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;<b>Mavericks  </b>&nbsp;</td><td>&nbsp;<b>7</b>&nbsp;</td><td>&nbsp;Mermen  &nbsp;</td><td>&nbsp;3&nbsp;</td><td>&nbsp;Regular 8&nbsp;</td><td><a href="generate-scorecard.php?game_id=125573">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#CCCCcc"><td><a href="oss-scoresheet?game_id=125762&mode=display">125762*</a></td><td>&nbsp;Sat Dec 6&nbsp;</td><td>&nbsp;11:15 PM&nbsp;</td><td>&nbsp;San Jose North &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;Charlie Browns  &nbsp;</td><td>&nbsp;3&nbsp;</td><td>&nbsp;<b>Mermen  </b>&nbsp;</td><td>&nbsp;<b>6</b>&nbsp;</td><td>&nbsp;Regular 9&nbsp;</td><td><a href="generate-scorecard.php?game_id=125762">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#DDDDDD"><td><a href="oss-scoresheet?game_id=127420&mode=display">127420*</a></td><td>&nbsp;Fri Dec 12&nbsp;</td><td>&nbsp;8:00 PM&nbsp;</td><td>&nbsp;SAP Center   &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;Raptors  &nbsp;</td><td>&nbsp;1&nbsp;</td><td>&nbsp;<b>Mermen  </b>&nbsp;</td><td>&nbsp;<b>8</b>&nbsp;</td><td>&nbsp;Regular 10&nbsp;</td><td><a href="generate-scorecard.php?game_id=127420">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#CCCCcc"><td><a href="oss-scoresheet?game_id=127446&mode=display">127446*</a></td><td>&nbsp;Fri Dec 19&nbsp;</td><td>&nbsp;10:45 PM&nbsp;</td><td>&nbsp;San Jose East &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;<b>Mermen  </b>&nbsp;</td><td>&nbsp;<b>10</b>&nbsp;</td><td>&nbsp;Red Dogs  &nbsp;</td><td>&nbsp;8&nbsp;</td><td>&nbsp;Regular 11&nbsp;</td><td><a href="generate-scorecard.php?game_id=127446">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#DDDDDD"><td><a href="oss-scoresheet?game_id=127487&mode=display">127487*</a></td><td>&nbsp;Fri Dec 26&nbsp;</td><td>&nbsp;8:15 PM&nbsp;</td><td>&nbsp;San Jose East &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;<b>Mermen  </b>&nbsp;</td><td>&nbsp;<b>5</b>&nbsp;</td><td>&nbsp;Blackhawks  &nbsp;</td><td>&nbsp;1&nbsp;</td><td>&nbsp;Regular 12&nbsp;</td><td><a href="generate-scorecard.php?game_id=127487">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#CCCCcc"><td><a href="oss-scoresheet?game_id=128028&mode=display">128028*</a></td><td>&nbsp;Wed Jan 7&nbsp;</td><td>&nbsp;11:15 PM&nbsp;</td><td>&nbsp;San Jose Center &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;Blackhawks  &nbsp;</td><td>&nbsp;2&nbsp;</td><td>&nbsp;<b>Mermen  </b>&nbsp;</td><td>&nbsp;<b>10</b>&nbsp;</td><td>&nbsp;Regular 13&nbsp;</td><td><a href="generate-scorecard.php?game_id=128028">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#DDDDDD"><td><a href="oss-scoresheet?game_id=128101&mode=display">128101*</a></td><td>&nbsp;Thu Jan 15&nbsp;</td><td>&nbsp;10:30 PM&nbsp;</td><td>&nbsp;San Jose East &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;Mermen  &nbsp;</td><td>&nbsp;2&nbsp;</td><td>&nbsp;<b>Charlie Browns  </b>&nbsp;</td><td>&nbsp;<b>6</b>&nbsp;</td><td>&nbsp;Regular 14&nbsp;</td><td><a href="generate-scorecard.php?game_id=128101">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#CCCCcc"><td><a href="oss-scoresheet?game_id=128185&mode=display">128185*</a></td><td>&nbsp;Fri Jan 23&nbsp;</td><td>&nbsp;11:15 PM&nbsp;</td><td>&nbsp;San Jose South &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;Charlie Browns  &nbsp;</td><td>&nbsp;3&nbsp;</td><td>&nbsp;<b>Mermen  </b>&nbsp;</td><td>&nbsp;<b>6</b>&nbsp;</td><td>&nbsp;Regular 15&nbsp;</td><td><a href="generate-scorecard.php?game_id=128185">Scoresheet</a></td><td>&nbsp;</td></tr><tr bgcolor="#DDDDDD"><td>129699</td><td>&nbsp;Sat Feb 7&nbsp;</td><td>&nbsp;9:45 PM&nbsp;</td><td>&nbsp;San Jose South &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;Raptors  &nbsp;</td><td>&nbsp;&nbsp;</td><td>&nbsp;Mermen  &nbsp;</td><td>&nbsp;&nbsp;</td><td>&nbsp;Regular 16&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr bgcolor="#CCCCcc"><td>129748</td><td>&nbsp;Thu Feb 12&nbsp;</td><td>&nbsp;10:30 PM&nbsp;</td><td>&nbsp;San Jose East &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;Mermen  &nbsp;</td><td>&nbsp;&nbsp;</td><td>&nbsp;Red Dogs  &nbsp;</td><td>&nbsp;&nbsp;</td><td>&nbsp;Regular 17&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr bgcolor="#DDDDDD"><td>129760</td><td>&nbsp;Fri Feb 13&nbsp;</td><td>&nbsp;10:00 PM&nbsp;</td><td>&nbsp;San Jose North &nbsp;</td><td>&nbsp;SIAHL@SJ&nbsp;</td><td>&nbsp;Senior CCC&nbsp;</td><td>&nbsp;Mermen  &nbsp;</td><td>&nbsp;&nbsp;</td><td>&nbsp;Mavericks  &nbsp;</td><td>&nbsp;&nbsp;</td><td>&nbsp;Regular 18&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table></center><center>Download Schedule:&nbsp;<a href="team-cal.php?team=2051&tlev=0&tseq=0&season=30&format=iCal">iCal</a>&nbsp;<a href="javascript:outlook_confirm('team-cal.php?team=2051&tlev=0&tseq=0&season=30&format=outlook')">Outlook</a>&nbsp;<a href="export-schedule-download.php?league=1&level=0&team=2051&season=30">Excel</a>&nbsp;<a href="webcal://stats.siahl.org/team-cal.php?team=2051&tlev=0&tseq=0&season=30&format=iCal">WebCal</a>&nbsp;</center><br><br><center><table border=0><tr><th colspan=15>Player Stats</th></tr><tr><th>Name</th><th>#</th><th>GP</th><th>Goals</th><th>Ass.</th><th>PPG</th><th>PPA</th><th>SHG</th><th>SHA</th><th>GWG</th><th>GWA</th><th>PSG</th><th>ENG</th><th>SOG</th><th>Pts</th></tr><tr bgcolor="#CCCCCC"><td align=center>Michael Yeater</td><TD align=center>8</td><TD align=center>14</td><TD align=center>16</td><TD align=center>15</td><TD align=center>2</td><TD align=center>2</td><TD align=center>4</td><TD align=center>0</td><TD align=center>0</td><TD align=center>1</td><TD align=center>0</td><TD align=center>1</td><TD align=center>0</td><TD align=center>31</td></tr><tr bgcolor="#DDDDDD"><td align=center>Billy Barnes</td><TD align=center>13</td><TD align=center>10</td><TD align=center>18</td><TD align=center>10</td><TD align=center>2</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>3</td><TD align=center>2</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>28</td></tr><tr bgcolor="#CCCCCC"><td align=center>Cameron Yeater</td><TD align=center>88</td><TD align=center>12</td><TD align=center>10</td><TD align=center>14</td><TD align=center>1</td><TD align=center>2</td><TD align=center>0</td><TD align=center>1</td><TD align=center>2</td><TD align=center>2</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>24</td></tr><tr bgcolor="#DDDDDD"><td align=center>Joe Burger</td><TD align=center>11</td><TD align=center>14</td><TD align=center>12</td><TD align=center>7</td><TD align=center>4</td><TD align=center>1</td><TD align=center>0</td><TD align=center>0</td><TD align=center>3</td><TD align=center>2</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>19</td></tr><tr bgcolor="#CCCCCC"><td align=center>Edward Tracy</td><TD align=center>17</td><TD align=center>12</td><TD align=center>1</td><TD align=center>17</td><TD align=center>0</td><TD align=center>1</td><TD align=center>0</td><TD align=center>1</td><TD align=center>0</td><TD align=center>3</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>18</td></tr><tr bgcolor="#DDDDDD"><td align=center>Don Wilcoxon</td><TD align=center>4</td><TD align=center>13</td><TD align=center>7</td><TD align=center>9</td><TD align=center>0</td><TD align=center>2</td><TD align=center>0</td><TD align=center>0</td><TD align=center>1</td><TD align=center>1</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>16</td></tr><tr bgcolor="#CCCCCC"><td align=center>Nick Burger</td><TD align=center>12</td><TD align=center>13</td><TD align=center>6</td><TD align=center>9</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>1</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>15</td></tr><tr bgcolor="#DDDDDD"><td align=center>Thomas Kelsch</td><TD align=center>5</td><TD align=center>6</td><TD align=center>7</td><TD align=center>6</td><TD align=center>0</td><TD align=center>2</td><TD align=center>0</td><TD align=center>0</td><TD align=center>1</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>13</td></tr><tr bgcolor="#CCCCCC"><td align=center>James Idemoto</td><TD align=center>23</td><TD align=center>12</td><TD align=center>4</td><TD align=center>7</td><TD align=center>0</td><TD align=center>2</td><TD align=center>0</td><TD align=center>0</td><TD align=center>1</td><TD align=center>2</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>11</td></tr><tr bgcolor="#DDDDDD"><td align=center>Richard Eramaa</td><TD align=center>24</td><TD align=center>12</td><TD align=center>3</td><TD align=center>6</td><TD align=center>0</td><TD align=center>1</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>2</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>9</td></tr><tr bgcolor="#CCCCCC"><td align=center>MICHAEL WALDO</td><TD align=center>47</td><TD align=center>12</td><TD align=center>4</td><TD align=center>5</td><TD align=center>1</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>1</td><TD align=center>0</td><TD align=center>1</td><TD align=center>0</td><TD align=center>9</td></tr><tr bgcolor="#DDDDDD"><td align=center>Ben Loveless</td><TD align=center>98</td><TD align=center>13</td><TD align=center>1</td><TD align=center>6</td><TD align=center>0</td><TD align=center>2</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>1</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>7</td></tr><tr bgcolor="#CCCCCC"><td align=center>Brent Taira</td><TD align=center>19</td><TD align=center>13</td><TD align=center>2</td><TD align=center>5</td><TD align=center>1</td><TD align=center>2</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>7</td></tr><tr bgcolor="#DDDDDD"><td align=center>Douglas Buck</td><TD align=center>00</td><TD align=center>12</td><TD align=center>1</td><TD align=center>4</td><TD align=center>0</td><TD align=center>1</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td><TD align=center>5</td></tr></table><br><table border=0><tr><th colspan=10>Goalie Stats</th></tr><tr><th>Name</th><th>#</th><th>GP</th><th>Shots</th><th>GA</th><th>GAA</th><th>Save %</th><th>Goals</th><th>Ass.</th><th>Pts</th></tr><tr bgcolor="#CCCCCC"><td align=center>William Q Barnes-Carr</td><TD align=center>*</td><TD align=center>1</td><TD align=center>33</td><TD align=center>2</td><TD align=center>2.00</td><TD align=center>0.939</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td></tr><tr bgcolor="#DDDDDD"><td align=center>craig  R cole</td><TD align=center>*</td><TD align=center>2</td><TD align=center>37</td><TD align=center>7</td><TD align=center>3.50</td><TD align=center>0.811</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td></tr><tr bgcolor="#CCCCCC"><td align=center>Jason   Molenda</td><TD align=center>*</td><TD align=center>2</td><TD align=center>23</td><TD align=center>4</td><TD align=center>2.00</td><TD align=center>0.826</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td></tr><tr bgcolor="#DDDDDD"><td align=center>Matthew R Salacain</td><TD align=center>31</td><TD align=center>10</td><TD align=center>233</td><TD align=center>24</td><TD align=center>2.40</td><TD align=center>0.897</td><TD align=center>0</td><TD align=center>0</td><TD align=center>0</td></tr></table></center><br><center>&copy; Time to Score, Inc</center></body>
'''

team_rollover_html = '''<html>
<style type="text/css">
	//<!--
	body {  font-family: Arial, Helvetica, sans-serif; font-size: 10pt}
	th   {  font-family: Arial, Helvetica, sans-serif; font-size: 10pt;
		font-weight: bold; background-color: #D3DCE3;}
		td   {  font-family: Arial, Helvetica, sans-serif; font-size: 10pt;}
		form   {  font-family: Arial, Helvetica, sans-serif; font-size: 10pt}
		h1b   {  font-family: Verdana, Arial, Helvetica, sans-serif;
			font-size: 16pt; font-weight: bold}
			A:link    {  font-family: Arial, Helvetica, sans-serif;
				font-size: 10pt; text-decoration: none; color: blue}
				A:visited {  font-family: Arial, Helvetica, sans-serif;
					font-size: 10pt; text-decoration: none; color: blue}
					A:hover   {  font-family: Arial, Helvetica, sans-serif;
						font-size: 10pt; text-decoration: underline; color: red}
						A:link.nav {  font-family: Verdana, Arial, Helvetica, sans-serif;
							color: #000000}
							A:visited.nav {  font-family: Verdana, Arial, Helvetica, sans-serif;
								color: #000000}
								A:hover.nav {  font-family: Verdana, Arial, Helvetica, sans-serif; color: red;}
								.nav {  font-family: Verdana, Arial, Helvetica, sans-serif; color: #000000}

								//-->
							</style>

							<body text="#000000" vlink="#1111aa" link="#0000ff" bgcolor="ffffff">
								<SCRIPT TYPE="text/javascript">
									<!--

									function outlook_confirm(link)
									{

										var confirmation = confirm("For Outlook, please save the file and then use the Import function on the File Menu to load the events, otherwise only the first event will be loaded\n");
										if (confirmation) { document.location = link; }

									}

  //-->
</SCRIPT>







<br>
<br>
<center>
	<table border=0>
		<TR>
			<th colspan=13>Game Results</th>
		</tr>
		<tr>
			<th>Game</th>
			<th>Date</th>
			<th>Time</th>
			<th>Rink</th>
			<th>League</th>
			<th>Level</th>
			<th>Away</th>
			<th>Goals</th>
			<th>Home</th>
			<th>Goals</th>
			<th>Type</th>
			<th>Scoresheet</th>
			<th>Box Score</th>
		</tr>
		<tr bgcolor="#DDDDDD">
			<td>127554</td>
			<td>&nbsp;Sat Dec 27&nbsp;</td>
			<td>&nbsp;5:15 PM&nbsp;</td>
			<td>&nbsp;San Jose East &nbsp;</td>
			<td>&nbsp;SIAHL@SJ&nbsp;</td>
			<td>&nbsp;Senior DDDD&nbsp;</td>
			<td>&nbsp;<b>Time Lords  </b>&nbsp;</td>
			<td>&nbsp;<b>6</b>&nbsp;</td>
			<td>&nbsp;K-Wings  &nbsp;</td>
			<td>&nbsp;1&nbsp;</td>
			<td>&nbsp;Regular 10&nbsp;</td>
			<td>
				<a href="generate-scorecard.php?game_id=127554">Scoresheet</a>
			</td>
			<td>&nbsp;</td>
		</tr>
		<tr bgcolor="#CCCCcc">
			<td>127520</td>
			<td>&nbsp;Sun Jan 4&nbsp;</td>
			<td>&nbsp;11:15 PM&nbsp;</td>
			<td>&nbsp;San Jose Center &nbsp;</td>
			<td>&nbsp;SIAHL@SJ&nbsp;</td>
			<td>&nbsp;Senior DDDD&nbsp;</td>
			<td>&nbsp;<b>Time Lords  </b>&nbsp;</td>
			<td>&nbsp;<b>6</b>&nbsp;</td>
			<td>&nbsp;Natural Disasters  &nbsp;</td>
			<td>&nbsp;0&nbsp;</td>
			<td>&nbsp;Regular 11&nbsp;</td>
			<td>
				<a href="generate-scorecard.php?game_id=127520">Scoresheet</a>
			</td>
			<td>&nbsp;</td>
		</tr>
	</table>
</center>
<center>Download Schedule:&nbsp;<a href="team-cal.php?team=2046&tlev=0&tseq=0&season=30&format=iCal">iCal</a>&nbsp;<a href="javascript:outlook_confirm('team-cal.php?team=2046&tlev=0&tseq=0&season=30&format=outlook')">Outlook</a>&nbsp;<a href="export-schedule-download.php?league=1&level=0&team=2046&season=30">Excel</a>&nbsp;<a href="webcal://stats.siahl.org/team-cal.php?team=2046&tlev=0&tseq=0&season=30&format=iCal">WebCal</a>&nbsp;</center>
<br>
<br>

    <br>
    <center>&copy; Time to Score, Inc</center>
</body>











</html>'''