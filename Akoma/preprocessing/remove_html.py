import io
import re
from os import listdir
from os.path import isfile, join

"""
    Remove all html elements that are not useful to us, and could cause problems
"""


def strip_html(stringo, full_strip: bool = False):
    shorter = 0
    working = 0
    for m in re.finditer('(<(.|\n)*?>)', stringo):
        # retval = "" + stringo
        if not exeption_tag(m.group(), full_strip):
            working = working + 1
            stringo = stringo[:m.start() - shorter] + stringo[m.end() - shorter:]
            shorter += m.end() - m.start()
            if working % 100 == 0 and working > 1000:
                print("Working=" + str(working))

    return stringo


def close_html_token2(stringo, token):
    longer = 0
    for m in re.finditer('<' + token + '(.*?)>', stringo):
        # retval = "" + stringo

        stringo = stringo[:m.end() + longer] + u"</" + token + ">" + stringo[m.end() + longer:]
        longer += len(u"</" + token + ">")
        # stringo = stringo[:m.end()] + u"</" + token + ">" + stringo[m.end():]
    return stringo


def close_html_token(stringo, token):
    m = re.search('<' + token + '(.*?)>', stringo)
    if m:
        return stringo[:m.end()] + u"</" + token + ">" + stringo[m.end():]
    return stringo


def remove_inner_html(stringo, tag):
    m = re.search('<' + tag + '(.*?)>', stringo)
    m2 = re.search('</' + tag + '>', stringo)
    if m and m2:
        return stringo[:m.end()] + u"</" + tag + ">" + stringo[m2.end():]
    return stringo


def make_tag_empty(stringo, tag):
    shorter = 0
    for m in re.finditer('(<p(.|\n)*?>)', stringo):
        # retval = "" + stringo
        # print(shorter)

        stringo = stringo[:m.start() - shorter] + "<p>" + stringo[m.end() - shorter:]
        shorter += m.end() - m.start() - 3

    return stringo


def replace_trash(stringo, trash):
    return stringo.replace(trash, "")


def exeption_tag(substring, full_stip=False):
    if full_stip:
        exepted_tag = []
    else:
        exepted_tag = ["p", "table", "tr", "td", "img", "th"]
    for t in exepted_tag:
        # if re.match("<\/?"+t+"(.|\n)*?>", substring)!= None:
        if re.match("<\/?" + t + "(.|\n)*?>", substring) is not None:
            return True
    return False


def preprocessing(filename, full_strip=False):
    """Remove html tags"""
    try:
        opened = io.open(filename, mode="r", encoding="utf-8")
    except:
        raise Exception("File not exist")

    # f = open(filename, "r")
    stringo = opened.read()
    stringo = remove_inner_html(stringo, "script")
    stringo = remove_inner_html(stringo, "style")
    stringo = strip_html(stringo, full_strip)
    stringo = make_tag_empty(stringo, "p")
    stringo = replace_trash(stringo, "&nbsp;")
    stringo = close_html_token2(stringo, "img")
    return stringo


def getListOfFiles(folderPath):
    onlyfiles = [fer for fer in listdir(folderPath) if isfile(join(folderPath, fer))]
    return onlyfiles


if __name__ == "__main__":
    from os import path

    basePath = path.dirname(__file__)
    filePath = path.abspath(path.join(basePath, "..", "data", "racts"))
    fileOut = path.abspath(path.join(basePath, "..", "data", "raw_racts"))
    filenames = getListOfFiles(filePath)

    for filename in filenames:
        try:
            print("Processing=" + filename)
            fileProcessing = path.join(filePath, filename)
            purified = preprocessing(fileProcessing, full_strip=True)
            f = io.open(path.join(fileOut, filename.replace(".html", ".txt")), mode="w", encoding="utf-8")
            f.write(purified)
            f.close()
        except:
            print("File not found " + str(filename))

    # for i in range(180, 181):
#
#    try:
#      print("File Start" + str(i))
#      purified = preprocessing('../data/aktovi/' + str(i) + '.html')
#      print("File finished" + str(i))
#      f = io.open('../data/aktovi_raw/' + str(i) + '.txt', mode="w", encoding="utf-8")
#      f.write(purified)
#      f.close()
#    except:
#      print("File not found " + str(i) + ".html")
