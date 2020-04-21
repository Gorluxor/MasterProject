import difflib
import os
import re
import statistics

try:
    from Akoma.utilities import utilities
    from Akoma.convertToLatin.Convert import top
except ModuleNotFoundError:
    try:
        from utilities import utilities
        from convertToLatin.Convert import top
    except ModuleNotFoundError:
        print("Import error")


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
    for elem in org_refs:
        href = re.findall('href=".*"', elem)
        if len(href) == 0:
            false_negative.append(elem)
            break
        else:
            href = href[0]
        for check in org_refs:
            if href in check:
                not_fp = True
        if not not_fp:
            false_negative.append(elem)
        not_fp = True
    fn = len(false_negative)
    fp = len(false_positive)
    return has / has + fp, has / len(org_refs)


def find_file_f1score_ref_similarity(source_new, source_annotated):
    new = open(source_new, mode="r", encoding="UTF-8")
    annotated = open(source_annotated, mode="r", encoding="UTF-8")
    new_text = "".join(new.readlines())
    annotated_text = "".join(annotated.readlines())
    sim = find_similarity(new_text, annotated_text)
    f_prec, f_rec = find_ref_similarity(new_text, annotated_text)
    f1_score = 2 * ((f_prec * f_rec) / (f_prec + f_rec))
    return top(f1_score), sim, f_prec,f_rec


def find_similarity(text, text2):
    similarity = difflib.SequenceMatcher(None, text, text2).ratio()
    return similarity


if __name__ == "__main__":
    location_annotated = "../data/annotated/"
    location_data = "../data/akoma_result/"
    annotated_files = utilities.sort_file_names(os.listdir(location_annotated))
    f1_list = []
    sim_list = []
    for i in range(0, len(annotated_files)):
        f1, similarity, prec,rec = find_file_f1score_ref_similarity(location_data + annotated_files[i],location_annotated + annotated_files[i])
        f1_list.append(f1)
        sim_list.append(similarity)
        print(annotated_files[i])
        # print("F1=" + str(f1))
        # print("SIM=" + str(similarity))
    print("F1_AVG :" + str(statistics.mean(f1_list)))
    print("SIM_AVG :" + str(statistics.mean(sim_list)))
