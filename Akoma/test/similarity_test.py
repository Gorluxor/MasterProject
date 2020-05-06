import difflib
import os
import re
import statistics
import xml.etree.ElementTree as ET
from functools import reduce

try:
    from Akoma.utilities import utilities
    from Akoma.utilities import ETree
except ModuleNotFoundError:
    try:
        from utilities import utilities
        from utilities import ETree
    except ModuleNotFoundError:
        print("Import error")
        exit(-1)

map_found_org = {
    ETree.get_akoma_tag("deo"): 0,
    ETree.get_akoma_tag("glava"): 0,
    ETree.get_akoma_tag("odeljak"): 0,
    ETree.get_akoma_tag("pododeljak"): 0,
    ETree.get_akoma_tag("clan"): 0,
    ETree.get_akoma_tag("stav"): 0,
    ETree.get_akoma_tag("tacka"): 0,
    ETree.get_akoma_tag("podtacka"): 0,
    ETree.get_akoma_tag("alinea"): 0}

map_found_new = {
    ETree.get_akoma_tag("deo"): 0,
    ETree.get_akoma_tag("glava"): 0,
    ETree.get_akoma_tag("odeljak"): 0,
    ETree.get_akoma_tag("pododeljak"): 0,
    ETree.get_akoma_tag("clan"): 0,
    ETree.get_akoma_tag("stav"): 0,
    ETree.get_akoma_tag("tacka"): 0,
    ETree.get_akoma_tag("podtacka"): 0,
    ETree.get_akoma_tag("alinea"): 0}


def get_id(tlc_text):
    got = re.search('showAs=".*?"', tlc_text)
    ref = re.search('TLC.*? ', tlc_text)
    return tlc_text[ref.span(0)[0]:ref.span(0)[1] - 1] + ":" + tlc_text[got.span(0)[0] + 8:got.span(0)[1] - 1]


def find_tlc_sim(got_text_new, got_text_org):
    new_refs = re.findall('<TLC.*?>', got_text_new)
    org_refs = re.findall("<TLC.*?>", got_text_org)
    has = 0
    fp = 0
    new_ids = [get_id(el) for el in new_refs if "TLCConcept" not in el]
    org_ids = [get_id(el) for el in org_refs if "TLCConcept" not in el]
    total = len(org_ids)
    for new_values in new_ids:
        if new_values in org_ids:
            has = has + 1
        else:
            fp = fp + 1
    return has / (has + fp), has / total


def find_structure_sim(got_text_new, got_text_org):
    tree_new = ET.fromstring(got_text_new)
    tree_org = ET.fromstring(got_text_org)
    for key in map_found_org:
        found = ETree.get_elements(tree_org, key)
        map_found_org[key] = found
    for key in map_found_new:
        found = ETree.get_elements(tree_new, key)
        map_found_new[key] = found
    has = 0
    fp = 0
    total_org = sum([len(map_found_org[el]) for el in map_found_org])
    for key in map_found_new:
        new_ids = [el.attrib['wId'] for el in map_found_new[key]]
        org_ids = [el.attrib['wId'] for el in map_found_org[key]]
        for new_wid in new_ids:
            if new_wid in org_ids:
                has = has + 1
            else:
                fp = fp + 1
    return has / (has + fp), has / total_org


def find_ref_similarity(text_new, text_org):
    """
    Return precision and recall for references in document annotated and new
    :param text_new: New document made
    :param text_org: Annotated by hand document
    :return: precision,recall
    """
    new_refs = re.findall('<ref .*?>', text_new)
    org_refs = re.findall("<ref .*?>", text_org)
    false_positive = list()
    false_negative = list()
    has = 0
    not_fp = False
    for el in new_refs:
        href = re.findall('href=".*"', el)
        if len(href) == 0:
            false_positive.append(el)
            break
        else:
            href = href[0]
        for check in org_refs:
            if href in check:
                has = has + 1
                not_fp = True
                break
        if not not_fp:
            false_positive.append(el)
        not_fp = False
    # for elem in org_refs:
    #     href = re.findall('href=".*"', elem)
    #     if len(href) == 0:
    #         false_negative.append(elem)
    #         break
    #     else:
    #         href = href[0]
    #     for check in org_refs:
    #         if href in check:
    #             not_fp = True
    #     if not not_fp:
    #         false_negative.append(elem)
    #     not_fp = True
    # fn = len(false_negative)
    fp = len(false_positive)
    return has / (has + fp), has / len(org_refs)


def load_data(source_new, source_annotated):
    try:
        new = open(source_new, mode="r", encoding="UTF-8")
        annotated = open(source_annotated, mode="r", encoding="UTF-8")
    except FileNotFoundError:
        exit(-1)
    new_text = "".join(new.readlines())
    annotated_text = "".join(annotated.readlines())
    new.close()
    annotated.close()
    return new_text, annotated_text


def find_fscore(precision, recall):
    return 2 * ((precision * recall) / (precision + recall))


def call_scores(new_text, annotated_text, which):
    """
    :param new_text: New text
    :param annotated_text: Annotated same files
    :param which: values = 'hir', 'tlc', 'ref', (structure, tlc references,
    :return: f1,precision,recall
    """
    if which == "hir":
        f_pre, f_rec = find_structure_sim(new_text, annotated_text)
    elif which == "ref":
        f_pre, f_rec = find_ref_similarity(new_text, annotated_text)
    elif which == "tlc":
        f_pre, f_rec = find_tlc_sim(new_text, annotated_text)
    else:
        return None
    if f_pre + f_rec == 0:
        f1_score = 0
    else:
        f1_score = find_fscore(f_pre, f_rec)
    return f1_score, f_pre, f_rec


def find_similarity(text, text2):
    similarity = difflib.SequenceMatcher(None, text, text2).ratio()
    return similarity


def print_res(res, text) -> None:
    decs = 2
    output = text + " F1: {:>7} Precision: {:>7} Recall: {:>7}".format(str(round(float(res[0]), decs)),
                                                                       str(round(float(res[1]), decs)),
                                                                       str(round(float(res[2]), decs)))
    print(output)


def average(lst):
    return reduce(lambda a, b: a + b, lst) / len(lst)


def list_mean(scores: list) -> list:
    return [str(average(scores[0])), str(average(scores[1])), str(average(scores[1]))]


if __name__ == "__main__":
    debug = True
    location_annotated = "../data/annotated/"
    location_data = "../data/akoma_result/"
    annotated_files = utilities.sort_file_names(os.listdir(location_annotated))
    list_scores_ref = []
    list_score_sim = []
    list_scores_hir = []
    list_scores_tlc = []
    for i in range(0, len(annotated_files)):
        text_new, text_ann = load_data(location_data + annotated_files[i], location_annotated + annotated_files[i])
        similarity = find_similarity(text_new, text_ann)
        scores_ref = call_scores(text_new, text_ann, "ref")
        scores_hir = call_scores(text_new, text_ann, "hir")
        scores_tlc = call_scores(text_new, text_ann, 'tlc')
        list_scores_tlc.append(scores_tlc)
        list_scores_hir.append(scores_hir)
        list_scores_ref.append(scores_ref)
        list_score_sim.append(similarity)
        print("{:>22}".format(annotated_files[i]))
        if debug:
            print_res(scores_ref, "REF")
            print_res(scores_tlc, "TLC")
            print_res(scores_hir, "HIR")
            print("SIM : " + str(similarity))

    print_res(list_mean(list_scores_ref), "AVG_REF")
    print_res(list_mean(list_scores_tlc), "AVG_TLC")
    print_res(list_mean(list_scores_hir), "AVG_HIR")
    print("SIM_AVG :" + str(statistics.mean(list_score_sim)))
