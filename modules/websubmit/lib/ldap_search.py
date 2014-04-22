from invenio.bibcirculation_cern_ldap import _cern_ldap_login,_ldap_connection_pool,ldap,CFG_CERN_LDAP_BASE
from thread import get_ident

CFG_SOURCE_NAME = "ldap_search"

def query_author_source(nickname):
    """Query the CERN LDAP server for information about a user.
    Return a dictionary of information"""

    try:
        connection = _ldap_connection_pool[get_ident()]
    except KeyError:
        connection = _ldap_connection_pool[get_ident()] = _cern_ldap_login()

    if nickname:
        query = '(displayName=*%s*)' % (nickname)
    elif email:
        query = '(mail=%s)' % ldap.filter.escape_filter_chars(email)
    elif ccid:
        query = '(employeeID=%s)' % ldap.filter.escape_filter_chars(str(ccid))
    else:
        return {}

    query_filter = "(& %s (| (employeetype=primary) (employeetype=external) (employeetype=ExCern) ) )" % query
    try:
        results = connection.search_st(CFG_CERN_LDAP_BASE, ldap.SCOPE_SUBTREE,
                                query_filter, timeout=5)
    except ldap.LDAPError:
        ## Mmh.. connection error? Let's reconnect at least once just in case
        sleep(1)
        connection = _ldap_connection_pool[get_ident()] = _cern_ldap_login()
        results = connection.search_st(CFG_CERN_LDAP_BASE, ldap.SCOPE_SUBTREE,
                                query_filter, timeout=5)

    formated_results = []

    for result in results:
        formated_results.append({'name' : result[1]['displayName'][0], 'email' : result[1]['mail'][0], 'affiliation': result[1].get('cernInstituteName',['CERN'])[0]})

    return formated_results
    ## if len(results) > 1:
    ##     ## Maybe one ExCern and primary at the same time. In this case let's give precedence to ExCern
    ##     types = {}
    ##     for result in results:
    ##         types[result[1]['employeeType'][0]] = result[1]
    ##     if 'ExCern' in types and 'Primary' in types:
    ##         return types['ExCern']
    ##     if 'Primary' in types:
    ##         return types['Primary']
    ##     ## Ok otherwise we just pick up something :-)
    ## if results:
    ##     return results[0][1]
    ## else:
    ##     return {}
