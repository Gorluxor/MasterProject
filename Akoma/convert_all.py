import io
import os
import xml.etree.ElementTree as ET

try:
    import Akoma
    from Akoma.utilities import ETree
    from Akoma.preprocessing import remove_html
    from Akoma.preprocessing import init_akoma
    from Akoma.tokenizer.HTMLTokenizer import HTMLTokenizer
    from Akoma.form_akoma.AkomaBuilder import AkomaBuilder
    from Akoma.reasoner.BasicReasoner import BasicReasoner
    from Akoma.reasoner.OdlukaReasoner import OdlukaReasoner
    from Akoma.form_akoma.MetadataBuilder import MetadataBuilder
    from Akoma.named_enitity_recognition.pattern_recognition import add_refs
except ModuleNotFoundError as sureError:
    try:
        from utilities import ETree
        from preprocessing import remove_html
        from preprocessing import init_akoma
        from tokenizer.HTMLTokenizer import HTMLTokenizer
        from form_akoma.AkomaBuilder import AkomaBuilder
        from tokenizer import patterns
        from reasoner.BasicReasoner import BasicReasoner
        from reasoner.OdlukaReasoner import OdlukaReasoner
        from form_akoma.MetadataBuilder import MetadataBuilder
        from named_enitity_recognition.pattern_recognition import add_refs
    except ModuleNotFoundError as newError:
        if not sureError.name.__eq__("Akoma") or not newError.name.__eq__("Akoma"):
            print(newError)
            print("Error")
            exit(-1)


def repair_mode(act):
    # TODO if time, Work in progress, Andrija zavrsiti
    # got = patterns.recognize_pattern(act)

    return act


def prettify(root):
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(ET.tostring(root, encoding='UTF-8', method="xml").decode())
    return dom.toprettyxml()


def apply_akn_tags(text: str, meta_name: str):
    """
    Applies to text Akoma Ntoso 3.0 tags for Republic of Serbia regulations
    :param text: HTML or plain text
    :param meta_name: name which was meta added 15 tag in meta
    :return: Labeled xml string
    """
    akoma_root = init_akoma.init_xml("act")
    if text.find("<p") == -1:
        text = repair_mode(text)
    html_root = ET.fromstring("<article>" + text + "</article>")

    metabuilder = MetadataBuilder("data/meta/allmeta.csv")
    metabuilder.build(meta_name, akoma_root)
    print(prettify(akoma_root))
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
    result_str = prettify(result_stablo).replace("&lt;","<").replace("&gt;",">").replace("&quot;","\"")
    return result_str


def convert_html(source, destination):
    stringo = remove_html.preprocessing(source)
    full_strip = remove_html.preprocessing(source, full_strip=True)
    meta_file_name = source.split("/")[-1]
    result_str = apply_akn_tags(stringo, meta_file_name)
    f = io.open(destination, mode="w", encoding="utf-8")
    f.write(result_str)
    f.close()


if __name__ == "__main__":
    nastavi = "464.html"  # ""651.html"
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
        print(fajl)
        convert_html(location_source + '/' + fajl, 'data/akoma_result/' + fajl[:-5] + ".xml")
