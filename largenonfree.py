#!/usr/bin/env python2.5

# Copyright 2009 bjweeks, MZMcBride

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

import datetime
import MySQLdb
import wikitools
import settings

report_title = settings.rootpage + 'Large non-free files'

report_template = u'''
Files in [[:Category:All non-free media]] that are larger than 999999 bytes \
and are not in [[:Category:Non-free Wikipedia file size reduction request]]; \
data as of <onlyinclude>%s</onlyinclude>.

{| class="wikitable sortable plainlinks" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! No.
! File
! Size
|-
%s
|}
'''

wiki = wikitools.Wiki(settings.apiurl)
wiki.login(settings.username, settings.password)

conn = MySQLdb.connect(host=settings.host, db=settings.dbname, read_default_file='~/.my.cnf')
cursor = conn.cursor()
cursor.execute('''
/* largenonfree.py SLOW_OK */
SELECT
  ns_name,
  page_title,
  img_size
FROM page
JOIN toolserver.namespace
ON dbname = %s
AND page_namespace = ns_id
JOIN image
ON img_name = page_title
JOIN categorylinks
ON cl_from = page_id
WHERE page_namespace = 6
AND cl_to = 'All_non-free_media'
AND img_size > 999999
AND NOT EXISTS (SELECT
                  1
                FROM categorylinks
                WHERE page_id = cl_from
                AND cl_to = 'Non-free_Wikipedia_file_size_reduction_request');
''' , settings.dbname)

i = 1
output = []
for row in cursor.fetchall():
    ns_name = u'%s' % unicode(row[0], 'utf-8')
    page_title = u'%s' % unicode(row[1], 'utf-8')
    full_page_title = u'[[:%s:%s|%s]]' % (ns_name, page_title, page_title)
    img_size = row[2]
    table_row = u'''| %d
| %s
| %s
|-''' % (i, full_page_title, img_size)
    output.append(table_row)
    i += 1

cursor.execute('SELECT UNIX_TIMESTAMP() - UNIX_TIMESTAMP(rc_timestamp) FROM recentchanges ORDER BY rc_timestamp DESC LIMIT 1;')
rep_lag = cursor.fetchone()[0]
current_of = (datetime.datetime.utcnow() - datetime.timedelta(seconds=rep_lag)).strftime('%H:%M, %d %B %Y (UTC)')

report = wikitools.Page(wiki, report_title)
report_text = report_template % (current_of, '\n'.join(output))
report_text = report_text.encode('utf-8')
report.edit(report_text, summary=settings.editsumm, bot=1)

cursor.close()
conn.close()