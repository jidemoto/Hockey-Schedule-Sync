import unittest
import NcwhlParser


def dummy_open(url):
    return DummyUrl()


class ScheduleParsesTestCase(unittest.TestCase):
    def runTest(self):
        NcwhlParser.urllib.urlopen = dummy_open
        games = NcwhlParser.rip_schedule("ScheduleURL", ['R6'])
        self.assertEqual(len(games), 1, "Wrong number of games parsed")
        self.assertEqual(games[0].rink, 'Ice Oasis')
        self.assertEqual(games[0].home, 'R3')
        self.assertEqual(games[0].away, 'R6')
        self.assertEqual(games[0].address, '3140 Bay Road, Redwood City, CA 94063')

        games = NcwhlParser.rip_schedule("ScheduleURL", ['R1'])
        self.assertEqual(len(games), 1, "Wrong number of games parsed")
        self.assertEqual(games[0].rink, 'Vallco')
        self.assertEqual(games[0].home, 'R1')
        self.assertEqual(games[0].away, 'R4')
        self.assertEqual(games[0].address, '10123 N Wolfe Rd, Cupertino, CA 95014')

        games = NcwhlParser.rip_schedule("ScheduleURL", ['R2'])
        self.assertEqual(len(games), 1, "Wrong number of games parsed")
        self.assertEqual(games[0].rink, 'Fremont')
        self.assertEqual(games[0].home, 'R2')
        self.assertEqual(games[0].away, 'R5')
        self.assertEqual(games[0].address, '44388 Old Warm Springs Boulevard, Fremont, CA 94538')

        games = NcwhlParser.rip_schedule("ScheduleURL", ['M1'])
        self.assertEqual(len(games), 1, "Wrong number of games parsed")
        self.assertEqual(games[0].rink, 'Oakland')
        self.assertEqual(games[0].home, 'M1')
        self.assertEqual(games[0].away, 'M2')
        self.assertEqual(games[0].address, '519 18th St, Oakland, CA 94612')


class DummyUrl:
    def read(self):
        return """
<html>
<body link=blue vlink=purple class=xl67>

<table border=0 cellpadding=0 cellspacing=0 width=1183 style='border-collapse:
 collapse;table-layout:fixed;width:1183pt'>
 <col class=xl67 width=65 style='mso-width-source:userset;mso-width-alt:2773;
 width:65pt'>
 <col class=xl65535 width=66 style='mso-width-source:userset;mso-width-alt:
 2816;width:66pt'>
 <col class=xl65535 width=62 style='mso-width-source:userset;mso-width-alt:
 2645;width:62pt'>
 <col class=xl65535 width=69 style='mso-width-source:userset;mso-width-alt:
 2944;width:69pt'>
 <col class=xl65535 width=81 style='mso-width-source:userset;mso-width-alt:
 3456;width:81pt'>
 <col class=xl65535 width=83 style='mso-width-source:userset;mso-width-alt:
 3541;width:83pt'>
 <col class=xl67 width=262 style='mso-width-source:userset;mso-width-alt:11178;
 width:262pt'>
 <col class=xl67 width=58 style='mso-width-source:userset;mso-width-alt:2474;
 width:58pt'>
 <col class=xl67 width=65 style='mso-width-source:userset;mso-width-alt:2773;
 width:65pt'>
 <col class=xl67 width=372 style='mso-width-source:userset;mso-width-alt:15872;
 width:372pt'>
 <tr class=xl66 height=19 style='height:19.0pt'>
  <td height=19 class=xl66 width=65 style='height:19.0pt;width:65pt'>Week</td>
  <td class=xl66 width=66 style='width:66pt'>Slot</td>
  <td class=xl66 width=62 style='width:62pt'>Day</td>
  <td class=xl66 width=69 style='width:69pt'>Date</td>
  <td class=xl66 width=81 style='width:81pt'>Time</td>
  <td class=xl66 width=83 style='width:83pt'>Rink</td>
  <td class=xl66 width=262 style='width:262pt'>Session</td>
  <td class=xl66 width=58 style='width:58pt'>Home</td>
  <td class=xl66 width=65 style='width:65pt'>Away</td>
  <td class=xl66 width=372 style='width:372pt'>Notes</td>
 </tr>
 <tr height=19 style='mso-height-source:userset;height:19.0pt'>
  <td colspan=7 height=19 class=xl114 style='border-right:1.0pt solid black;
  height:19.0pt'>START WINTER 2014-15 EVALS</td>
  <td class=xl67></td>
  <td class=xl67></td>
  <td class=xl67></td>
 </tr>
 <tr height=19 style='mso-height-source:userset;height:19.0pt'>
  <td height=19 class=xl68 style='height:19.0pt;border-top:none'>Week 1</td>
  <td class=xl69 style='border-top:none;border-left:none'>1</td>
  <td class=xl70 style='border-top:none;border-left:none'>Tue</td>
  <td class=xl70 style='border-top:none;border-left:none'>2-Sep-14</td>
  <td class=xl71 style='border-top:none;border-left:none'>8:15 PM</td>
  <td class=xl72 style='border-top:none;border-left:none'>Vallco</td>
  <td class=xl73 style='border-top:none;border-left:none;font-size:14.0pt;
  color:black;font-weight:400;text-decoration:none;text-underline-style:none;
  text-line-through:none;font-family:Calibri;border-top:1.0pt solid windowtext;
  border-right:1.0pt solid windowtext;border-bottom:.5pt hairline windowtext;
  border-left:.5pt hairline windowtext;background:#FFFC92;mso-pattern:black none'>Leaguewide
  Scrimmage</td>
  <td class=xl67></td>
  <td class=xl67></td>
  <td class=xl67></td>
 </tr>
  <tr height=18 style='mso-height-source:userset;height:18.0pt'>
  <td height=18 class=xl74 style='height:18.0pt;border-top:none'>&nbsp;</td>
  <td class=xl75 style='border-top:none;border-left:none'>18</td>
  <td class=xl76 style='border-top:none;border-left:none'>Sat</td>
  <td class=xl76 style='border-top:none;border-left:none'>20-Sep-14</td>
  <td class=xl77 style='border-top:none;border-left:none'>7:30 PM</td>
  <td class=xl78 style='border-top:none;border-left:none'>Ice Oasis</td>
  <td class=xl81 style='border-top:none;border-left:none;font-size:14.0pt;
  color:black;font-weight:400;text-decoration:none;text-underline-style:none;
  text-line-through:none;font-family:Calibri;border-top:.5pt hairline windowtext;
  border-right:1.0pt solid windowtext;border-bottom:.5pt hairline windowtext;
  border-left:.5pt hairline windowtext;background:#FFC7CE;mso-pattern:black none'>Red</td>
  <td class=xl67>R3</td>
  <td class=xl67>R6</td>
  <td class=xl67></td>
 </tr>
  </tr>
  <tr height=18 style='mso-height-source:userset;height:18.0pt'>
  <td height=18 class=xl74 style='height:18.0pt;border-top:none'>&nbsp;</td>
  <td class=xl75 style='border-top:none;border-left:none'>18</td>
  <td class=xl76 style='border-top:none;border-left:none'>Sat</td>
  <td class=xl76 style='border-top:none;border-left:none'>20-Sep-14</td>
  <td class=xl77 style='border-top:none;border-left:none'>7:30 PM</td>
  <td class=xl78 style='border-top:none;border-left:none'>Fremont</td>
  <td class=xl81 style='border-top:none;border-left:none;font-size:14.0pt;
  color:black;font-weight:400;text-decoration:none;text-underline-style:none;
  text-line-through:none;font-family:Calibri;border-top:.5pt hairline windowtext;
  border-right:1.0pt solid windowtext;border-bottom:.5pt hairline windowtext;
  border-left:.5pt hairline windowtext;background:#FFC7CE;mso-pattern:black none'>Red</td>
  <td class=xl67>R2</td>
  <td class=xl67>R5</td>
  <td class=xl67></td>
 </tr>
  </tr>
  <tr height=18 style='mso-height-source:userset;height:18.0pt'>
  <td height=18 class=xl74 style='height:18.0pt;border-top:none'>&nbsp;</td>
  <td class=xl75 style='border-top:none;border-left:none'>18</td>
  <td class=xl76 style='border-top:none;border-left:none'>Sat</td>
  <td class=xl76 style='border-top:none;border-left:none'>20-Sep-14</td>
  <td class=xl77 style='border-top:none;border-left:none'>7:30 PM</td>
  <td class=xl78 style='border-top:none;border-left:none'>Vallco</td>
  <td class=xl81 style='border-top:none;border-left:none;font-size:14.0pt;
  color:black;font-weight:400;text-decoration:none;text-underline-style:none;
  text-line-through:none;font-family:Calibri;border-top:.5pt hairline windowtext;
  border-right:1.0pt solid windowtext;border-bottom:.5pt hairline windowtext;
  border-left:.5pt hairline windowtext;background:#FFC7CE;mso-pattern:black none'>Red</td>
  <td class=xl67>R1</td>
  <td class=xl67>R4</td>
  <td class=xl67></td>
 </tr>
 <tr height=18 style='mso-height-source:userset;height:18.0pt'>
  <td height=18 class=xl74 style='height:18.0pt;border-top:none'>&nbsp;</td>
  <td class=xl75 style='border-top:none;border-left:none'>19</td>
  <td class=xl76 style='border-top:none;border-left:none'>Sat</td>
  <td class=xl76 style='border-top:none;border-left:none'>20-Sep-14</td>
  <td class=xl77 style='border-top:none;border-left:none'>6:45 PM</td>
  <td class=xl78 style='border-top:none;border-left:none'>Oakland</td>
  <td class=xl81 style='border-top:none;border-left:none;font-size:14.0pt;
  color:black;font-weight:400;text-decoration:none;text-underline-style:none;
  text-line-through:none;font-family:Calibri;border-top:.5pt hairline windowtext;
  border-right:1.0pt solid windowtext;border-bottom:.5pt hairline windowtext;
  border-left:.5pt hairline windowtext;background:#DA9694;mso-pattern:black none'>Maroon</td>
  <td class=xl67>M1</td>
  <td class=xl67>M2</td>
  <td class=xl67></td>
 </tr>
</body>

</html>
"""