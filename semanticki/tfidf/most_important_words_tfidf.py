"""
 Iz svakog pravnog akta izvucemo clanove, reci u okviru tih clanove (tokenizacija), lem, stem. Konvertujemo reci u id.
"""
from os import path
import re
from connector import connector
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


def get_stop_words():
    stop_words_file = open(r"stopwords.txt", mode="r+", encoding="utf8")
    stop_words = stop_words_file.readlines()
    stop_words = list(str(x).replace("\n", "") for x in stop_words)
    return stop_words


def get_file_names_in_folder(file_path):
    from os import listdir
    from os.path import isfile, join
    filenames = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    return filenames


def get_file_names(folder_data, aktovi_folder):
    # folderData=data aktoviFolder=aktovi_raw_lat
    base_path = path.dirname(__file__)
    file_path = path.abspath(path.join(base_path, "..", folder_data, aktovi_folder))
    filenames = get_file_names_in_folder(file_path)
    return filenames, file_path


def listToString(list_data):
    val = ""
    for i in range(0, len(list_data)):
        val += list_data[i] + " "
    return val


def get_tf_idf_values_document(folder_path, filenames=None, return_just_words=True, threshold=0.09, max_elements=0,
                               with_file_names=True, debug=False):
    """
    Returns most used words in document by TF-IDF, uses RAW Legal documents (without HTML)
    :param folder_path: folder path to files which should be processed
    :param filenames: if specific files want to be processed (list of filenames) to get tfdif values of them
    :param return_just_words:  True return just words, False return value list [ word, probability]
    :param threshold:  threshold for probability to be added in return value
    :param max_elements:  Set return to max elements, ex. want just top 5 most relevant, then set max_elements to 5
    :param with_file_names:  Add filename in list of returned values next to most important words
    :param debug:  Prints values
    :return: Returns most used words in document, Type LIST, Depending on return_just_words, threshold and max_elements
    """
    # break_word = 0
    stop_words_file = open(path.dirname(__file__)+"\\stopwords.txt", mode="r+", encoding="utf8")
    stop_words = stop_words_file.readlines()
    stop_words = list(str(x).replace("\n", "") for x in stop_words)

    if not filenames:
        file_names = get_file_names_in_folder(folder_path)
    else:
        file_names = filenames

    results = []
    for filename in file_names:
        list_clan_for_file = []
        print("Start " + str(filename))
        # break_word = break_word + 1
        check = path.join(folder_path, filename)
        file = open(check, encoding="utf8")
        all_lines = file.readlines()
        act_array = []
        list_to_str = ' '.join([str(elem) for elem in all_lines]) + "Član 0."
        found = re.finditer("Član [0-9]*\.", list_to_str)
        start_from = 0
        ends_to = 0
        for m in found:
            if start_from.__eq__(ends_to):
                ends_to = 0
            else:
                ends_to = m.start()
            if ends_to != 0:
                insert_string = list_to_str[start_from:ends_to]  # m.group().strip() = what was found in regex
                act_array.append(insert_string)
            start_from = m.end()

        c_bl = "#NBLC"
        tokens = connector.only_lam(c_bl.join(act_array))
        tokens = [tok for tok in tokens if tok not in stop_words or tok.isdigit()]
        clans = " ".join(tokens)
        list_clan_for_file = clans.split(c_bl) #Otpimized


        vectorizer = TfidfVectorizer()
        result = vectorizer.fit_transform(list_clan_for_file)
        # print(bow)
        if debug:
            print(vectorizer.get_feature_names())
        # print(result)
        first_vector_tfidfvectorizer = result[0]  # get the first vector out (for the first document)

        df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=vectorizer.get_feature_names(),
                          columns=["tfidf"])  # place tf-idf values in a pandas data frame
        df = df.sort_values(by=["tfidf"], ascending=False)

        list_words = list()
        for row in df.itertuples():
            if row.tfidf <= threshold:
                break
            list_words.append([row.Index, row.tfidf])
            if max_elements != 0:
                if max_elements <= len(list_words):
                    break
        if debug:
            print(df.head())
        if return_just_words:
            list_words = [item[0] for item in list_words]
        if with_file_names:
            results.append([filename, list_words])
        else:
            results.append(list_words)
        if debug:
            print(results[len(results) - 1])
    return results


if __name__ == '__main__':


   #filenames , folderPath = get_file_names("", "aktovi_raw_lat")
   # filenames = filenames[0:10]
    base_path = path.dirname(__file__)
    tf_idf_values = get_tf_idf_values_document(base_path, filenames=["1.txt", "1.txt"], return_just_words=False)
    print(tf_idf_values)
    # print([item[0] for item in tf_idf_values]) #FILES if return file names also
    # print([item[1] for item in tf_idf_values]) #WORDS if return file names also
