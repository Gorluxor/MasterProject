import xml.etree.ElementTree as ET
import io

try:
    from Akoma.utilities import utilities
    from Akoma.form_akoma.Metadata import Metadata
    from Akoma.preprocessing import init_akoma
except ModuleNotFoundError:
    try:
        from utilities import utilities
        from form_akoma.Metadata import Metadata
        from preprocessing import init_akoma
    except ModuleNotFoundError:
        print("Error")
        exit(-1)
import os

PREFIX = "{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}"
SOURCE = "#somebody"  # "#pravno-informacioni-sistem"
ADDED_DATE = "-01-01"


def fix_date(before):
    a = before.split("-")
    if len(a) == 1:
        return before + ADDED_DATE;
    for i in range(0, len(a)):
        if len(a[i]) < 2:
            a[i] = "0" + a[i]
    after = "-".join(a)
    return after


def add_new_meta(meta: Metadata):
    """
    If file to added meta
    Назив прописа  # ELI#Напомена издавача#Додатне информације#Врста прописа#Доносилац#Област#Група#Датум усвајања#Гласило и датум објављивања#Датум ступања на снагу основног текста#Датум примене#Правни претходник#Издавач#filename
    :param meta:
    :return:
    """
    file_meta = open(utilities.get_root_dir() + "/data/meta/allmeta.csv", mode="a")
    deli = "#"
    new_line = meta.act_name + deli + meta.eli + deli + meta.napomena_izdavaca + deli + meta.dodatne_informacije + deli + meta.vrsta_propisa + deli + meta.donosilac + deli + meta.oblast + deli + meta.grupa + deli + meta.datum_usvajanja + deli + meta.glasilo_i_datum + deli + meta.datum_stupanja + deli + meta.pravni_prethodnik + deli + meta.izdavac + deli + meta.filename
    file_meta.write()

    pass


class MetadataBuilder():

    def __init__(self, csv_file):
        self.csv = io.open(csv_file, mode="r", encoding="utf-8")
        self.expressionuri = ""

    def identification(self, metadata):
        base = ET.Element("identification", {"source": SOURCE})
        base.append(self.frbrwork(metadata["work"]["date"], metadata["work"]["version"], metadata["author"]))
        base.append(
            self.frbrexpression(metadata["manifest"]["date"], metadata["manifest"]["version"], metadata["editor"]))
        base.append(
            self.frbrmanifestation(metadata["manifest"]["date"], metadata["manifest"]["version"], metadata["editor"]))
        return base

    def frbrwork(self, date, version, author):
        base = ET.Element("FRBRWork")
        base.append(ET.Element("FRBRthis", {"value": "/rs/act/" + date + "/" + version + "/main"}))
        base.append(ET.Element("FRBRuri", {"value": "/rs/act/" + date + "/" + version}))
        base.append(ET.Element("FRBRdate", {"date": fix_date(date), "name": "Generation"}))
        base.append(ET.Element("FRBRauthor", {"href": "#" + author, "as": "#author"}))
        base.append(ET.Element("FRBRcountry", {"value": "rs"}))
        return base

    def frbrexpression(self, date, version, editor):
        base = ET.Element("FRBRExpression")

        base.append(ET.Element("FRBRthis", {"value": "/rs/act/" + date + "/" + version + "/srp@/main"}))
        base.append(ET.Element("FRBRuri", {"value": "/rs/act/" + date + "/" + version + "/srp@"}))
        self.expressionuri = "/rs/act/" + date + "/" + version + "/srp@"
        base.append(ET.Element("FRBRdate", {"date": fix_date(date), "name": "Generation"}))
        base.append(ET.Element("FRBRauthor", {"href": "#" + editor, "as": "#editor"}))
        base.append(ET.Element("FRBRlanguage", {"language": "srp"}))

        return base

    def frbrmanifestation(self, date, version, editor):
        base = ET.Element("FRBRManifestation")

        base.append(ET.Element("FRBRthis", {"value": "/rs/act/" + date + "/" + version + "/srp@/main.xml"}))
        base.append(ET.Element("FRBRuri", {"value": "/rs/act/" + date + "/" + version + "/srp@.akn"}))

        base.append(ET.Element("FRBRdate", {"date": fix_date(date), "name": "Generation"}))
        base.append(ET.Element("FRBRauthor", {"href": "#" + editor, "as": "#editor"}))
        base.append(ET.Element("FRBRformat", {"value": "xml"}))

        return base

    def publication(self, publication):
        base = ET.Element("publication", {"date": fix_date(publication["date"]), "name": publication["journal"].lower(),
                                          "showAs": publication["journal"], "number": publication["number"]})
        return base

    """
        [{"wId": "vrsta", value: "Zakon"},
        {"wid": "oblast", ...},
        {"wid": "grupa", ...}
        ]
    """

    def clssification(self, clssifications):
        base = ET.Element("classification", {"source": SOURCE})
        for dict in clssifications:
            newk = ET.Element("keyword", {"wId": dict["id"], "value": dict["value"].lower(), "showAs": dict["value"],
                                          "dictionary": "TODO"})  # TODO Andrija Popraviti dictionary
            base.append(newk)
        return base

    """
        [{"wid": "usvajanje", date: "2018-12-21"},
        {"wid": "stupanje na snagu", date: "2018-12-21"},
        "wid": "primena", date: "2018-12-21"},
        ]
    """

    def workflow(self, workflows):
        base = ET.Element("workflow", {"source": SOURCE})
        for dict in workflows:
            newk = ET.Element("step", {"wId": dict["id"], "date": dict["date"],
                                       "by": "#TODO"})  # TODO Andrija TLC Person or TLC Organization reference
            base.append(newk)
        return base

    def lifecycle(self, lifecycles):
        base = ET.Element("lifecycle", {"source": SOURCE})
        cnt = 1
        for date in lifecycles:
            found_i = date.find("/") + 1
            if cnt == 1:
                newk = ET.Element("eventRef",
                                  {"wId": "e" + str(cnt), "refersTo": date, "date": fix_date(date[found_i:found_i + 4]),
                                   "type": "generation", "source": SOURCE})
            else:
                newk = ET.Element("eventRef",
                                  {"wId": "e" + str(cnt), "refersTo": date, "date": fix_date(date[found_i:found_i + 4]),
                                   "type": "amendment", "source": SOURCE})
            base.append(newk)
            cnt += 1
        return base

    def notes(self, notes1, notes2):
        base = ET.Element("notes", {"source": SOURCE})
        if notes1 != "":
            newk = ET.Element("note", {"wId": "not1"})
            p = ET.Element("p")
            p.text = notes1
            newk.append(p)
            base.append(newk)
        if notes2 != "":
            if notes1 != "":
                newk = ET.Element("note", {"wId": "not2"})
            else:
                newk = ET.Element("note", {"wId": "not1"})
            p = ET.Element("p")
            p.text = notes1
            newk.append(p)
            base.append(newk)
        return base

    # SUMA = []
    def build(self, filename, akomaroot):
        meta = list(akomaroot)[0].find(PREFIX + "meta")
        if meta is None:
            meta = list(akomaroot)[0].find("meta")

        metainfo = None
        # print(csv.read())
        for line in self.csv.readlines():
            values = line.strip().split("#")
            if filename == values[14]:
                metainfo = Metadata(values)
                break
        if metainfo is None:
            print(filename)
            print("Fajl nije pronadjen u metadata.csv")
            return
        try:
            _ = metainfo.work
            has_work = True
        except AttributeError:
            has_work = False
        if has_work and metainfo.work is not None:
            meta.append(self.identification({"work": metainfo.work, "manifest": metainfo.manifest,
                                             "author": "somebody", "editor": "somebody"}))
        else:
            print(filename, metainfo.act_name)
            dict = {"date": metainfo.datum_usvajanja, "version": metainfo.version}
            meta.append(self.identification({"work": dict, "manifest": dict,
                                             "author": "somebody", "editor": "somebody"}))

        if metainfo.publication != False and metainfo.publication != None:
            meta.append(self.publication(metainfo.publication))
        else:
            pass
        # print(filename, metainfo.publication)
        # SUMA.append(0)#sluzi za brojanje koliko njih ukupno ima neuspesno parsiranu publikaciju, nista vise

        if len(metainfo.classifications) > 0:
            meta.append(self.clssification(metainfo.classifications))

        if metainfo.lifecycle is not None and len(metainfo.lifecycle) > 1:
            meta.append(self.lifecycle(metainfo.lifecycle))

        if len(metainfo.workflow) > 0:
            meta.append(self.workflow(metainfo.workflow))

        references = ET.Element("references", {"source": SOURCE})
        temprory = ET.Element("TLCConcept", {"href": "#", "showAs": "Temp"})
        references.insert(0, temprory)
        meta.append(references)

        if metainfo.napomena_izdavaca != "" or metainfo.dodatne_informacije != "":
            meta.append(self.notes(metainfo.napomena_izdavaca, metainfo.dodatne_informacije))


if __name__ == "__main__":
    akoma_root = init_akoma.init_xml("act")

    for fajl in os.listdir("../data/acts"):
        metabuilder = MetadataBuilder("../data/meta/allmeta.csv")
        metabuilder.build(fajl, akoma_root)
# print(len(SUMA))
