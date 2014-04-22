#!/usr/bin/python

from urlparse import urlunsplit
from urllib import urlencode
from urllib2 import urlopen

import sys
CFG_JSON_AVAILABLE = True
if sys.hexversion < 0x2060000:
    try:
        import simplejson as json
    except:
        CFG_JSON_AVAILABLE = False
else:
    import json

# Custom field keys when calling the API
CFG_ATLAS_GLANCE_AUTHORS_LASTNAME_FIELD_KEY  = "lastname"
CFG_ATLAS_GLANCE_AUTHORS_FIRSTNAME_FIELD_KEY = "firstname"
CFG_ATLAS_GLANCE_AUTHORS_INITIALS_FIELD_KEY  = "initials"
CFG_ATLAS_GLANCE_AUTHORS_CERNCCID_FIELD_KEY  = "cernccid"
CFG_ATLAS_GLANCE_AUTHORS_INSPIRE_FIELD_KEY   = "inspireid"
CFG_ATLAS_GLANCE_AUTHORS_INSTITUTE_FIELD_KEY = "affiliation"
CFG_ATLAS_GLANCE_AUTHORS_EMAIL_FIELD_KEY     = "email"

# Special custom operator key and value when calling the API
# Example: _boolean will result to an empty string as a field
CFG_ATLAS_GLANCE_AUTHORS_OPERATOR_KEY        = ""
CFG_ATLAS_GLANCE_AUTHORS_OPERATOR_VALUE      = "_OPERATOR_"

# Mapping between our custom field keys and the ones used on ATLAS Glance,
# including the custom operator key and value.
CFG_ATLAS_GLANCE_AUTHORS_FIELDS = {
    CFG_ATLAS_GLANCE_AUTHORS_LASTNAME_FIELD_KEY  : "ATLASAUTHDBMEMBLASTNAME",
    CFG_ATLAS_GLANCE_AUTHORS_FIRSTNAME_FIELD_KEY : "ATLASAUTHDBMEMBFIRSTNAME",
    CFG_ATLAS_GLANCE_AUTHORS_INITIALS_FIELD_KEY  : "ATLASAUTHDBMEMBINITIALS",
    CFG_ATLAS_GLANCE_AUTHORS_CERNCCID_FIELD_KEY  : "ATLASAUTHDBMEMBCERNCCID",
    CFG_ATLAS_GLANCE_AUTHORS_INSPIRE_FIELD_KEY   : "ATLASAUTHDBMEMBINSPIRE",
    CFG_ATLAS_GLANCE_AUTHORS_INSTITUTE_FIELD_KEY : "ATLASAUTHDBMEMBINSTITUTE",
    CFG_ATLAS_GLANCE_AUTHORS_EMAIL_FIELD_KEY     : "ATLASAUTHDBMEMBEMAIL",
    CFG_ATLAS_GLANCE_AUTHORS_OPERATOR_KEY        : CFG_ATLAS_GLANCE_AUTHORS_OPERATOR_VALUE,
}

# Inversed mapping between our custom field keys and the ones used on ATLAS Glance
CFG_ATLAS_GLANCE_AUTHORS_FIELDS_INVERSED = dict((v,k) for k, v in CFG_ATLAS_GLANCE_AUTHORS_FIELDS.iteritems())

# Custom operator keys when calling the API
CFG_ATLAS_GLANCE_AUTHORS_CONTAINS_OPERATOR_KEY       = "contains"
CFG_ATLAS_GLANCE_AUTHORS_EQUAL_TO_OPERATOR_KEY       = "equals"
CFG_ATLAS_GLANCE_AUTHORS_DIFFERENT_THAN_OPERATOR_KEY = "not_equals"
CFG_ATLAS_GLANCE_AUTHORS_IS_EMPTY_OPERATOR_KEY       = "is_empty"
CFG_ATLAS_GLANCE_AUTHORS_IS_NOT_EMPTY_OPERATOR_KEY   = "is_not_empty"
CFG_ATLAS_GLANCE_AUTHORS_BOOLEAN_OPERATOR_KEY        = "boolean"

# Mapping between our custom operator keys and the ones used on ATLAS Glance
CFG_ATLAS_GLANCE_AUTHORS_OPERATORS = {
    CFG_ATLAS_GLANCE_AUTHORS_CONTAINS_OPERATOR_KEY       : "-1",
    CFG_ATLAS_GLANCE_AUTHORS_EQUAL_TO_OPERATOR_KEY       : "0",
    CFG_ATLAS_GLANCE_AUTHORS_DIFFERENT_THAN_OPERATOR_KEY : "5",
    CFG_ATLAS_GLANCE_AUTHORS_IS_EMPTY_OPERATOR_KEY       : "7",
    CFG_ATLAS_GLANCE_AUTHORS_IS_NOT_EMPTY_OPERATOR_KEY   : "8",
    CFG_ATLAS_GLANCE_AUTHORS_BOOLEAN_OPERATOR_KEY        : "op",
}

# Allowed values for each ATLAS Glance operator
CFG_ATLAS_GLANCE_AUTHORS_OPERATOR_KEY_ALLOWED_VALUES = {
    CFG_ATLAS_GLANCE_AUTHORS_OPERATORS[CFG_ATLAS_GLANCE_AUTHORS_BOOLEAN_OPERATOR_KEY] : ('or',
                                                                                         'and'),
}

# The actual value used by ATLAS Glance when a field is null or empty
CFG_ATLAS_GLANCE_AUTHORS_NULL_EMPTY_VALUE = "null_empty"

# Separator between fields and operators when calling the API
CFG_ATLAS_GLANCE_AUTHORS_FIELD_OPERATOR_SEPARATOR = "_"

# The GET parameter keys used in ATLAS Glance for field, operator and value
CFG_ATLAS_GLANCE_AUTHORS_FIELD_PARAMETER_KEY = "c"
CFG_ATLAS_GLANCE_AUTHORS_OPERATOR_PARAMETER_KEY = "o"
CFG_ATLAS_GLANCE_AUTHORS_VALUE_PARAMETER_KEY = "v"

# The GET parameter key used in ATLAS Glance for the number of search parameters defined
CFG_ATLAS_GLANCE_AUTHORS_NUMBER_OF_PARAMETERS_PARAMETER_KEY = "n"

# The GET parameter key used in ATLAS Glance for the boolean operator
CFG_ATLAS_GLANCE_AUTHORS_BOOLEAN_OPERATOR_PARAMETER_KEY = "op"

# The GET parameter key and value used in ATLAS Glance for the output format
CFG_ATLAS_GLANCE_AUTHORS_OUTPUT_FORMAT_PARAMETER_KEY = "of"
CFG_ATLAS_GLANCE_AUTHORS_OUTPUT_FORMAT_PARAMETER_VALUE = "json"

# The GET parameter key and value used in ATLAS Glance for the Search Interface ID (SIID)
CFG_ATLAS_GLANCE_AUTHORS_SIID_PARAMETER_KEY = "siid"
CFG_ATLAS_GLANCE_AUTHORS_SIID_PARAMETER_VALUE = "6016"

# The parts that make up the query URL for ATLAS Glance
CFG_ATLAS_GLANCE_AUTHORS_QUERY_URL_SCHEME   = "https"
CFG_ATLAS_GLANCE_AUTHORS_QUERY_URL_NETLOC   = "atglance.web.cern.ch"
CFG_ATLAS_GLANCE_AUTHORS_QUERY_URL_PATH     = "/atglance/cgi-bin/executeQuery"
CFG_ATLAS_GLANCE_AUTHORS_QUERY_URL_FRAGMENT = ""

# Webaccess source_name variable
CFG_SOURCE_NAME = "atlas"

def query_author_source(author_string):
    ## kwargs_dict = {}
    author_strings = author_string.replace("  "," ").split(" ")
   ## last_name = author_string.split(" ")[0]
   ## first_name = author_string.split(" ")[1]
    if len(author_strings) < 2:
        return query_atlas_glance_authors(lastname_contains=author_strings[0], firstname_contains=author_strings[0], _boolean='or')[0]
    elif len(author_string) == 2:
        return query_atlas_glance_authors(lastname_contains=author_strings[0], firstname_contains=author_strings[0], _boolean='or')[0]
    elif len(author_string) > 2:
        return query_atlas_glance_authors(lastname_contains=author_strings[0], firstname_contains=author_strings[0], _boolean='or')[0]
    else:
        return {}
   ## for last_name in last_names:
   ##     if last_name:
   ##         kwargs_dict["lastname_contains"].append(last_name)
   ## for first_name in first_names:
   ##     if first_name:
   ##         kwargs_dict["firstname_contains"].append(first_name)
   ## kwargs_dict["_boolean"]="and"
   ## return query_atlas_glance_authors(**kwargs_dict)
  ## return query_atlas_glance_authors(lastname_contains=last_name, firstname_contains=first_name, _boolean='or')

def query_atlas_glance_authors(**kwargs):
    """
    """

    results = {}
    error = None

    parsed_kwargs, parsed_operators, error = _query_atlas_glance_authors_parse_kwargs(kwargs)

    if error is None:

        query_url = _query_atlas_glance_authors_create_query(parsed_kwargs, parsed_operators)

        results_json, error = _query_atlas_glance_authors_execute_query(query_url)

        if error is None:

            if CFG_JSON_AVAILABLE:
                results = _query_atlas_glance_authors_parse_results(results_json)
            else:
                error = "Error: JSON is not available."

    return results, error

def _query_atlas_glance_authors_parse_kwargs(kwargs):
    """
    """

    parsed_kwargs = []
    parsed_operators = []
    error = None

    for (key, value) in kwargs.iteritems():
        field_and_operator = key.split(CFG_ATLAS_GLANCE_AUTHORS_FIELD_OPERATOR_SEPARATOR, 1)
        if len(field_and_operator) == 2:
            (field, operator) = field_and_operator
            parsed_field    = CFG_ATLAS_GLANCE_AUTHORS_FIELDS.get(field, None)
            parsed_operator = CFG_ATLAS_GLANCE_AUTHORS_OPERATORS.get(operator, None)
            if parsed_field is not None and parsed_operator is not None:
                if parsed_field == CFG_ATLAS_GLANCE_AUTHORS_OPERATOR_VALUE:
                    if value in CFG_ATLAS_GLANCE_AUTHORS_OPERATOR_KEY_ALLOWED_VALUES.get(parsed_operator, ()):
                        parsed_operators.append((parsed_operator, value))
                else:
                    if parsed_operator == CFG_ATLAS_GLANCE_AUTHORS_OPERATORS[CFG_ATLAS_GLANCE_AUTHORS_IS_EMPTY_OPERATOR_KEY]:
                        if value is False:
                            parsed_operator = CFG_ATLAS_GLANCE_AUTHORS_OPERATORS[CFG_ATLAS_GLANCE_AUTHORS_IS_NOT_EMPTY_OPERATOR_KEY]
                        value = CFG_ATLAS_GLANCE_AUTHORS_NULL_EMPTY_VALUE
                    elif parsed_operator == CFG_ATLAS_GLANCE_AUTHORS_OPERATORS[CFG_ATLAS_GLANCE_AUTHORS_IS_NOT_EMPTY_OPERATOR_KEY]:
                        if value is False:
                            parsed_operator = CFG_ATLAS_GLANCE_AUTHORS_OPERATORS[CFG_ATLAS_GLANCE_AUTHORS_IS_EMPTY_OPERATOR_KEY]
                        value = CFG_ATLAS_GLANCE_AUTHORS_NULL_EMPTY_VALUE
                    parsed_kwargs.append((parsed_field, parsed_operator, value))
            elif parsed_field is None and parsed_operator is None:
                error = 'Error: "%s" is not a valid field and "%s" is not a valid operator.' % (field, operator)
            elif parsed_field is None:
                error = 'Error: "%s" is not a valid field.' % (field, )
            elif parsed_operator is None:
                error = 'Error: "%s" is not a valid operator.' % (operator, )
        else:
            error = 'Error: "%s" is not a valid field and operator combination.' % (field_and_operator[0], )

    return parsed_kwargs, parsed_operators, error

def _query_atlas_glance_authors_create_query(parsed_kwargs, parsed_operators):
    """
    """

    query_parameters = []

    query_parameters.append((CFG_ATLAS_GLANCE_AUTHORS_SIID_PARAMETER_KEY,
                             CFG_ATLAS_GLANCE_AUTHORS_SIID_PARAMETER_VALUE))

    parsed_kwargs_len = len(parsed_kwargs)

    for parsed_kwarg_index in range(parsed_kwargs_len):
        (parsed_field, parsed_operator, value) = parsed_kwargs[parsed_kwarg_index]
        query_parameters.append((CFG_ATLAS_GLANCE_AUTHORS_FIELD_PARAMETER_KEY + str(parsed_kwarg_index),
                                 parsed_field))
        query_parameters.append((CFG_ATLAS_GLANCE_AUTHORS_OPERATOR_PARAMETER_KEY + str(parsed_kwarg_index),
                                 parsed_operator))
        query_parameters.append((CFG_ATLAS_GLANCE_AUTHORS_VALUE_PARAMETER_KEY + str(parsed_kwarg_index),
                                 value))

    query_parameters.append((CFG_ATLAS_GLANCE_AUTHORS_NUMBER_OF_PARAMETERS_PARAMETER_KEY,
                             str(parsed_kwargs_len)))

    query_parameters.extend(parsed_operators)

    query_parameters.append((CFG_ATLAS_GLANCE_AUTHORS_OUTPUT_FORMAT_PARAMETER_KEY,
                             CFG_ATLAS_GLANCE_AUTHORS_OUTPUT_FORMAT_PARAMETER_VALUE))

    query = urlencode(query_parameters)

    query_url = urlunsplit((CFG_ATLAS_GLANCE_AUTHORS_QUERY_URL_SCHEME,
                            CFG_ATLAS_GLANCE_AUTHORS_QUERY_URL_NETLOC,
                            CFG_ATLAS_GLANCE_AUTHORS_QUERY_URL_PATH,
                            query,
                            CFG_ATLAS_GLANCE_AUTHORS_QUERY_URL_FRAGMENT))

    return query_url

def _query_atlas_glance_authors_execute_query(query_url):
    """
    """

    results = None
    error = None

    try:
        # TODO: have a timeout
        response = urlopen(query_url)
        results = response.read()
    except Exception, e:
        error = "Error: %s" % (str(e), )

    return results, error

def _query_atlas_glance_authors_parse_results(results_json):
    """
    """

    results = []

    results_dict = json.loads(results_json)

    # TODO: De-hardcode 'id', 'metadata' and 'results'
    # They custom JSON names coming from ATLAS Glance
    results_fields = [CFG_ATLAS_GLANCE_AUTHORS_FIELDS_INVERSED[results_field['id']]
                      for results_field
                      in results_dict['metadata']]

    results = [dict(zip(results_fields ,results_result))
               for results_result
               in results_dict['results']]

    return results
