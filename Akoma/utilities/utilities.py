import re

try:
    from Akoma.form_akoma.Metadata import Metadata
    from Akoma.tokenizer import patterns
    from Akoma.convertToLatin import Convert
except ModuleNotFoundError:
    try:
        from convertToLatin import Convert
        from tokenizer import patterns
        from form_akoma.Metadata import Metadata
    except ModuleNotFoundError as e:
        print(e)
        print("Error")
        exit()


def get_meta(filename: str, path: str = "..//data/meta/allmeta.csv"):
    """

    :param filename: name of scraped document
    :param path: path to metadata csv file
    :return: Metadata.class or None if not found
    """
    csv = open(path, mode="r", encoding="utf-8")
    for line in csv.readlines():
        values = line.strip().split("#")
        if filename == values[14]:
            csv.close()
            return Metadata(values)
    csv.close()
    return None


def sort_file_names(file_names_list):
    from functools import cmp_to_key
    return sorted(file_names_list, key=cmp_to_key(compare_file_names))


def compare_file_names(item1: str, item2: str):
    num1 = int(item1[0:item1.find(".")])
    num2 = int(item2[0:item2.find(".")])
    return num1 - num2


def regex_events(document_text: str) -> list:
    found = []
    day = '((?<!\d)\d{1}(?!\d)|(?<!\d)\d{2})\.'
    month_lat = 'januara|januar|februar|februara|marta|mart|april|aprila|maja|maj|jun|juna|avgusta|avgust|septembra|septebar|oktobra|oktobar|novembar|novembra|decembra|decembar'
    month_cir = 'јануара|јануар|фебруар|фебруара|марта|март|април|априла|маја|мај|јун|јуна|августа|август|септембра|септебар|октобра|октобар|новембар|новембра|децембра|децембар'
    god = '\d{4}\.'
    reg_pattern = day + '( )+(' + month_lat + '|' + month_cir + ')( )+' + god
    do = True
    document_text = document_text.replace("\n", " ")
    while do:
        match = re.search(reg_pattern, document_text)
        if match is None:
            break
        where = match.span(0)
        text = document_text[where[0]:where[1]]
        document_text = document_text[where[1]:]
        if text not in found:
            found.append(text)
    return found


def entities_add_date(map_ner: dict, events: list):
    for date in events:
        date = Convert.convert_string(date)
        date = re.sub("\s\s+", " ", date)
        if map_ner.get('date') is None:
            map_ner['date'] = []
        if date not in map_ner['date']:
            map_ner['date'].append(date)


def month_in(text) -> bool:
    if 'januar' in text or 'јануар' in text:
        return True
    elif "febuar" in text or 'фебуар' in text:
        return True
    elif "mart" in text or 'март' in text:
        return True
    elif "april" in text or 'април' in text:
        return True
    elif "maj" in text or 'мај' in text:
        return True
    elif "jun" in text or 'јун' in text:
        return True
    elif "jul" in text or 'јул' in text:
        return True
    elif "avgust" in text or 'август' in text:
        return True
    elif "septemb" in text or 'септемб' in text:
        return True
    elif "octob" in text or 'оцтоб' in text:
        return True
    elif "novemb" in text or 'новемб' in text:
        return True
    elif "decemb" in text or 'децемб' in text:
        return True
    return False


def number_in(text, just_year=False, just_day=False) -> bool:
    found_year = re.findall('\d{4}', text)
    found_day = re.findall('(?<!\d)\d{1}(?!\d)', text)
    found_day_2 = re.findall('(?<!\d)\d{2}(?!\d)', text)
    if found_year and (found_day or found_day_2) or (found_year and just_year) or \
        ((found_day or found_day_2) and just_day):
        return True
    else:
        return False


def special_date(text: str) -> bool:
    text = text.strip().replace(".", "")
    if text[0] in patterns.AZBUKA_VELIKA or text[0] in patterns.LAT_AZBUKA_VELIKA:
        if text[1] not in patterns.AZBUKA_VELIKA and text[1] not in patterns.LAT_AZBUKA_VELIKA:
            return True
    else:
        return False


def find_clan_text(text):
    from convertToLatin import regex_patterns
    import re
    tag_clan = "Član"
    if "Član" not in text:
        tag_clan = "Члан"
    act_array = []
    if text.find("<") != -1:
        text = regex_patterns.strip_html_tags(text)

    list_to_str = text + tag_clan + " 0."
    found = re.finditer(tag_clan + " [0-9]*\.", list_to_str)
    start_from = 0
    ends_to = 0
    for m in found:
        if start_from == ends_to:
            ends_to = 0
        else:
            ends_to = m.start()
        if ends_to != 0:
            insert_string = list_to_str[start_from:ends_to]
            act_array.append(insert_string)
        start_from = m.end()
    return act_array


def get_root_dir():
    from os import path
    pather = path.dirname(__file__)
    path_this = path.normpath(pather)
    i = path_this.rfind("\\")
    if i == -1:  # MAC FIND
        i = pather.rfind('/')
    b = path_this[:i]
    return b.replace("\\", "/")


if __name__ == "__main__":
    a = get_meta("1.html")
    print(a.act_name)

    print(get_root_dir())
    print("End")
