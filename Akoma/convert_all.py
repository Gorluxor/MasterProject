import io
import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

try:
    import Akoma
    from Akoma.convertToLatin import regex_patterns
    from Akoma.utilities import ETree, utilities
    from Akoma.preprocessing import init_akoma
    from Akoma.tokenizer.HTMLTokenizer import HTMLTokenizer
    from Akoma.form_akoma.AkomaBuilder import AkomaBuilder
    from Akoma.reasoner.BasicReasoner import BasicReasoner
    from Akoma.reasoner.OdlukaReasoner import OdlukaReasoner
    from Akoma.form_akoma.MetadataBuilder import MetadataBuilder
    from Akoma.named_enitity_recognition.references import add_refs
except ModuleNotFoundError as sureError:
    try:
        from utilities import ETree, utilities
        from convertToLatin import regex_patterns
        from preprocessing import init_akoma
        from tokenizer.HTMLTokenizer import HTMLTokenizer
        from form_akoma.AkomaBuilder import AkomaBuilder
        from tokenizer import patterns
        from reasoner.BasicReasoner import BasicReasoner
        from reasoner.OdlukaReasoner import OdlukaReasoner
        from form_akoma.MetadataBuilder import MetadataBuilder
        from named_enitity_recognition.references import add_refs
    except ModuleNotFoundError as newError:
        if not sureError.name.__eq__("Akoma") or not newError.name.__eq__("Akoma"):
            print(newError)
            print("Error")
            exit(-1)


def structure_repair_one(act: str, tag_name: str):
    import re
    text_find = "<\/" + tag_name + ">"
    text_replace = "</" + tag_name + ">"
    text_to_find = r'' + text_find + "[ ]*" + text_find
    act = re.sub(text_to_find, text_replace, act)
    return act


def structure_repair(act: str):
    exepted_tag = ["p", "table", "tr", "td", "img", "th"]
    for i in range(0, len(exepted_tag)):
        act = structure_repair_one(act, exepted_tag[i])
    return act


def advance_repair_mode(act: str):
    pass


def repair_mode(act: str):
    import re
    while re.search("(\n\n\n|  )", act) is not None:
        act = act.replace("\n\n\n", "\n\n")
        act = act.replace("  ", " ")
    get_title = re.search(patterns.ARTICLE_NAME, act.upper())
    if get_title is None:
        print("Convert_all>repair mode fail")
        exit(-1)
    root_art = ET.Element("article")
    if get_title.span(0)[0] is not 0:
        title_el = ET.Element('p')
        title_el.text = act[0:get_title.span(0)[0]]
        root_art.append(title_el)
    opening = True
    text_from = -1
    text_to = -1
    pattern_to_find = "\n."
    # pattern_to_find = "\n\n."
    searcher = re.compile(pattern_to_find)
    for m in searcher.finditer(act):
        cord = m.span(0)
        if opening:
            text_from = cord[0] + 2
            opening = not opening
        else:
            text_to = cord[1] - 3
            new_el = ET.Element('p')
            new_el.text = act[text_from:text_to]
            text_from = text_to + 2
            root_art.append(new_el)
    new_el = ET.Element('p')
    new_el.text = act[text_from:len(act)]
    root_art.append(new_el)
    # fixed = ETree.prettify(root_art)
    # print(fixed)
    return root_art


def apply_akn_tags(text: str, meta_name: str, skip_tfidf=False):
    """
    Applies to text Akoma Ntoso 3.0 tags for Republic of Serbia regulations
    :param text: HTML or plain text
    :param meta_name: name which was meta added 15 tag in meta
    :param skip_tfidf: Don't add references> TLCconcept for document
    :return: Labeled xml string
    """
    akoma_root = init_akoma.init_xml("act")
    repaired = False
    if text.find("<p") == -1:
        repaired = True
        new_html_root = repair_mode(text)
    else:
        text = regex_patterns.strip_html_tags_exept(text)
    if not repaired:
        try:
            html_root = ET.fromstring("<article>" + text + "</article>")
        except Exception as e:
            got = BeautifulSoup(text, "lxml")
            text = got.prettify().replace("<html>", "").replace("</html>", "").replace("<body>", "").replace("</body",
                                                                                                             "")
            html_root = ET.fromstring("<article>" + text + "</article>")
    elif repaired:
        html_root = new_html_root

    metabuilder = MetadataBuilder("data/meta/allmeta.csv")
    metabuilder.build(meta_name, akoma_root, skip_tfidf)
    print(ETree.prettify(akoma_root))
    builder = AkomaBuilder(akoma_root)
    reasoner = BasicReasoner(HTMLTokenizer(html_root), builder)
    reasoner.start()

    if reasoner.current_hierarchy[4] == 0:
        akoma_root = init_akoma.init_xml("act")
        metabuilder = MetadataBuilder("data/meta/allmeta.csv")
        metabuilder.build(fajl, akoma_root, skip_tfidf=skip_tfidf)

        builder = AkomaBuilder(akoma_root)
        reasoner = OdlukaReasoner(HTMLTokenizer(html_root), builder)
        reasoner.start()

    result_str = builder.result_str()
    # try:
    result_stablo = add_refs(akoma_root, result_str, metabuilder.expressionuri)
    # except Exception as e:
    #     file_ref_exeption = open(utilities.get_root_dir() + "/data/" + "za_ninu.txt", mode="a+")
    #     file_ref_exeption.write(meta_name + ":" + str(e) + "\n")
    #     file_ref_exeption.close()
    #     return result_str
    result_str = ETree.prettify(result_stablo).replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"").replace(
        '<references source="#somebody"/>', "")
    return result_str


def convert_html(source, destination):
    try:
        opened = io.open(source, mode="r", encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError("File not exist")
    text = "".join(opened.readlines())
    full_strip = regex_patterns.strip_html_tags_exept(text)
    # full_strip = remove_html.preprocessing(source)  # full_strip = remove_html.preprocessing(source, full_strip=True)
    meta_file_name = source.split("/")[-1]
    result_str = apply_akn_tags(full_strip, meta_file_name, skip_tfidf=True)
    f = io.open(destination, mode="w", encoding="utf-8")
    f.write(result_str)
    f.close()


if __name__ == "__main__":
    nastavi = "1205.html"  # ""651.html"
    idemo = False
    stani = [
        "1005.html", "980.html", "986.html", "981.html", "210.html", "1033", "1204"  # problematicni PROVERITI 176
        , "180.html"]  # Veliki fajlovi
    location_source = "data/acts"
    fajls = utilities.sort_file_names(os.listdir(location_source))

    for fajl in fajls:
        if (fajl == nastavi):
            idemo = True
        if not idemo:
            continue
        if fajl in stani:
            continue
        print(fajl)
        # try:
        convert_html(location_source + '/' + fajl, 'data/akoma_result/' + fajl[:-5] + ".xml")
        # except Exception as e:
        #     file_ref_exeption = open(utilities.get_root_dir() + "/data/" + "za_andriju.txt", mode="a+")
        #     file_ref_exeption.write(fajl + ":" + str(e) + "\n")
        #     file_ref_exeption.close()
