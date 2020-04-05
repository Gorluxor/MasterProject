import io
import os
import xml.etree.ElementTree as ET

try:
    from Akoma.utilities import ETree
    from Akoma.preprocessing import remove_html
    from Akoma.preprocessing import init_akoma
    from Akoma.tokenizer.HTMLTokenizer import HTMLTokenizer
    from Akoma.form_akoma.AkomaBuilder import AkomaBuilder
    from Akoma.reasoner.BasicReasoner import BasicReasoner
    from Akoma.reasoner.OdlukaReasoner import OdlukaReasoner
    from Akoma.form_akoma.MetadataBuilder import MetadataBuilder
    from Akoma.named_enitity_recognition.pattern_recognition import add_refs
except ModuleNotFoundError:
    try:
        from utilities import ETree
        from preprocessing import remove_html
        from preprocessing import init_akoma
        from tokenizer.HTMLTokenizer import HTMLTokenizer
        from form_akoma.AkomaBuilder import AkomaBuilder
        from reasoner.BasicReasoner import BasicReasoner
        from reasoner.OdlukaReasoner import OdlukaReasoner
        from form_akoma.MetadataBuilder import MetadataBuilder
        from named_enitity_recognition.pattern_recognition import add_refs
    except ModuleNotFoundError:
        print("Error")
        exit(-1)


def prettify(root):
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(ET.tostring(root, encoding='UTF-8', method="xml").decode())
    return dom.toprettyxml()


def convert_html(source, destination):
    stringo = remove_html.preprocessing(source)
    fajl = source.split("/")[-1]
    akoma_root = init_akoma.init_xml("act")

    html_root = ET.fromstring("<article>" + stringo + "</article>")

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
    ET.dump(builder.akomaroot)
    print(prettify(akoma_root))
    result_str = add_refs(result_str, metabuilder.expressionuri)
    f = io.open(destination, mode="w", encoding="utf-8")
    f.write(result_str)
    f.close()


if __name__ == "__main__":
    nastavi = "85.html"  # ""651.html"
    idemo = False
    stani = [
        "562.html"]  # ["1160.html", "1575.html", "908.html", "2348.html", "318.html", "3062.html"] #ovi fajlovi su samo preveliki pa njihovo procesiranje traje dugo
    location_source = "data/acts"
    fajls = os.listdir(location_source)
    for fajl in fajls:
        if (fajl == nastavi):
            idemo = True
        if not idemo:
            continue
        if fajl in stani:
            continue
        convert_html(location_source + '/' + fajl, 'data/akoma_result/' + fajl[:-5] + ".xml")
