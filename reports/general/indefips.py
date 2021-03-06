# Copyright 2008, 2013 bjweeks, MZMcBride, Tim Landscheidt

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Report class for indefinitely blocked IPs
"""

import datetime
import re

import reports

class report(reports.report):
    def get_title(self):
        return 'Indefinitely blocked IPs'

    def get_preamble(self, conn):
        cursor = conn.cursor()
        cursor.execute('SELECT UNIX_TIMESTAMP() - UNIX_TIMESTAMP(rc_timestamp) FROM recentchanges ORDER BY rc_timestamp DESC LIMIT 1;')
        rep_lag = cursor.fetchone()[0]
        current_of = (datetime.datetime.utcnow() - datetime.timedelta(seconds=rep_lag)).strftime('%H:%M, %d %B %Y (UTC)')

        return 'Indefinitely blocked IPs whose block reasons do not contain "(proxies|proxy|checkuser)"; data as of <onlyinclude>%s</onlyinclude>.' % current_of

    def get_table_columns(self):
        return ['IP', 'Admin', 'Timestamp', 'Reason']

    def get_table_rows(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
/* indefips.py SLOW_OK */
SELECT
  CONVERT(ipb_address USING utf8),
  CONVERT(ipb_by_text USING utf8),
  ipb_timestamp,
  CONVERT(ipb_reason USING utf8)
FROM ipblocks
WHERE ipb_expiry = "infinity"
AND ipb_user = 0;
''')

        for ipb_address, ipb_by_text, ipb_timestamp, ipb_reason in cursor:
            if not re.search(r'(proxies|proxy|checkuser)', ipb_reason, re.I|re.U):
                if not re.search(r'(^[^0-9])', ipb_address, re.I|re.U):
                    ipb_address = u'[[User talk:%s|]]' % ipb_address
                    if ipb_reason:
                        ipb_reason = u'<nowiki>%s</nowiki>' % ipb_reason
                    else:
                        ipb_reason = ''
                    yield [ipb_address, ipb_by_text, ipb_timestamp, ipb_reason]

        cursor.close()
