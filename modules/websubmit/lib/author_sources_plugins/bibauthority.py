from invenio.search_engine import perform_request_search
from invenio.bibfield import get_record
from invenio.bibfield_utils import retrieve_authorid_type,retrieve_authorid_id
from invenio.websubmit_config import CFG_SUBFIELFD_TO_JSON_FIELDS

CFG_SOURCE_NAME = 'bibauthority'

def query_author_source(nickname):
    rec_ids = perform_request_search(c="People",p=nickname)
    authors = []
    for _id in rec_ids[:20]:
        rec = get_record(_id)
        author = {
                'name' : rec['authors'][0]['full_name'],
                }
        author.update({
                CFG_SUBFIELFD_TO_JSON_FIELDS['x'].get(retrieve_authorid_type(x['value']))
                or retrieve_authorid_type(x['value']):retrieve_authorid_id(x['value'])
                for x in rec['system_control_number']
                })
        authors.append(author)
    return authors

