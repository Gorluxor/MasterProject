import io
import xml.etree.ElementTree as ET

import preprocessing.remove_html
import preprocessing.init_akoma
from tokenizer.HTMLTokenizer import HTMLTokenizer

from form_akoma.AkomaBuilder import AkomaBuilder
from reasoner.BasicReasoner import BasicReasoner
from reasoner.OdlukaReasoner import OdlukaReasoner
from form_akoma.MetadataBuilder import MetadataBuilder
from named_enitity_recognition.pattern_recognition import add_refs


"""
    source should be somethin like "data/aktovi_html/2126.html"
    destination is the path for the result xml file
"""
def convert_html(source, destination):
    stringo = preprocessing.remove_html.preprocessing(source)
    fajl = source.split("/")[-1]
    akoma_root = preprocessing.init_akoma.init_xml("act")

    html_root = ET.fromstring("<article>" + stringo + "</article>")

    metabuilder = MetadataBuilder("data/metadata.csv")
    metabuilder.build(fajl, akoma_root)
    builder = AkomaBuilder(akoma_root)
    reasoner = BasicReasoner(HTMLTokenizer(html_root), builder)
    reasoner.start()

    if reasoner.current_hierarchy[4] == 0:
        akoma_root = preprocessing.init_akoma.init_xml("act")
        metabuilder = MetadataBuilder("data/metadata.csv")
        metabuilder.build(fajl, akoma_root)

        builder = AkomaBuilder(akoma_root)
        reasoner = OdlukaReasoner(HTMLTokenizer(html_root), builder)
        reasoner.start()

    result_str = builder.result_str()
    result_str = add_refs(result_str, metabuilder.expressionuri)
    f = io.open(destination, mode="w", encoding="utf-8")
    f.write(result_str)
    f.close()

import sys
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        convert_html(sys.argv[1], sys.argv[2])
    else:
        convert_html("data/aktovi_html/2126.html", "data/ustav.xml")