import io
def getListOfFiles(filePath):

  onlyfiles = [f for f in listdir(filePath) if isfile(join(filePath, f))]
  return onlyfiles


def convert(char):
  switcher = {
    'А': "A",
    'Б': "B",
    'В': "V",
    'Г': "G",
    'Д': "D",
    'Ђ': "Đ",
    'Е': "E",
    'Ж': "Ž",
    'З': "Z",
    'И': "I",
    'Ј': "J",
    'K': "K",
    'Л': "L",
    'Љ': "LJ",
    'М': "M",
    'Н': "N",
    'Њ': "NJ",
    'О': "O",
    'П': "P",
    'Р': "R",
    'С': "S",
    'Т': "T",
    'Ћ': "Ć",
    'У': "U",
    'Ф': "F",
    'Х': "H",
    'Ц': "C",
    'Ч': "Č",
    'Џ': "DŽ",
    'Ш': "Š",
    'а': "a",
    'б': "b",
    'в': "v",
    'г': "g",
    'д': "d",
    'ђ': "đ",
    'е': "e",
    'ж': "ž",
    'з': "z",
    'и': "i",
    'ј': "j",
    'к': "k",
    'л': "l",
    'љ': "lj",
    'м': "m",
    'н': "n",
    'њ': "nj",
    'о': "o",
    'п': "p",
    'р': "r",
    'с': "s",
    'т': "t",
    'ћ': "ć",
    'у': "u",
    'ф': "f",
    'х': "h",
    'ц': "c",
    'ч': "č",
    'џ': "dž",
    'ш': "š",
  }
  func = switcher.get(char, "Invalid")
  if func == "Invalid":
    return char
  return func


if __name__ == '__main__':
  print("Main start")

  from os import listdir
  from os import path
  from os.path import isfile, join

  basePath = path.dirname(__file__)
  filePath = path.abspath(path.join(basePath, "..", "data", "acts"))
  fileOut = path.abspath(path.join(basePath, "..", "data", "racts"))

  filenames = getListOfFiles(filePath)
  extens = ".txt"
  for filename in filenames:
        check = path.join(filePath,filename);
        outputApsolute = path.join(fileOut, filename);
        file = open(check, encoding="utf8")
        outputFile = open(outputApsolute,mode="x",encoding="utf8")
        for line in file:
          for ch in line:
            outputFile.write(convert(ch))