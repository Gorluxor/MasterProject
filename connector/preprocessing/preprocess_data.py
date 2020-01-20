# Iz svakog pravnog akta izvucemo clanove, reci u okviru tih clanove (tokenizacija), lem, stem. Konvertujemo reci u id.
from os import path
import re


def getFileNames(folderData, aktoviFolder):
  # folderData=data aktoviFolder=aktovi_raw_lat
  from os import listdir
  from os.path import isfile, join
  basePath = path.dirname(__file__)
  filePath = path.abspath(path.join(basePath, "..", folderData, aktoviFolder))
  filenames = [f for f in listdir(filePath) if isfile(join(filePath, f))]
  return filenames, filePath


if __name__ == '__main__':

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

            actArray[i]
            print('I=' + str(i) + '   ' + actArray[i][1:25].strip())
        fileArray.append(actArray)





