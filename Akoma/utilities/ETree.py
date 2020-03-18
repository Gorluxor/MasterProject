import utilities
import xml.etree.ElementTree as ET

# https://eli.thegreenplace.net/2012/03/15/processing-xml-in-python-with-elementtree/

TAG_DEO = 'part'
TAG_GLAVA = 'chapter'
TAG_ODELJAK = 'section'
TAG_PODODELJAK = 'subsection'
TAG_CLAN = 'article'
TAG_STAV = 'paragraph'  # 'clause'
TAG_TACKA = 'point'
TAG_PODTACKA = 'hcontainer'
TAG_ALINEA = 'alinea'

Tag_dict = {'deo': TAG_DEO, 'glava': TAG_GLAVA, 'odeljak': TAG_ODELJAK, 'pododeljak': TAG_PODODELJAK, 'clan': TAG_CLAN,
            'stav': TAG_STAV, 'tacka': TAG_TACKA, 'podtacka': TAG_PODTACKA, 'alinea': TAG_ALINEA}
CNS = '{http://www.akomantoso.org/2.0}'


def get_akoma_tag(name):
    """
    Iz tagova pravnih propisa vraća tagove u Akoma Ntoso specifikacije koji su dogovoreni
    :param name: Name of hierarchical element in legal document like Deo,Glava ....
    :return: Appointed tag in Akoma Ntoso 3.0 specification
    """
    name = name.lower()
    return Tag_dict[name]  # Tag_dict.get(name)


def append_to_element_by_id(root, name, id, new_element, namespace=CNS):
    if not ET.iselement(new_element):
        raise ValueError('Expected new element should be element of ElementTree library')
    ret = get_elements_by_id(root, name, id, namespace)
    ret[0].append(new_element)


def get_elements(root, name, namespace=CNS):
    ret = [iter_chapter for iter_chapter in root.iter(tag=namespace + name)]
    return ret


def get_elements_by_id(root, name, id, namespace=CNS):
    ret = [iter_chapter for iter_chapter in get_elements(root, name, namespace) if iter_chapter.attrib['id'] == id]
    return ret


def get_glavas_by_id(root, id, namespace=CNS):
    ret = get_elements_by_id(root, TAG_GLAVA, id, namespace)
    return ret


def get_glavas(root, namespace=CNS):
    return get_elements(root, TAG_GLAVA, namespace)


def get_clans(root, namespace=CNS):
    return get_elements(root, TAG_CLAN, namespace)


def get_clan_by_id(root, id, namespace=CNS):
    return get_elements_by_id(root, TAG_CLAN, id, namespace)


def try1():
    print("TRY1")


if __name__ == "__main__":
    # Deprecated
    # f = open(path, mode="r", encoding="utf8")
    # lines = f.readlines()
    # str_lines = "".join(lines)
    # rootic = ET.fromstring(str_lines)

    path = utilities.get_root_dir() + "/data/akoma_result/1.xml"

    tree = ET.parse(path)
    ns = '{http://www.akomantoso.org/2.0}'
    g = get_glavas_by_id(tree, "gla1", ns)

    to_add = ET.fromstring('<chapter id="new_chap"><num>10</num><content>Zakon rada</content></chapter>\n')  # RADI
    to_add2 = ET.fromstring('<chapter id="new_2"><num>20</num><content>Zakon buca</content></chapter>\n')  # RADI

    append_to_element_by_id(tree, 'chapter', 'gla1', to_add2) # Primer dodavanja
    g[0].append(to_add)  # Primer kada rucno dodajes na bilo koje element u stablu
    Root = tree.getroot()

    ET.dump(Root)

    for elem in Root.iter(tag=ns + "chapter"):
        ss = elem.attrib['id']
        print(elem.tag, elem.attrib)
        a = 1

    ET.dump(Root)
