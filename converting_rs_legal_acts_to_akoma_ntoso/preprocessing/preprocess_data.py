# Iz svakog pravnog akta izvucemo clanove, reci u okviru tih clanove (tokenizacija), lem, stem. Konvertujemo reci u id.
from os import path
import re
from connector import connector
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def getFileNames(folderData, aktoviFolder):
  # folderData=data aktoviFolder=aktovi_raw_lat
  from os import listdir
  from os.path import isfile, join
  basePath = path.dirname(__file__)
  filePath = path.abspath(path.join(basePath, "..", folderData, aktoviFolder))
  filenames = [f for f in listdir(filePath) if isfile(join(filePath, f))]
  return filenames, filePath



if __name__ == '__main__':

  #bow = dict()

  stopWordsFile = open("stopwords.txt", mode="r+", encoding="utf8")
  stopWords = stopWordsFile.readlines()
  stopWords = list(str(x).replace("\n", "") for x in stopWords)
  filenames, filePath = getFileNames("data", "aktovi_raw_lat")
  fileArray = []

  for filename in filenames:
        check = path.join(filePath,filename)
        file = open(check, encoding="utf8")
        allLines = file.readlines()
        actArray = []
        listToStr = ' '.join([str(elem) for elem in allLines]) + "Član 0."
        found = re.finditer("Član [0-9]*\.", listToStr)
        startFrom = 0
        endsTo = 0
        for m in found:
          if startFrom.__eq__(endsTo):
            endsTo = 0
          else:
            endsTo = m.start()
          if endsTo != 0:
            insertString = listToStr[startFrom:endsTo]  # m.group().strip() = what was found in regex
            actArray.append(insertString)
          startFrom = m.end()

        for i in range(0,actArray.__len__()):
            bow = list()
            nesto = actArray[i]
            listTokens = connector.only_lam(nesto)
            for j in range(0,actArray.__len__()):
                if listTokens.__len__() <= j:
                    break
                if listTokens[j] in stopWords or listTokens[j].isdigit():
                    continue
                bow.append(listTokens[j])

            vectorizer = TfidfVectorizer()
            result = vectorizer.fit_transform(list(bow))
            print(bow)
            print(vectorizer.get_feature_names())
            print(result)
            first_vector_tfidfvectorizer = result[0]  # get the first vector out (for the first document)

            df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=vectorizer.get_feature_names(),
                              columns=["tfidf"])  # place tf-idf values in a pandas data frame
            df.sort_values(by=["tfidf"], ascending=False)

            #print('I=' + str(i) + '   ' + actArray[i][1:25].strip())







#        for i in range(0,actArray.__len__()):
#            nesto = actArray[i]
#            listTokens = connector.only_lam(nesto)
#            for j in range(0,actArray.__len__()):
#                if listTokens.__len__() <= j:
#                    break
#                if listTokens[j] in stopWords or listTokens[j].isdigit():
#                    continue
#                value_got = bow.get(listTokens[j])
#                if value_got == None:
#                    bow[listTokens[j]] = 1
#                else:
#                    bow[listTokens[j]] += 1