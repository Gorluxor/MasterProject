import re
from termcolor import colored

# '((члан|став|тачка|тачке|podtaчка|алинеја).? [0-9]+(\\.)?,?\\s?)+(\\s овог \\s\w*)?'

# akn/<država>/act/<godina publikovanja u formatu YYYY-MM-DD ili samo YYYY>/<broj akta u godini ili ako se ne zna "nn">/srb@/
# <!main, !imedoc.akn ili !schedule_1.pdf (extenzija manifestacije)>/<chp_4 je chapter 4>
# art_3__para_5__point_c

pattern = 'id="(\w+)-?(\w+)?-?(\w+)?"'

further = "(\\.?\\s?,?\\s?)"
nabrajanje = '(члан.?\\s[0-9]+)' + further + '(став.?\\s[0-9]+)?' + further + '((тачка|тачке).?\\s[0-9]+)?'


def add_refs1(stringo, cnt, this_id):
    longer = 0
    for m in re.finditer(nabrajanje + '\\b(овог)?', stringo):
        ending = get_ending(m, stringo)

        open = u"<ref " + "id=\"ref" + str(cnt) + "\" href=\"akn" + this_id + "/!main~" + ending + "\" >"

        stringo = stringo[:m.start() + longer] + open + stringo[m.start() + longer:]
        longer += len(open)

        stringo = stringo[:m.end() + longer] + u"</ref>" + stringo[m.end() + longer:]
        longer += len(u"</ref>")
        # print(m.start(), m.end(), m.group(0))
        cnt += 1
        # stringo = stringo[:m.end()] + u"</" + token + ">" + stringo[m.end():]
    return stringo, cnt


nabrajanjeCl = '(чл. [0-9]+\.?)(((,)|(.? и))( [0-9]+\.?))*'


def add_refsCl(stringo, cnt, this_id):
    longer = 0
    for m in re.finditer(nabrajanjeCl + '.\\b(овог)?', stringo):
        ending = get_ending(m, stringo[m.regs[0][0] + longer:m.regs[0][1] + longer], True)

        open = u"<ref " + "id=\"ref" + str(cnt) + "\" href=\"akn" + this_id + "/!main~" + ending + "\" >"

        stringo = stringo[:m.start() + longer] + open + stringo[m.start() + longer:]
        longer += len(open)

        stringo = stringo[:m.end() + longer] + u"</ref>" + stringo[m.end() + longer:]
        longer += len(u"</ref>")
        # print(m.start(), m.end(), m.group(0))
        cnt += 1
        # stringo = stringo[:m.end()] + u"</" + token + ">" + stringo[m.end():]
    return stringo, cnt


def get_ending(m, stringToScan, cl=False):
    regexBroj = '[0-9]+'
    matches = re.findall(regexBroj, stringToScan)
    retval = ""
    if not cl:
        if m.group(1):
            m1 = re.search("([0-9]+)", m.group(1))
            if m1:
                retval += "art_" + m1.group(0) + "_"
        if m.group(3):
            m2 = re.search("([0-9]+)", m.group(3))
            if m2:
                retval += "_para_" + m2.group(0) + "_"
        if m.group(5):
            m3 = re.search("([0-9]+)", m.group(5))
            if m3:
                retval += "_point_" + m3.group(0) + "_"
    # pom_place = re.search(retval[:-1], stringo)
    # pom_string = stringo[pom_place.regs[0][0]-5: pom_place.regs[0][0]]
    # retval = pom_string + retval
    else:
        matches.sort()
        retval = "art_" + matches[0] + "->art_" + matches[len(matches) - 1] + "_"
        # for match in matches:
        #     retval = retval + "art_" + match + "__"
    return retval[:-1]


nabrajanje2 = '(члан.?\\s[0-9]+)?' + further + '(став.?\\s[0-9]+)?' + further + '((тачка|тачке).?\\s[0-9]+)?'


def add_refs2(stringo, cnt):
    longer = 0
    for m in re.finditer(nabrajanje2 + '(Службени.*?)([0-9]+/[0-9]+(,\s)?)+', stringo):
        # retval = "" + stringo
        m1 = re.search("([0-9]+)/([0-9]+)", m.group(0))
        if m1:
            open = u"<ref " + "id=\"ref" + str(cnt) + "\" href=\"akn/rs/act/" + m1.group(2) + "/" + m1.group(
                1) + "/srp@\">"
        else:
            open = u"<ref " + "id=\"ref" + str(cnt) + "\">"
        stringo = stringo[:m.start() + longer] + open + stringo[m.start() + longer:]
        longer += len(open)

        stringo = stringo[:m.end() + longer] + u"</ref>" + stringo[m.end() + longer:]
        longer += len(u"</ref>")
        # print(m.start(), m.end(), m.group(0))
        cnt += 1
        # stringo = stringo[:m.end()] + u"</" + token + ">" + stringo[m.end():]
    return stringo, cnt


# ^(?!.*(red|green|blue)).*engine
nabrajanje3 = '(став.?\\s[0-9]+)' + further + '((тачка|тачке).?\\s[0-9]+)?'


def add_refs3(stringo, cnt, this_id):
    longer = 0
    for m in re.finditer(nabrajanje3 + '\\b(овог)?', stringo):
        if not re.search(nabrajanje + '\\b(овог)?', stringo[m.regs[0][0] + longer - 40: m.regs[0][1] + longer]):
            ending = get_ending2(m, stringo, longer)

            open = u"<ref " + "id=\"ref" + str(cnt) + "\" href=\"akn" + this_id + "/!main~" + ending + "\" >"

            stringo = stringo[:m.start() + longer] + open + stringo[m.start() + longer:]
            longer += len(open)

            stringo = stringo[:m.end() + longer] + u"</ref>" + stringo[m.end() + longer:]
            longer += len(u"</ref>")
            # print(m.start(), m.end(), m.group(0))
            cnt += 1
            # stringo = stringo[:m.end()] + u"</" + token + ">" + stringo[m.end():]
    return stringo, cnt


def get_ending2(m, stringo, longer):
    retval = ""
    if m.group(1):
        m2 = re.search("([0-9]+)", m.group(1))
        if m2:
            retval += "para_" + m2.group(0) + "_"
    if m.group(3):
        m3 = re.search("([0-9]+)", m.group(3))
        if m3:
            retval += "_point_" + m3.group(0) + "_"
    # print(retval[:-1])
    pom_place = re.search(pattern, stringo[m.regs[0][0] + longer - 250: m.regs[0][1] + longer + 20])
    pom_string = ""
    try:
        pom_string = "act_" + pom_place.string[pom_place.regs[2][0]:pom_place.regs[2][1]][4:] + "__"
    except AttributeError as e1:
        text_error = ">>Error in NER>pattern_recoginition.py, Nina <3 pogledaj me, stavi break point ovde 145 linija"
        print(colored(text_error, 'red'))  # TODO NINA FIX
        print(e1)
    retval = pom_string + retval
    return retval[:-1]


def add_refs(stringo, this_id):
    cnt = 0
    stringo, cnt = add_refs1(stringo, cnt, this_id)
    stringo, cnt = add_refsCl(stringo, cnt, this_id)
    # print("PHASE 2")
    stringo, cnt = add_refs2(stringo, cnt)
    stringo, cnt = add_refs3(stringo, cnt, this_id)
    return stringo
