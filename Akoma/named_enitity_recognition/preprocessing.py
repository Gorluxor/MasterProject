import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import io


def read_data(path):
    f = io.open(path, mode="r", encoding="utf-8")

    #f = open("../data/NER/labeled/labled_data1.json", "r")
    stringo = f.read()
    d = json.loads(stringo)
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    reseult = []
    for p in d["annotations_and_examples"]:
        tokens = nltk.word_tokenize(p["content"])
        tagged = nltk.pos_tag(tokens)
        print(tagged)


if __name__ == "__main__":
    read_data("../data/NER/labeled/labled_data1.json")





