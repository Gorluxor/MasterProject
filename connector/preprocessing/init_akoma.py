import xml.etree.ElementTree as ET
import re

"""
    Used to fix parts of a html file that are unreadable to ElementTree; if needed.
"""
def trash(stringo):

    #tree = ET.parse('../aktovi/1.html')
    #print(stringo)
    stringo = close_html_token("meta", stringo)
    stringo = close_html_token("link", stringo)
    stringo = close_html_token("img", stringo)
    stringo = close_html_token_exact("col", stringo)
    stringo = add_fake_root_node(stringo)
    #print(stringo)
    root = ET.fromstring(stringo)

    #for child in root:
     #   print(child.tag, child.attrib)

def close_html_token(token, stringo):
    m = re.search('(<'+token+')(.*?)(>)', stringo)
    if m:
        return stringo[:m.end()] + u"</"+token+">" + stringo[m.end():]
    return stringo


def close_html_token_exact(token, stringo):
    m = re.search('(<'+token+'>)', stringo)
    if m:
        return stringo[:m.end()] + u"</"+token+">" + stringo[m.end():]
    return stringo

def add_fake_root_node(stringo):
    return u"<article>" + stringo + u"</article>"

def init_xml(type):
    retval = ''#'< ?xml version = "1.0" encoding = "UTF-8"? >\n'
    retval += '<akomaNtoso '
    retval += 'xmlns = "http://www.akomantoso.org/2.0" '
    retval += 'xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance" '
    retval += 'xsi:schemaLocation = "http://www.akomantoso.org/2.0 ./akomantoso20.xsd" >\n'

    retval += '<'+type+'><meta></meta><body></body></'+type+'>'
    retval += '</akomaNtoso>'
    #print(retval)
    ET.register_namespace('', "http://www.akomantoso.org/2.0")
    root = ET.fromstring(retval)
    print("SADAD", list(list(root)[0]))
    return root
