from urllib2 import urlopen,quote
from lxml import etree
from invenio.bibformat_engine import BibFormatObject

CFG_VIAF_WIKIPEDIA_LINK_BFO_FIELD = "848"
CFG_VIAF_WIKIPEDIA_NAME_LABEL_SUBFIELD = 'a'
CFG_VIAF_WIKIPEDIA_NAME_VALUE_SUBFIELD = 'wikipedia'
CFG_VIAF_WIKIPEDIA_LINK_SUBFIELD = 'l'
CFG_VIAF_BASE_URL = 'http://viaf.org/'
CFG_VIAF_XML_NAMESPACES = {"ns2":"http://viaf.org/viaf/terms#", "foaf" : "http://xmlns.com/foaf/0.1/",\
                           "owl" : "http://www.w3.org/2002/07/owl#", "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#" ,\
                            "void" : "http://rdfs.org/ns/void#"}

def get_wikipedia_link(viaf_id):
    url = CFG_VIAF_BASE_URL + "viaf/" + str(viaf_id) +"/viaf.xml"
    string_xml = urlopen(url).read()
    xml = etree.fromstring(str(string_xml))
    author_wikipedia_id = xml.xpath("/ns2:VIAFCluster/ns2:sources/ns2:source[contains(text(),'WKP')]/@nsid",namespaces={"ns2":"http://viaf.org/viaf/terms#"})
    url_to_wikipedia = None
    if type(author_wikipedia_id) is list and author_wikipedia_id:
        author_wikipedia_id = author_wikipedia_id[0]
        url_to_wikipedia = "http://www.wikipedia.com/wiki/"+author_wikipedia_id
    return url_to_wikipedia


def get_possible_matches(author_name):
    url = CFG_VIAF_BASE_URL + 'viaf/search/?query=' + quote('local.mainHeadingEl='+author_name) + '&httpAccept=application/xml'
    string_xml = urlopen(url).read()
    xml = etree.fromstring(str(string_xml))
    author_resourses_xmlnodes = xml.xpath('//ns2:VIAFCluster',namespaces=CFG_VIAF_XML_NAMESPACES)
    possible_matches = []
    for author in author_resourses_xmlnodes:
        possible_matches.append({})
        possible_matches[-1]['names'] = [x.text for x in author.xpath("./ns2:mainHeadings/ns2:data/ns2:text",namespaces=CFG_VIAF_XML_NAMESPACES)]
        possible_matches[-1]['viaf'] = author.xpath("./ns2:viafID",namespaces=CFG_VIAF_XML_NAMESPACES)[0].text
        possible_matches[-1]['link'] = CFG_VIAF_BASE_URL + 'viaf/' + possible_matches[-1]['viaf']
    return possible_matches



def get_wiki_link_from_bfo(bfo):
    link = None
    fields = []
    if type(bfo) is BibFormatObject:
        fields = bfo.fields(CFG_VIAF_WIKIPEDIA_LINK_BFO_FIELD)
    else:
        fields = bfo.get(CFG_VIAF_WIKIPEDIA_LINK_BFO_FIELD,[])
    for field in fields:
        if type(field) is dict:
            if field.get(CFG_VIAF_WIKIPEDIA_NAME_LABEL_SUBFIELD) == CFG_VIAF_WIKIPEDIA_NAME_VALUE_SUBFIELD:
                link = field.get(CFG_VIAF_WIKIPEDIA_LINK_SUBFIELD)
        else:
            record_dict = {}
            for subfields in field:
                if type(subfields) is list:
                    for subfield in subfields:
                        record_dict[subfield[0]] = subfield[1]
            if record_dict.get(CFG_VIAF_WIKIPEDIA_NAME_LABEL_SUBFIELD) == CFG_VIAF_WIKIPEDIA_NAME_VALUE_SUBFIELD:
                link = record_dict.get(CFG_VIAF_WIKIPEDIA_LINK_SUBFIELD)
    return link



