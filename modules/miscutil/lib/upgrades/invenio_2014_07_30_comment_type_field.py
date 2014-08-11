# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2012, 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.


from invenio.dbquery import run_sql
from invenio.webmessage_mailutils import email_quoted_txt2html

depends_on = ['invenio_2013_10_18_new_index_filetype']

def info():
    return "New index filename."


def do_upgrade():
    pass


def do_upgrade_atlantis():
    batch_size = 1000

    run_sql("""ALTER TABLE cmtRECORDCOMMENT
               ADD body_format VARCHAR(30) DEFAULT 'text'
               AFTER body;""")
    count = run_sql("""SELECT COUNT(*)
                       FROM cmtRECORDCOMMENT""")[0][0]

    c_id,c_body,c_body_format = 0,1,2
    select_query = """ SELECT id,body,body_format
                FROM cmtRECORDCOMMENT
                limit %s,%s"""

    update_query = """ UPDATE cmtRECORDCOMMENT
                    SET body_format = "html", body = "%s"
                    WHERE id = %s"""

    for i in xrange(0,int(count/batch_size)+1):
        comments = run_sql(select_query,(i*batch_size,(i+1)*batch_size))
        for comment in comments:
            if body_format == "text":
                comment[c_body] = email_quoted_txt2html(comment[c_body])
                run_sql(update_query,(comment[c_body],comment[c_id]))


def estimate():
    return 1

def pre_upgrade():
    pass

def post_upgrade():
    pass
