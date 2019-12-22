import io
import os
import xml.etree.ElementTree as ET

import preprocessing.remove_html
import preprocessing.init_akoma
from tokenizer.HTMLTokenizer import HTMLTokenizer

from form_akoma.AkomaBuilder import AkomaBuilder
from reasoner.BasicReasoner import BasicReasoner
from reasoner.OdlukaReasoner import OdlukaReasoner
from form_akoma.MetadataBuilder import MetadataBuilder
from named_enitity_recognition.pattern_recognition import add_refs

if __name__ == "__main__":
    nastavi = "651.html"
    idemo = False
    stani = ["1160.html", "1575.html", "908.html", "2348.html", "318.html", "3062.html"] #ovi fajlovi su samo preveliki pa njihovo procesiranje traje dugo
    for fajl in os.listdir("data/aktovi_html"):
        if(fajl == nastavi):
            idemo=True
        if not idemo:
            continue
        if fajl in stani:
            continue
        print(fajl)
        stringo = preprocessing.remove_html.preprocessing("data/aktovi_html/"+fajl)
        akoma_root = preprocessing.init_akoma.init_xml("act")
        #break
        #f = io.open('data/aktovi_raw/' +fajl, mode="w", encoding="utf-8")
        #f.write(stringo)
       # f.close()

        html_root = ET.fromstring("<article>" + stringo + "</article>")
        #form_akoma.structure.fill_body(akoma_root, html_root)

        metabuilder = MetadataBuilder("data/metadata.csv")
        metabuilder.build(fajl, akoma_root)
        try: #just in case
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
            f = io.open('data/akoma_result/' + fajl[:-5]+".xml", mode="w", encoding="utf-8")
            f.write(result_str)
            f.close()
        except:
            continue
