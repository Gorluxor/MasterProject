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

further = "(\\.?\\s?,?\\s?)"
azbuka_pattern = '[а|б|в|г|д|ђ|е|ж|з|и|ј|к|л|љ|м|н|њ|о|п|р|с|т|ћ|у|ф|х|ц|ч|џ|ш]?'
regexBroj = '[0-9]+'
regexBrojSlovo = '[0-9]+[а|б|в|г|д|ђ|е|ж|з|и|ј|к|л|љ|м|н|њ|о|п|р|с|т|ћ|у|ф|х|ц|ч|џ|ш]'
nabrajanje = '(члан.?\\s[0-9]+)' + further + '(став.?\\s[0-9]+)?' + further + '((тачка|тачке).?\\s[0-9]+)?'
nabrajanjeCl = '(чл. [0-9]+\.?)(((,)|(.? и))( [0-9]+\.?))*'
nabrajanjeClDoCl = '(чл. [0-9]+\.)( до )((чл. )?[0-9]+(\.|,))'
nabrajanjeClCrtaClan = '(чл. [0-9]+' + azbuka_pattern + ')(–|-)((чл. )?[0-9]+' + azbuka_pattern + ')'
nabrajanje2 = '(члан.?\\s[0-9]+)?' + further + '(став.?\\s[0-9]+)?' + further + '((тачка|тачке).?\\s[0-9]+)?'
nabrajanje3 = '(став.?\\s[0-9]+)' + further + '((тачка|тачке).?\\s[0-9]+)?'

def make_reference(cnt, this_id, ending, stringo, m, longer):
    open = u"<ref " + "wId=\"ref" + str(cnt) + "\" href=\"akn" + this_id + "/!main~" + ending + "\" >"

    stringo = stringo[:m.start() + longer] + open + stringo[m.start() + longer:]
    longer += len(open)

    stringo = stringo[:m.end() + longer] + u"</ref>" + stringo[m.end() + longer:]
    longer += len(u"</ref>")

    cnt += 1
    return stringo, longer, cnt

def make_reference_for_counting(cnt, this_id, start, end, ending, stringo, longer):
    open = u"<ref " + "wId=\"ref" + str(cnt) + "\" href=\"akn" + this_id + "/!main~" + ending + "\" >"

    stringo = stringo[:start + longer] + open + stringo[start + longer:]
    longer += len(open)

    stringo = stringo[:end + longer] + u"</ref>" + stringo[end + longer:]
    longer += len(u"</ref>")

    cnt += 1
    return stringo, longer, cnt

def find_range_list(stringToScan, edges):
    position = 0;
    listOfIndex = []
    pomList = []
    for pom in re.finditer(regexBroj, stringToScan):
        if int(pom.group()) == edges[position][0] and edges[position][0] == edges[position][1]:
            listOfIndex.append([pom.regs[0], pom.regs[0]])
            position = position + 1
        elif int(pom.group()) == edges[position][0]:
            pomList = []
            pomList.append(pom.regs[0])
        elif int(pom.group()) == edges[position][1]:
            pomList.append(pom.regs[0])
            listOfIndex.append(pomList)
            position = position + 1
    return listOfIndex

def get_reference_for_clan_nabrajanje(m, stringo):
    retval = ""
    if m.group(1):
        m1 = re.search("([0-9]+" + azbuka_pattern + ")", m.group(1))
        if m1:
            retval += "art_" + m1.group(0) + "->"
    if m.group(3):
        m2 = re.search("([0-9]+)" + azbuka_pattern, m.group(3))
        if m2:
            retval += "art_" + m2.group(0) + "_"
    return retval[:-1]

def get_reference_for_clan_stav_tacka(m):
    retval = ""
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
    return retval

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
    pomLista = clan_id.split('-')
    pomBroj = re.findall(regexBroj, pomLista[len(pomLista)-1])
    pom_string = "act_" + pomBroj[0] + "__"
    retval = pom_string + retval
    return retval[:-1]

def get_ending(m, stringToScan, cnt, this_id, cl=False):
    matches = re.findall(regexBrojSlovo, stringToScan)
    retval = ""
    if not cl:
        retval = get_reference_for_clan_stav_tacka(m)
    else:
        if len(matches) != 0:
            retval = "art_" + str(matches[0]) + "->art_" + str(matches[len(matches) - 1]) + "_"
        else:
            matches = re.findall(regexBroj, stringToScan)
            if len(matches) == 1:
                retval = "art_" + str(matches[0]) + "_"
            else:
                matches = [int(i) for i in matches]
                matches.sort()
                edges = ranges(matches)

                if len(edges) == 1:
                    retval = "art_" + str(matches[0]) + "->art_" + str(matches[len(matches) - 1]) + "_"
                else:
                    range_list_for = find_range_list(stringToScan, edges)
                    for edge in edges:
                        if edge[0] == edge[1]:
                            reference = make_reference_for_counting()
                    retval = "art_" + str(matches[0]) + "_"
    return retval[:-1]

def add_refs1(stringo, cnt, this_id):
    longer = 0
    for m in re.finditer(nabrajanje + '\\b(овог)?', stringo):
        ending = get_ending(m, stringo)

        stringo, longer, cnt = make_reference(cnt, this_id, ending, stringo, m, longer)
    return stringo, cnt

def add_refsCl(stringo, cnt, this_id):
    longer = 0
    for m in re.finditer(nabrajanjeCl + '.\\b(овог)?', stringo):
        findPattern = re.match(nabrajanjeClDoCl, stringo[m.regs[0][0]:m.regs[0][0] + 20])
        foundPattern = re.match(nabrajanjeClCrtaClan, stringo[m.regs[0][0]:m.regs[0][0] + 20])
        if findPattern:
            firstIndex = findPattern.regs[0][0] + m.regs[0][0] + longer
            lastIndex = findPattern.regs[0][1] + m.regs[0][0] + longer
            ending = get_reference_for_clan_nabrajanje(findPattern, stringo[firstIndex:lastIndex])
        elif foundPattern:
            firstIndex = foundPattern.regs[0][0] + m.regs[0][0] + longer
            lastIndex = foundPattern.regs[0][1] + m.regs[0][1] + longer
            ending = get_reference_for_clan_nabrajanje(foundPattern, stringo[firstIndex:lastIndex])
        else:
            ending = get_ending(m, stringo[m.regs[0][0] + longer:m.regs[0][1] + longer], cnt, this_id, True)

        stringo, longer, cnt = make_reference(cnt, this_id, ending, stringo, m, longer)
    return stringo, cnt

def add_refs2(stringo, cnt):
    longer = 0
    for m in re.finditer(nabrajanje2 + '(Службени.*?)([0-9]+/[0-9]+(,\s)?)+', stringo):
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
        cnt += 1
    return stringo, cnt

def add_refs3(stringo, cnt, this_id, clan_id):
    longer = 0
    for m in re.finditer(nabrajanje3 + '\\b(овог)?', stringo):
        if not re.search(nabrajanje + '\\b(овог)?', stringo[m.regs[0][0] + longer - 40: m.regs[0][1] + longer]):
            ending = get_ending2(m, clan_id)

            stringo, longer, cnt = make_reference(cnt, this_id, ending, stringo, m, longer)
            # stringo = stringo[:m.end()] + u"</" + token + ">" + stringo[m.end():]
    return stringo, cnt

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
                    stringoRet, cnt = add_refs1(stav_text, cnt, this_id)
                    stringoRet, cnt = add_refsCl(stringoRet, cnt, this_id)
                    # print("PHASE 2")
                    stringoRet, cnt = add_refs2(stringoRet, cnt)
                    stringoRet, cnt = add_refs3(stringoRet, cnt, this_id, clan_id)
                    el_content_p_tag.text = stringoRet
                    # print(prettify(stablo))
                # print(el_stav.tag)
                listaObradjenihParagrafa.append(el_stav.attrib['wId'])
    # print(el_clan.tag, el_clan.attrib)

    return stablo
