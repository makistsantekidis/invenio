from invenio.bibcirculation_cern_ldap import _cern_ldap_login,_ldap_connection_pool,ldap,CFG_CERN_LDAP_BASE
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
