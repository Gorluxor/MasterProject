import io
import re
"""
    Remove all html elements that are not useful to us, and could cause problems
"""
def strip_html(stringo):
    shorter = 0
    for m in re.finditer('(<(.|\n)*?>)', stringo):
        #retval = "" + stringo
        stringo = stringo[:m.start()-shorter] + stringo[m.end()-shorter:]
        shorter +=m.end()-m.start()

    return stringo
def close_html_token2(stringo, token):
    longer = 0
    for m in re.finditer('<'+token+'(.*?)>', stringo):
        # retval = "" + stringo

        stringo = stringo[:m.end() + longer]+ u"</" + token + ">" +stringo[m.end() + longer:]
        longer += len(u"</" + token + ">")
        #stringo = stringo[:m.end()] + u"</" + token + ">" + stringo[m.end():]
    return stringo

def close_html_token(stringo, token):
    m = re.search('<'+token+'(.*?)>', stringo)
    if m:
        return stringo[:m.end()] + u"</"+token+">" + stringo[m.end():]
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
        #retval = "" + stringo
        #print(shorter)

        stringo = stringo[:m.start()-shorter] + "<p>" + stringo[m.end()-shorter:]
        shorter +=m.end()-m.start() - 3

    return stringo

def replace_trash(stringo, trash):
    return stringo.replace(trash, "")

def exeption_tag(substring):
    exepted_tag = ["p","table", "tbody", "tr", "td", "img", "th"]
    for t in exepted_tag:
        if(re.match("<\/?"+t+"(.|\n)*?>", substring)!= None):
            return True
    return False


def preprocessing(filename):
    f = io.open(filename, mode="r", encoding="utf-8")
    #f = open(filename, "r")
    stringo = f.read()
    stringo = remove_inner_html(stringo, "script")
    stringo = remove_inner_html(stringo, "style")
    stringo = strip_html(stringo)
    stringo = make_tag_empty(stringo, "p")
    stringo = replace_trash(stringo, "&nbsp;")
    stringo = close_html_token2(stringo, "img")
    return stringo


if __name__ == "__main__":
    for i in range(1, 2425):
        print(i)
        try:
            stringo = preprocessing('../data/aktovi/' +str(i)+'.html')
            f = io.open('../data/aktovi_raw/' +str(i)+'.txt', mode="w", encoding="utf-8")
            f.write(stringo)
            f.close()
        except FileNotFoundError:
            continue