import xml.etree.ElementTree as ET
import re
from enum import IntEnum

ROMAN_NUMERAL = "[MDCLXVI]+"


class TokenType(IntEnum):
    DEO = 0
    GLAVA = 1
    ODELJAK = 2
    PODODELJAK = 3
    CLAN = 4
    STAV = 5
    TACKA = 6
    PODTACKA = 7
    ALINEJA = 8


class FoundToken():
    def __init__(self, type, name, value, number, number2=None, numberstr=None):
        self.type = type
        self.name = name
        self.value = value
        self.number = number
        self.number2 = number2
        self.numberstr = numberstr


def is_vrsta_akta(text):
    m = re.match("(ОДЛУКА|ОДУЛУКУ|ПРАВИЛНИК|ЗАКОН|ПРОПИС|ЗАКЉУЧАК|КОДЕКС|ЛИСТУ|ПЛАН|УРЕДБА|УРЕДБУ)", text.upper())
    if m:
        return True
    return False

def recognize_pattern(el):
    if el.tag == "table" or el.tag == "img":
        retval = FoundToken(TokenType.STAV, "став", ET.tostring(el, encoding="utf-8", method="html"), None)
        print(retval.value)
        return retval
    text = el.text
    if text is None:
        text = ""
    text = text.strip()
    text = re.sub("\s", " ", text)
    if text == "":
        return False
    retval = is_deo(text)
    if retval:
        return retval
    retval = is_glava(text)
    if retval:
        return retval
    retval = is_odeljak(text)
    if retval:
        return retval
    retval = is_pododeljak(text)
    if retval:
        return retval
    retval = is_clan(text)
    if retval:
        return retval
    retval = is_tacka(text)
    if retval:
        return retval
    retval = is_podtacka(text)
    if retval:
        return retval
    retval = is_alineja(text)
    if retval:
        return retval
    retval = is_stav(text)
    if retval:
        return retval
    return None

brojevi = ["ПРВИ", "ДРУГИ", "ТРЕЋИ", "ЧЕТВРТИ", "ПЕТИ", "ШЕСТИ", "СЕДМИ", "ОСМИ","ДЕВЕТИ" , "ДЕСЕТИ", "ЈЕДАНАЕСТИ", "ДВАНАЕСТИ"]

def is_deo(text):
    m = re.match("(.*) (ДЕО|део)", text)
    if m:
        for i in range(0, len(brojevi)):
            if brojevi[i] == m.group(1):
                return FoundToken(TokenType.DEO, "део", None, i + 1, numberstr=text)

    m = re.match("(ДЕО|део) (.*)", text)
    if m:
        for i in range(0, len(brojevi)):
            if brojevi[i] == m.group(2):
                return FoundToken(TokenType.DEO, "део", None, i + 1, numberstr=text)
    return False

def is_glava(text):
    m = re.match("(Глава|ГЛАВА) ("+ROMAN_NUMERAL+")", text)
    if m:
        return FoundToken(TokenType.GLAVA, "глава", None, roman_to_int(m.group(2)), numberstr=m.group(2))

    m = re.match("(" + ROMAN_NUMERAL + ")(\.) (.*)" , text)
    if m:
        return FoundToken(TokenType.GLAVA, "глава", m.group(3), roman_to_int(m.group(1)), numberstr=m.group(1))

    return False


def is_odeljak(text):
    m = re.match("([0-9]+)(\.)(.*)", text)
    if m:
        return FoundToken(TokenType.ODELJAK, "одељак", m.group(3), int(m.group(1)), numberstr=m.group(1)+".")
    return False


def is_pododeljak(text):
    m = re.match("([а-з])(\))(.*)", text)#TODO: fix
    if m:
        return FoundToken(TokenType.PODODELJAK, "пододељак", m.group(3), None, numberstr=m.group(1))
    return False


def is_clan(text):
    m = re.match("(Члан) ([0-9]+)(\.)", text)
    if m:
        return FoundToken(TokenType.CLAN, "члан",None , int(m.group(2)), numberstr=m.group(2)+".")
    m = re.match("(Чл\.) ([0-9]+\-[0-9]+)(\.)", text)
    if m:
        br1 = int(m.group(2).split("-")[0])
        br2 = int(m.group(2).split("-")[1])
        return FoundToken(TokenType.CLAN, "члан", None, br1, br2, numberstr=m.group(2)+".")
    return False

def is_stav(text):
    #sve moze da bude stav?
    return FoundToken(TokenType.STAV, "став", text, None)

def is_tacka(text):
    m = re.match("([0-9]+)(\))(.*)", text)
    if m:
        return FoundToken(TokenType.TACKA, "тачка", m.group(3), int(m.group(1)),numberstr=m.group(1)+")")
    return False

def is_podtacka(text):
    m = re.match("(\()([0-9]+)(\))(.*)", text)
    if m:
        return FoundToken(TokenType.PODTACKA, "подтачка", m.group(4), int(m.group(2)), numberstr="("+m.group(2)+")")
    return False

def is_alineja(text):
    m = re.match("(– ?\w?)(.*)", text)
    if m:
        return FoundToken(TokenType.ALINEJA, "алинеја", m.group(2), None)
    return False

def int_to_roman(input):
    """ Convert an integer to a Roman numeral.
    Source: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch03s24.html"""

    if not isinstance(input, type(1)):
        raise (TypeError, "expected integer, got %s" % type(input))
    if not 0 < input < 4000:
        raise (ValueError, "Argument must be between 1 and 3999")
    ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
    nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)

def roman_to_int(input):
    """ Convert a Roman numeral to an integer.
    Source: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch03s24.html"""
    input = input.upper()
    nums = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}
    sum = 0
    for i in range(len(input)):
        try:
            value = nums[input[i]]
            # If the next place holds a larger number, this value is negative
            if i+1 < len(input) and nums[input[i+1]] > value:
                sum -= value
            else: sum += value
        except KeyError:
            raise (ValueError, 'input is not a valid Roman numeral: %s' % input)
    # easiest test for validity...
    if int_to_roman(sum) == input:
        return sum
    else:
        raise (ValueError, 'input is not a valid Roman numeral: %s' % input)


class TestElement():
    def __init__(self, text):
        self.text = text

if __name__=="__main__":
    if not is_glava("Глава V"):
        print("is_glava - Error")

    if not is_glava("I. Наслов главе"):
        print("is_glava - Error")

    if not is_odeljak("1. Наслов неког одељка"):
        print("is_odeljak - Error")

    if not is_pododeljak("д) Наслов пододељка, нешто компликовано"):
        print("is_pododeljak - Error")

    if not is_clan("Члан 145."):
        print("is_clan - Error")

    if not is_clan("Чл. 14-72."):
        print("is_clan - Error")

    if not is_tacka("1) Објашњење о првој тачцич;"):
        print("is_tacka - Error")

    if not is_podtacka("(4) Објашњење неке поддачке нешто тако."):
        print("is_podtacka - Error")

    if not is_alineja("– у 2014. години на дан 31. децембар – у висини 1/12 укупног износа обавезе утврђене из члана 2. овог закона;"):
        print("is_alineja - Error")



    print(recognize_pattern(TestElement("Глава MXXXIV")).number)
    print(recognize_pattern(TestElement("(4) Објашњење неке поддачке нешто тако.")).number)
    print(recognize_pattern(TestElement("Чл. 14-72.")).number,recognize_pattern(TestElement("Чл. 14-72.")).number2)
    print(recognize_pattern(TestElement("д) Наслов пододељка, нешто компликовано")).name)
    print(recognize_pattern(TestElement("astasoitjpaisnf asf asfkja sf asfk s")).type-1 == TokenType.CLAN)

