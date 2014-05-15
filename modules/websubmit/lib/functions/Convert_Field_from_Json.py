#onverts the field value (from its repective file) from JSON to a format that bibconvert understands
## Copyright (C) 2004, 2005, 2006, 2007, 2008, 2010, 2011 CERN.
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


def encapsulate_id(id_dict,key,value):
    if (type(value) == list):
        f = open('/tmp/qweasdzxc','w')
        f.write(str(value))
        f.close()
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
    json_field = parameters.get("json_field",None)


    from invenio.websubmit_functions.Shared_Functions import get_dictionary_from_string
    ## Dictionary that translates json keys to tpl keys
    params_rename_me = parameters.get("json_to_tpl_fields","")
    json_to_tpl_fields = get_dictionary_from_string(params_rename_me)

    ## separators in case a field has more than one values
    field_key_to_separator = { 'AUTHOR_ID' : '</subfield><subfield code="x">', 'DEMOTHE_AU' : ', '}

    authority_container_dictionary = get_dictionary_from_string(parameters.get("authority_container_dictionary",""))


    filename = "%s/%s" % (curdir,json_field)
    if os.path.exists(filename):

        ## open the file that corresponds to the field
        ## and read its contents into a dictionary
        fp = open(os.path.join(curdir,filename),"r")
        obj = json.loads(fp.read())
        fp.close()

        field_values = []
        ## for all the items in the field iterate their key,value
        ## and place them with their transalte from json key in
        ## the field_values dictionary
        for items in obj['items']:
            field_values.append(reduce(lambda x,y: x.update(y) or x,[{f:""} for f in set(json_to_tpl_fields.itervalues())]))
            for k,v in items.iteritems():
                if json_to_tpl_fields.get(k,None):
                    if not field_values[-1].get(json_to_tpl_fields[k],None):
                        field_values[-1][json_to_tpl_fields[k]] = encapsulate_id(authority_container_dictionary,k,v)
                    else:
                        field_values[-1][json_to_tpl_fields[k]] += \
                                field_key_to_separator[json_to_tpl_fields[k]] + encapsulate_id(authority_container_dictionary,k,v)

        files = {}
        fields = [field for field in json_to_tpl_fields.itervalues()]
        ## For every field that must be saved in the, use the name
        ## of the previous
        for field in fields:
            fp = open(os.path.join(curdir,field),"w")
            for field_value in field_values:
                fp.write(str(field_value.get(field,"")).strip().encode('string_escape') + "\n")
            fp.close()

    return ""


