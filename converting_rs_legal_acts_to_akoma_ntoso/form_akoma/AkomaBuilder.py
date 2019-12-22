from tokenizer.patterns import  is_vrsta_akta
from tokenizer.TokenType import TokenType
import xml.etree.ElementTree as ET

PREFIX = "{http://www.akomantoso.org/2.0}"


class AkomaBuilder():

    def __init__(self, akomaroot):
        ET.register_namespace('', "http://www.akomantoso.org/2.0")
        self.akomaroot = akomaroot
        self.current = list(akomaroot)[0].find(PREFIX+"body")
        self.stack = [self.current]
        #print(self.result_str())
        #print(self.stack, list(akomaroot)[0].tag)

    def build_preface(self, tokens):
        counter = 0
        preamble = None
        preface = None
        act = list(self.akomaroot)[0]
        for token in tokens[::-1]:
            if preface is None:
                preface = ET.Element("preface")
            counter += 1
            if "напомена" in token.value.lower():
                counter -= 1
            elif counter == 1 :
                date = ET.Element("date")
                date.text = token.value
                preface.insert(0, date)
            elif counter == 2:
                title = ET.Element("title")
                title.text = token.value
                preface.insert(0, title)
            elif is_vrsta_akta(token.value):
                title = ET.Element("title")
                title.text = token.value
                preface.insert(0, title)
                counter -= 1
            elif counter == 3:
                authority = ET.Element("authority")
                authority.text = token.value
                preface.insert(0, authority)
            elif counter >3:
                if preamble is None:
                    preamble = ET.Element("preamble")
                p = ET.Element("p")
                p.text = token.value
                preamble.insert(0, p)
            else:
                counter -= 1
        if preface is not None:
            act.insert(1, preface)
        if preamble is not None:
            act.insert(1, preamble)

    def add_special(self, token):
        parent = self.stack[-1]
        parent.append(token)

    def add_token(self, token, identification):
        #print(token.name, identification, token.value)
        novi = self.create_element(token, identification)
        parent = self.current_parent(identification)

        parent.append(novi)
        self.stack.append(novi)


    def current_parent(self, identification):
        for i in range(len(self.stack)-1,-1,-1):
            node = self.stack[i]
            #print(i, self.stack)
            if node.tag == PREFIX+"body":
                return node

            id = node.attrib["id"]
            if id in identification:
                content = node.find("content")
               # print('TEXT', list(node))
                if content is not None:
                    return content
                else:
                    return node
            self.stack.pop()
        return False

    def create_element(self, token, identification):
        base = ET.Element(token.name, {"id": identification})
        if token.numberstr is not None:
            num = ET.Element("num")
            num.text = token.numberstr
            base.append(num)

        content = ET.Element("content")
        if token.type <= TokenType.CLAN and token.value is not None:
            heading = ET.Element("heading")
            heading.text = token.value
            base.append(heading)
        elif token.type == TokenType.STAV and token.special is not None:
            base.append(token.special)
        elif token.value is not None:
            p = ET.Element("p")
            p.text = token.value
            content.append(p)

        base.append(content)
        return base

    def result_str(self):
        import xml.dom.minidom

        dom = xml.dom.minidom.parseString(ET.tostring(self.akomaroot,encoding='UTF-8', method="xml").decode())  # or xml.dom.minidom.parseString(xml_string)
        pretty_xml_as_string = dom.toprettyxml()

        return pretty_xml_as_string#str(ET.tostring(self.akomaroot,encoding='UTF-8', method="xml").decode())
