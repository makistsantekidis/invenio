## This file is part of Invenio.
## Copyright (C) 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014 CERN.
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

from invenio.bibcirculation_cern_ldap import _cern_ldap_login,_ldap_connection_pool,CFG_CERN_LDAP_BASE
from thread import get_ident
from time import sleep

CFG_SOURCE_NAME = "ldap"



def query_author_source(nickname):
    """Query the CERN LDAP server for information about a user.
    Return a dictionary of information"""

    try:
        connection = _ldap_connection_pool[get_ident()]
    except KeyError:
        connection = _ldap_connection_pool[get_ident()] = _cern_ldap_login()

    if nickname:
        query = '(displayName=*%s*)' % (nickname)
    else:
        return {}

    query_filter = "(& %s (| (employeetype=primary) (employeetype=external) (employeetype=ExCern) ) )" % query
    try:
        results = connection.search_st(CFG_CERN_LDAP_BASE, ldap.SCOPE_SUBTREE,
                                query_filter, timeout=5)
    except ldap.LDAPError:
        return {}

    formated_results = []

    for result in results:
        formated_results.append({'name' : result[1]['displayName'][0], 'email' : result[1]['mail'][0], 'affiliation': result[1].get('cernInstituteName',['CERN'])[0]})

    return formated_results
