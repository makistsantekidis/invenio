#onverts the field value (from its repective file) from JSON to a format that bibconvert understands
## Copyright (C) 2004, 2005, 2006, 2007, 2008, 2010, 2011, 2012, 2013, 2014 CERN.
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

__revision__ = "$Id$"

import os
import json
from invenio.websubmit_functions.Shared_Functions import get_dictionary_from_string,ParamFromFile,write_file
from invenio.websubmit_config import CFG_SUBFIELD_DEFINITIONS,CFG_JSON_TO_TPL_FIELDS,CFG_AUTHORITY_CONTAINER_DICTIONARY,CFG_TPL_FIELDS

def encapsulate_id(id_dict,key,value):
    if key in id_dict and str(value).strip():
        return id_dict[key]%value
    else:
        return value



def Convert_Field_from_Json(parameters, curdir, form, user_info=None):
    """
    Converts the field value (from its repective file) from JSON to a format that bibconvert understands
    """
    global sysno

    ## the name of the field that has the json inside
    json_field = parameters.get("authors_json_field",None)

    ## separators in case a field has more than one values
    field_key_to_separator = { 'AUTHOR_ID' : '</subfield><subfield code="%s">' % CFG_SUBFIELD_DEFINITIONS['id'], 'DEMOTHE_AU' : ', '}

    filename = "%s/%s" % (curdir,json_field)
    if os.path.exists(filename):

        ## open the file that corresponds to the field
        ## and read its contents into a dictionary
        json_str = ParamFromFile(os.path.join(curdir,filename))
        obj = json.loads(json_str)

        field_values = []
        ## for all the items in the field iterate their key,value
        ## and place them with their transalte from json key in
        ## the field_values dictionary
        for items in obj['items']:
            field_values.append(dict(CFG_TPL_FIELDS))
            for k,v in items.iteritems():
                if CFG_JSON_TO_TPL_FIELDS.get(k):
                    if field_values[-1].get(CFG_JSON_TO_TPL_FIELDS[k]) and field_key_to_separator.get(CFG_JSON_TO_TPL_FIELDS[k]):
                        field_values[-1][CFG_JSON_TO_TPL_FIELDS[k]] += \
                                field_key_to_separator[CFG_JSON_TO_TPL_FIELDS[k]] + encapsulate_id(CFG_AUTHORITY_CONTAINER_DICTIONARY,k,v)
                    else:
                        field_values[-1][CFG_JSON_TO_TPL_FIELDS[k]] = encapsulate_id(CFG_AUTHORITY_CONTAINER_DICTIONARY,k,v)
        fields = list(set(CFG_JSON_TO_TPL_FIELDS.itervalues()))
        ## For every field that must be saved in the, use the name
        ## of the previous
        for field in fields:
            attributes_to_write = []
            for field_value in field_values:
                val = str(field_value.get(field,"")).strip().encode('string_escape')
                if not val:
                    val = "#None#"
                attributes_to_write.append(val)
            attributes_to_write = "\n".join(attributes_to_write)
            write_file(os.path.join(curdir,field),attributes_to_write)
