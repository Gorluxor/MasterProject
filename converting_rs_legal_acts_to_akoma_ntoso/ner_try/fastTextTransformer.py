# Requires: FastText Model https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.sh.300.bin.gz
# Creates from Word -> Vector , word2vec from fasttext
import fasttext.util

def writeToDataset(fastText):
    file = open("fastnumdataset.csv", mode="w+", encoding="utf8")
    filecsv = open("dataset.csv", mode="r+", encoding="utf8")

    data = filecsv.readlines()
    dataClass = list()

    for i in range(len(data)):
        spliter = data[i].split(";")
        data[i] = fastText.get_word_vector(spliter[0].lower())
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


filepath = "../../cc.sh.300.bin" # Download: https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.sh.300.bin.gz
print("Start Loading")
ft = fasttext.load_model(filepath)
  #fasttext.util.find_nearest_neighbor() #nece da radi
frrr = ft.get_word_vector("Kosovo")
print("Ref encodovoana:")
print(frrr)
print("End Loading")
writeToDataset(ft)

