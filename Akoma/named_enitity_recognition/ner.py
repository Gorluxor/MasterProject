import pickle
import numpy as np
from itertools import groupby
import spacy

try:
    import Akoma
    from Akoma.named_enitity_recognition.readutils import SentenceGetter, word2features, read_and_prepare_csv, \
        sent2features, sent2labels, sent2tokens
    from Akoma.connector.connector import tokenize_pos
    from Akoma.named_enitity_recognition.readutils import SentenceGetter, word2features, read_and_prepare_csv, \
        sent2features, sent2labels, sent2tokens
    from Akoma.spacy_ner import UseSpacy
    from Akoma.utilites import utilities
except ModuleNotFoundError as sureError:
    try:
        from named_enitity_recognition.readutils import SentenceGetter, word2features, read_and_prepare_csv, \
            sent2features, sent2labels, sent2tokens
        from connector.connector import tokenize_pos
        from named_enitity_recognition.readutils import SentenceGetter, word2features, read_and_prepare_csv, \
            sent2features, sent2labels, sent2tokens
        from spacy_ner import UseSpacy
        from utilities import utilities
    except ModuleNotFoundError as newError:
        if not sureError.name == "Akoma" or not newError.name == "Akoma":
            print(newError)
            print("Error")
            exit(-1)

filename = 'data/ner/modelReldiD.sav'
crf = pickle.load(open(filename, 'rb'))
NER_OBJ = None
# deriv_elements = []
# loc_elements = []
# org_elements = []
# per_elements = []
# misc_elements = []
# date_elements = []


"""
O
B-deriv-per

B-loc
I-loc

B-org
I-org

B-per
I-per

B-misc
I-misc

B-date
I-date
"""


def find_elements(element, res_list, map_of_lists):
    res_list = res_list[0]
    last = None
    continuous = ""
    for x in range(len(res_list)):
        if res_list[x] != 'O':
            tag = res_list[x].split('-')
            if tag[0] == 'B':
                if last is not None:
                    map_of_lists[last].append(continuous)
                last = tag[1]
                continuous = element[x]
            elif last == tag[1]:
                continuous = continuous + ' ' + element[x]
            else:
                last = None
    if continuous != "":
        if last is not None:
            map_of_lists[last].append(continuous)


def sort_got_data(doc, map_of_lists, keys) -> None:
    continuous = ""
    last = None
    old = None
    for index, token in enumerate(doc):
        if token.ent_type_ == "":
            tag = ["O", "O"]
        else:
            tag = token.ent_type_.split("-")
        if "B" == tag[0]:
            if len(doc) == index + 1:
                map_of_lists[tag[1]].append(continuous)
                continuous = ""
                continue
            if last is None and old is not None:
                map_of_lists[old].append(continuous)
                continuous = ""
            last = tag[1]
            continuous = continuous + " " + token.text
            continuous = continuous.strip()
        elif last == tag[1]:
            continuous = continuous + ' ' + token.text
            continuous = continuous.strip()
        else:
            if last is not None:
                old = last
            last = None

    for key in keys:
        map_of_lists[key] = list(np.unique(map_of_lists[key]))
        # print("How are we here? Text: " + token.text + " LABEL" + token.label_)


def do_spacy_ner(sentences, model="xx_ent_wiki_sm", custom=True):
    global NER_OBJ
    if NER_OBJ is None:
        if custom:
            NER_OBJ = spacy.load(utilities.get_root_dir() + "/data/spacy/model")
        else:
            NER_OBJ = spacy.load(model)
    text = ".\n".join(sentences)
    doc2 = NER_OBJ(text)
    ents = doc2.ents
    new_ents = [[el.label_, el.text] for el in ents]
    keys = (np.unique(
        [str.lower(el[0]).replace("b-", "").replace("i-", "") for el in new_ents]))  # ["PER","ORG","MISC","LOC"]
    map_of_lists = dict()
    for key in keys:
        map_of_lists[key] = []
    if not custom:
        for entries in new_ents:
            map_of_lists[str.lower(entries[0])].append(entries[1])
        for key in keys:
            map_of_lists[key] = list(np.unique(map_of_lists[key]))
    else:
        sort_got_data(doc2, map_of_lists, keys)
    return map_of_lists


def do_ner_on_sentences(sentences):
    map_of_lists = {'deriv': [], 'loc': [], 'org': [], 'per': [],
                    'misc': [], 'date': []}

    merged_sentences = "`".join(sentences)
    w = tokenize_pos(merged_sentences)

    df = [(x, y) for x, y, z in w]
    separated_list = [list(group) for key, group in groupby(df, key=lambda t: t[0] != '`') if key]

    for tw in separated_list:
        el = [x for x, y in tw]
        y_pred = crf.predict([sent2features(tw)])
        find_elements(el, y_pred, map_of_lists)

    for key in map_of_lists:
        map_of_lists[key] = list(np.unique(map_of_lists[key]))

    return map_of_lists
