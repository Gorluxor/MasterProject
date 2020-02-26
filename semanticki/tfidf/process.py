from os import path
from connector.connector import checkIfRomanNumeral
from tfidf.most_important_words_tfidf import get_tf_idf_values_document
import re
import tfidf.util
import tfidf.utilities
import tfidf.owl
from convertToLatin import Convert


def inside_important(tfidf, clan_info, iter):
    tf_inside = []
    for tf in tfidf:
        found = re.search(tf[0], clan_info[iter])
        if found is not None:
            tf_inside.append(tf[0])
    return tf_inside

def toLatin(str):
    return "".join([Convert.convert(s) for s in str])


def add_meta_to_act(curr_zakon, meta):
    curr_zakon.local_id = meta.eli
    curr_zakon.title = [toLatin(meta.act_name)]
    curr_zakon.date_of_publication = meta.datum_usvajanja
    curr_zakon.first_date_of_entry_into_force = meta.datum_primene
    curr_zakon.date_of_applicability = meta.datum_stupanja
    curr_zakon.number = [meta.publication['number']]
    curr_zakon.version_date = meta.datum_usvajanja
    curr_zakon.publisher = [toLatin(meta.donosilac)]
    curr_zakon.published_in = [toLatin(meta.izdavac)]


    print(meta)

def generate_owl(folder_path, filenames=None):
    result = get_tf_idf_values_document(folder_path, filenames=filenames, return_just_words=False)

    for el in result:
        f = open(folder_path + "\\" + el[0], "r", encoding="utf-8")
        info = "".join(f.readlines())
        # for q in el[1]:
        #     print(q)
        clans_data = tfidf.util.from_content_to_act_list(info)
        clan_info = tfidf.util.gather_clans(info)
        # Otvori fajl, pronađe strukture, generišu clanovi, dodaju se
        # print(clans_data)
        meta = tfidf.utilities.get_meta("1.html", "data\\allmeta.csv")
        latin_name = toLatin(meta.act_name).replace(' ', '_')
        dis = {}
        curr_zakon = tfidf.owl.add_legal_resource(latin_name)
        add_meta_to_act(curr_zakon, meta)
        i = 0
        for info in clan_info:

            curr_sub = tfidf.owl.add_legal_sub(latin_name[:30] + info.replace(' ', '_'))
            is_about = inside_important(el[1], clans_data, i)
            for new_concept in is_about:
                if new_concept not in dis:
                    dis[new_concept] = tfidf.owl.add_concept(new_concept)

            if is_about.__len__ != 0:
                curr_sub.is_about = [dis[s] for s in is_about]
            curr_sub.is_part_of = [curr_zakon]
            i = i + 1
        tfidf.owl.save()


if __name__ == '__main__':
    base_path = path.dirname(__file__)
    generate_owl(base_path, filenames=["1.txt"])
