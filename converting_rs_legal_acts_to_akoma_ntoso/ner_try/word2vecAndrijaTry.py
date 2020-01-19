# Depricated, Unused
# My trained word2vec model
def trainWrod2vec():
    import pandas as pd
    import numpy as np
    stopWordsFile = open("../preprocessing/stopwords.txt", mode="r+",
                         encoding="utf8")  # nzm sto nije htela funkcija da radi
    stopWords = stopWordsFile.readlines()
    stopWords = list(str(x).replace("\n", "") for x in stopWords)

    colnames = ['word', 'class']
    dataset = pd.read_csv('dataset.csv', delimiter=";", encoding="utf-8", names=colnames)
    X = dataset.drop('class', axis=1)
    y = dataset['class']

    # Cleaing the text
    processed_article = X.values
    for j in range(len(processed_article)):
       processed_article[j] = [processed_article[j][0].lower()]
    all_words = processed_article
    # Removing Stop Words



    from gensim.models import Word2Vec
    word2vec = Word2Vec(all_words, min_count=1, size=5, iter=2, batch_words=20,negative=5)
    return word2vec


def writeToDataset(word2vec):
    file = open("numdataset.csv", mode="w+", encoding="utf8")
    filecsv = open("dataset.csv", mode="r+", encoding="utf8")

    data = filecsv.readlines()
    dataClass = list()

    for i in range(len(data)):
        spliter = data[i].split(";")
        data[i] = word2vec.wv[spliter[0].lower()]
        dataClass.append(spliter[1])

    lines = []
    for i in range(len(data)):
        wordencoded = data[i].tolist()
        line = ""
        for j in range(0,len(wordencoded)):
            line = line + str(wordencoded[j]) + ";"
        line = line + str(dataClass[i])
        lines.append(line)
    file.writelines(lines)
    return True



if __name__ == '__main__':
    word2vec = trainWrod2vec()
    writeToDataset(word2vec)
    vocabulary = word2vec.wv.vocab
    #print(vocabulary)
    v1 = word2vec.wv['Beogradu'.lower()]
    #print(v1)
    sim_words = word2vec.wv.most_similar('Beogradu'.lower())
    print(sim_words)
