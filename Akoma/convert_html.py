import io
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

try:
    from utilities import ETree
    from Akoma.preprocessing import init_akoma
    from Akoma.tokenizer.HTMLTokenizer import HTMLTokenizer
    from Akoma.form_akoma.AkomaBuilder import AkomaBuilder
    from Akoma.reasoner.BasicReasoner import BasicReasoner
    from Akoma.reasoner.OdlukaReasoner import OdlukaReasoner
    from Akoma.form_akoma.MetadataBuilder import MetadataBuilder
    from Akoma.named_enitity_recognition.references import add_refs
except ModuleNotFoundError:
    try:
        from utilities import ETree
        from preprocessing import init_akoma
        from tokenizer.HTMLTokenizer import HTMLTokenizer
        from form_akoma.AkomaBuilder import AkomaBuilder
        from reasoner.BasicReasoner import BasicReasoner
        from reasoner.OdlukaReasoner import OdlukaReasoner
        from form_akoma.MetadataBuilder import MetadataBuilder
        from named_enitity_recognition.pattern_recognition import add_refs
        from convertToLatin import regex_patterns
    except ModuleNotFoundError:
        print("Error in convert_html.py importing modules")
        exit(-1)

"""
    source should be somethin like "data/aktovi_html/2126.html"
    destination is the path for the result xml file
"""


def convert_html(source, destination):
    try:
        f = open(source, mode="r", encoding="UTF-8")
    except FileNotFoundError as error:
        print(error)
    text = "".join(f.readlines())
    text = regex_patterns.strip_html_tags_exept(text)
    fajl = source.split("/")[-1]
    akoma_root = init_akoma.init_xml("act")
    try:
        html_root = ET.fromstring("<article>" + text + "</article>")
    except Exception as e:
        got = BeautifulSoup(text, "lxml")
        text = got.prettify().replace("<html>", "").replace("</html>", "").replace("<body>", "").replace("</body", "")
        html_root = ET.fromstring("<article>" + text + "</article>")

    metabuilder = MetadataBuilder("data/meta/allmeta.csv")
    metabuilder.build(fajl, akoma_root)
    builder = AkomaBuilder(akoma_root)
    reasoner = BasicReasoner(HTMLTokenizer(html_root), builder)
    reasoner.start()

    if reasoner.current_hierarchy[4] == 0:
        akoma_root = init_akoma.init_xml("act")
        metabuilder = MetadataBuilder("data/meta/allmeta.csv")
        metabuilder.build(fajl, akoma_root)

        builder = AkomaBuilder(akoma_root)
        reasoner = OdlukaReasoner(HTMLTokenizer(html_root), builder)
        reasoner.start()

    result_str = builder.result_str()
    result_stablo = add_refs(akoma_root, result_str, metabuilder.expressionuri)
    result_str = ETree.prettify(result_stablo).replace("&lt;", "<").replace("&gt;", ">").replace("&quot;",                                                                                                 "\"").replace(
        '<references source="#somebody"/>', "")
    f = io.open(destination, mode="w", encoding="utf-8")
    f.write(result_str)
    f.close()


import sys

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        convert_html(sys.argv[1], sys.argv[2])
    else:
        convert_html("data/acts/1.html", "data/akoma_result/ustav.xml")
