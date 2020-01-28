# Requires: FastText Model https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.sh.300.bin.gz
# Creates from Word -> Vector , word2vec from fasttext
import fasttext.util

def writeToDataset(fastText):
    delimiter = "\t"
    file = open("datasetReldiSw2v.csv", mode="w+", encoding="utf8")
    filecsv = open("datasetReldiS.csv", mode="r+", encoding="utf8")

    data = filecsv.readlines()
    dataClass = list()
    dataSequence = list()
    for i in range(0,len(data)):
        if i==0:
            continue
        spliter = data[i].split(delimiter)
        vector = fastText.get_word_vector(spliter[1].lower())
        data[i] = vector
        dataClass.append(spliter[3] + delimiter + spliter[4])
        dataSequence.append(spliter[0])

    colnames = "Sequence #" + delimiter
    for i in range(0, 300):
        colnames = colnames + "word" + str(i + 1) + delimiter
    colnames = colnames + "PosTag"

    lines = []
    for i in range(len(data)):
        if i == 0:
            lines.append(colnames + "\n")
            continue
        wordencoded = data[i].tolist()
        line = ""
        line = str(dataSequence[i-1]) + delimiter
        for j in range(0 , len(wordencoded)):
            line = line + str(wordencoded[j]) + delimiter
        line = line + str(dataClass[i-1])
        lines.append(line)
    file.writelines(lines)
    return True


filepath = "../../cc.sh.300.bin" # Download: https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.sh.300.bin.gz
print("Start Loading")
ft = fasttext.load_model(filepath)
  #fasttext.util.find_nearest_neighbor() #nece da radi

frrr = ft.get_word_vector("Kosovo")
print("Ref encodovoana:")
print(frrr)
print("End Loading")
writeToDataset(ft)

