from invenio.dbquery import run_sql


def get_cmtrecordcomment_to_bibdocfile_association(recID):
    """
    Retrieves all the associations between the comments of a record
    and bibdocfiles they refer to.
    :param recID: Id of the record
    :return: correlations between comments and bibdocfiles
    """
    query = """SELECT *
               FROM cmtRECORDCOMMENT_bibdocfile
               WHERE id_record = %s"""
    import json
    res = run_sql(query, (recID,), with_dict=True)

    return json.dumps(res)

def add_comment_to_file_association(redID, cmtID, bibdocfileID, version, mime):
    """
    Adds an association of a comment to a bibdocfile
    :param redID: Id of the record
    :param cmtID: Id of the comment
    :param bibdocfileID: Id of the bibdocfile
    """
    query = """INSERT INTO cmtRECORDCOMMENT_bibdocfile
             (id_record, id_comment, id_bibdoc, version, mime)
             VALUES (%s, %s, %s, %s, %s)"""
    res = run_sql(query, (redID, cmtID, bibdocfileID, version, mime))
    return res


def get_bibdocfiles_of_record(recID, only_used_p=False):
    """
    Retrieves all bibdocfiles associated with a record
    :param recID: Id of the record
    :return: array of dictionaries with each dictionary representing a bibdocfile
    """
    if only_used_p:
        query = """SELECT id_record, cmtRECORDCOMMENT_bibdocfile.id_bibdoc, version, mime, docname
                   FROM cmtRECORDCOMMENT_bibdocfile INNER JOIN bibdocfsinfo
                   ON cmtRECORDCOMMENT_bibdocfile.id_bibdoc = bibdocfsinfo.id_bibdoc
                   WHERE cmtRECORDCOMMENT_bibdocfile.id_record = %s
                    """
    else:
        query = """SELECT docname, version, mime, id_bibrec, bibdocfsinfo.id_bibdoc
                   FROM bibrec_bibdoc INNER JOIN bibdocfsinfo
                   ON bibrec_bibdoc.id_bibdoc = bibdocfsinfo.id_bibdoc
                   WHERE bibrec_bibdoc.id_bibrec = %s
                    """
    res = run_sql(query, (recID,),  with_dict=True)
    return res


