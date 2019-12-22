from os import path

fileToClean = "linkovi4.txt"

basePath = path.dirname(__file__)
filePath = path.abspath(path.join(basePath, "..", "data", "linkovi"))
f = open(path.join(filePath, fileToClean),mode="r", encoding="utf8")
lines = f.readlines()
f.close()
fileOtherName = fileToClean.split(".")[0] + "_doc" + ".txt"
fother = open(path.join(filePath, fileOtherName), "w", encoding="utf8")

f = open(path.join(filePath, fileToClean),mode="w", encoding="utf8")
for line in lines:
  if not line.strip("\n").__contains__("viewdoc"):
    f.write(line)
  else:
    fother.write(line)

f.close()