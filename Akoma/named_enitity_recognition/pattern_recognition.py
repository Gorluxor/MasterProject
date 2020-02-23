import re

#'((члан|став|тачка|тачке|podtaчка|алинеја).? [0-9]+(\\.)?,?\\s?)+(\\s овог \\s\w*)?'
further = "(\\.?\\s?,?\\s?)"
nabrajanje = '(члан.?\\s[0-9]+)'+further+'(став.?\\s[0-9]+)?'+further+'((тачка|тачке).?\\s[0-9]+)?'
def add_refs1(stringo, cnt, this_id):
    longer = 0
    for m in re.finditer(nabrajanje +'\\b(овог)?', stringo):
        ending = get_ending(m)

        open = u"<ref " + "id=\"ref" + str(cnt) + "\" href=\""+this_id+ending+"\" >"

        stringo = stringo[:m.start() + longer] + u"<ref>" + stringo[m.start() + longer:]
        longer += len(u"<ref>")

        stringo = stringo[:m.end() + longer]+ u"</ref>" +stringo[m.end() + longer:]
        longer += len(u"</ref>")
       # print(m.start(), m.end(), m.group(0))
        cnt += 1
        #stringo = stringo[:m.end()] + u"</" + token + ">" + stringo[m.end():]
    return stringo, cnt

def get_ending(m):
    retval = ""
    if m.group(1):
        m1 = re.search("([0-9]+)", m.group(1))
        if m1:
            retval += "clan"+m1.group(0)+"-"
    if m.group(3):
        m2 = re.search("([0-9]+)", m.group(3))
        if m2:
            retval += "stav" + m2.group(0)+"-"
    if m.group(5):
        m3 = re.search("([0-9]+)", m.group(5))
        if m3:
            retval += "tac" + m3.group(0)+"-"
   # print(retval[:-1])
    return retval[:-1]

nabrajanje2 = '(члан.?\\s[0-9]+)?'+further+'(став.?\\s[0-9]+)?'+further+'((тачка|тачке).?\\s[0-9]+)?'
def add_refs2(stringo, cnt):
    longer = 0
    for m in re.finditer(nabrajanje2 + '(Службени.*?)([0-9]+/[0-9]+(,\s)?)+', stringo):
        # retval = "" + stringo
        m1 = re.search("([0-9]+)/([0-9]+)", m.group(0))
        if m1:
            open =  u"<ref "+"id=\"ref"+str(cnt)+"\" href=\"/rs/act/"+m1.group(2)+"/"+m1.group(1)+"/srp@\">"
        else:
            open = u"<ref "+"id=\"ref"+str(cnt)+"\">"
        stringo = stringo[:m.start() + longer] + open + stringo[m.start() + longer:]
        longer += len(open)

        stringo = stringo[:m.end() + longer]+ u"</ref>" +stringo[m.end() + longer:]
        longer += len(u"</ref>")
        #print(m.start(), m.end(), m.group(0))
        cnt+=1
        #stringo = stringo[:m.end()] + u"</" + token + ">" + stringo[m.end():]
    return stringo, cnt

def add_refs(stringo, this_id):
    cnt = 0
    stringo, cnt = add_refs1(stringo, cnt, this_id)
    #print("PHASE 2")
    stringo, cnt = add_refs2(stringo, cnt)
    return stringo