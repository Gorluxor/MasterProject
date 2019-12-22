import re
from os import path

# s = 'asdf=5;iwantthis123jasd'
# result = re.search('asdf=5;(.*)123jasd', s)
# print(result.group(1))
#
# s = 'Član 1.\n\r iwantthis \n\r Član 2. \n\r 123jasd'
# result = re.search('Član [1-9][0-9]*[.](.*)Član [1-9][0-9]*[.]', s, flags=re.DOTALL)
# print(result.group(1))



basePath = path.dirname(__file__)
with open(path.join(basePath, "..", "data", "test", "1.txt"), "r", encoding="utf-8") as f:
    lines = f.readlines()
listToStr = ' '.join([str(elem) for elem in lines])

allData = []




while re.search('Član [1-9][0-9]*[.]', listToStr):
    result1 = re.search('Član [1-9][0-9]*[.](.*?)Član [1-9][0-9]*[.]', listToStr, flags=re.DOTALL)
    if result1 is None:
        result1 = re.search('Član [1-9][0-9]*[.]', listToStr)
        lastIndex = result1.regs[0][1]
        allData.append(listToStr[lastIndex + 1:])
        listToStr = listToStr[lastIndex:]
    else:
        lastIndex = result1.regs[1][1]
        allData.append(result1.group(1))
        listToStr = listToStr[lastIndex:]
print(allData.__len__())

# def getFileNames(folderData, aktoviFolder):
#     # folderData=data aktoviFolder=aktovi_raw_lat
#     from os import listdir
#     from os.path import isfile, join
#     basePath = path.dirname(__file__)
#     filePath = path.abspath(path.join(basePath, "..", folderData, aktoviFolder))
#     filenames = [f for f in listdir(filePath) if isfile(join(filePath, f))]
#     return filenames, filePath
#
#
# if __name__ == '__main__':
#     filenames, filePath = getFileNames("data", "test")
#     for filename in filenames:
#         check = path.join(filePath, filename);
#         file = open(check, encoding="utf8")
#        info = file.readlines()
