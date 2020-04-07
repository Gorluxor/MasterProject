import re
from termcolor import colored
from Akoma.utilities.utilities import *
from Akoma.utilities.ETree import *

def prettify(root):
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(ET.tostring(root, encoding='UTF-8', method="xml").decode())
    return dom.toprettyxml()

def ranges(nums):
    nums = sorted(set(nums))
    gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
    edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
    return list(zip(edges, edges))

#'((члан|став|тачка|тачке|podtaчка|алинеја).? [0-9]+(\\.)?,?\\s?)+(\\s овог \\s\w*)?'


# akn/<država>/act/<godina publikovanja u formatu YYYY-MM-DD ili samo YYYY>/<broj akta u godini ili ako se ne zna "nn">/srb@/
# <!main, !imedoc.akn ili !schedule_1.pdf (extenzija manifestacije)>/<chp_4 je chapter 4>
# art_3__para_5__point_c

pattern = 'wId="(\w+)-?(\w+)?-?(\w+)?"'

further = "(\\.?\\s?,?\\s?)"
nabrajanje = '(члан.?\\s[0-9]+)' + further + '(став.?\\s[0-9]+)?' + further + '((тачка|тачке).?\\s[0-9]+)?'


def add_refs1(stringo, cnt, this_id):
    longer = 0
    for m in re.finditer(nabrajanje + '\\b(овог)?', stringo):
        ending = get_ending(m, stringo)

        open = u"<ref " + "wId=\"ref" + str(cnt) + "\" href=\"akn" + this_id + "/!main~" + ending + "\" >"

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

        open = u"<ref " + "wId=\"ref" + str(cnt) + "\" href=\"akn" + this_id + "/!main~" + ending + "\" >"

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
    regexBrojSlovo = '[0-9]+\w'
    matches = re.findall(regexBrojSlovo, stringToScan)
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
        if len(matches) != 0:
            pass
        else:
            matches = re.findall(regexBroj, stringToScan)
            matches = [int(i) for i in matches]
            matches.sort()
            edges = ranges(matches)
            position = 0;
            listOfIndex = []
            pomList = []
            for pom in re.finditer(regexBroj, stringToScan):
                if int(pom.group()) == edges[position][0] and edges[position][0] == edges[position][1]:
                    listOfIndex.append([pom.regs[0],pom.regs[0]])
                    position = position + 1
                elif int(pom.group()) == edges[position][0]:
                    pomList = []
                    pomList.append(pom.regs[0])
                elif int(pom.group()) == edges[position][1]:
                    pomList.append(pom.regs[0])
                    listOfIndex.append(pomList)
                    position = position + 1

        retval = "art_" + str(matches[0]) + "->art_" + str(matches[len(matches) - 1]) + "_"
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
            open = u"<ref " + "wId=\"ref" + str(cnt) + "\" href=\"akn/rs/act/" + m1.group(2) + "/" + m1.group(
                1) + "/srp@\">"
        else:
            open = u"<ref " + "wId=\"ref" + str(cnt) + "\">"
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


def add_refs3(stringo, cnt, this_id, clan_id):
    longer = 0
    for m in re.finditer(nabrajanje3 + '\\b(овог)?', stringo):
        if not re.search(nabrajanje + '\\b(овог)?', stringo[m.regs[0][0] + longer - 40: m.regs[0][1] + longer]):
            ending = get_ending2(m, clan_id)

            open = u"<ref " + "wId=\"ref" + str(cnt) + "\" href=\"akn" + this_id + "/!main~" + ending + "\" >"

            stringo = stringo[:m.start() + longer] + open + stringo[m.start() + longer:]
            longer += len(open)

            stringo = stringo[:m.end() + longer] + u"</ref>" + stringo[m.end() + longer:]
            longer += len(u"</ref>")
            # print(m.start(), m.end(), m.group(0))
            cnt += 1
            # stringo = stringo[:m.end()] + u"</" + token + ">" + stringo[m.end():]
    return stringo, cnt


def get_ending2(m, clan_id):
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
    pom_string = ""
    try:
        pomLista = clan_id.split('-')
        pom_string = "act_" + pomLista[len(pomLista) - 1] + "__"
    except AttributeError as e1:
        text_error = ">>Error in NER>pattern_recoginition.py, Nina <3 pogledaj me, stavi break point ovde 145 linija"
        print(colored(text_error, 'red'))  # TODO NINA FIX
        print(e1)
    retval = pom_string + retval
    return retval[:-1]


def add_refs(stablo, stringo, this_id):
    cnt = 0


    listaClanova = get_elements(stablo, 'article', namespace="")
    listaObradjenihParagrafa = []

    for el_clan in listaClanova:  # Primer pristupa svakom članu
        clan_id = el_clan.attrib['wId']
        for el_stav in el_clan.iter('paragraph'):
            if el_stav.attrib['wId'] not in listaObradjenihParagrafa:
                for el_content_p_tag in el_stav.iter('p'):
                    got_parent = get_parent_nth_parent(el_content_p_tag, 2)  # Pribavljanje roditelja
                    stav_text = el_content_p_tag.text
                    stringo, cnt = add_refs1(stav_text, cnt, this_id)
                    stringo, cnt = add_refsCl(stringo, cnt, this_id)
                    # print("PHASE 2")
                    stringo, cnt = add_refs2(stringo, cnt)
                    stringo, cnt = add_refs3(stringo, cnt, this_id, clan_id)
                    el_content_p_tag.text = stringo
                    # print(prettify(stablo))
                # print(el_stav.tag)
                listaObradjenihParagrafa.append(el_stav.attrib['wId'])
    # print(el_clan.tag, el_clan.attrib)

    # stringo, cnt = add_refs1(stringo, cnt, this_id)
    # stringo, cnt = add_refsCl(stringo, cnt, this_id)
    # # print("PHASE 2")
    # stringo, cnt = add_refs2(stringo, cnt)
    # stringo, cnt = add_refs3(stringo, cnt, this_id)
    return stringo
