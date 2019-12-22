import xml.etree.ElementTree as ET
import io
from form_akoma.Metadata import Metadata
import preprocessing.init_akoma
import os

PREFIX = "{http://www.akomantoso.org/2.0}"
SOURCE = "#somebody"#"#pravno-informacioni-sistem"

class MetadataBuilder():

	def __init__(self, csv_file):
		self.csv = io.open(csv_file, mode="r", encoding="utf-8")
		self.expressionuri = ""

	def identification(self, metadata):
		base = ET.Element("identification", {"source": SOURCE})
		base.append(self.frbrwork(metadata["work"]["date"], metadata["work"]["version"], metadata["author"]))
		base.append(self.frbrexpression(metadata["manifest"]["date"], metadata["manifest"]["version"], metadata["editor"]))
		base.append(self.frbrmanifestation(metadata["manifest"]["date"], metadata["manifest"]["version"], metadata["editor"]))
		return base

	def frbrwork(self, date, version, author):
		base = ET.Element("FRBRWork")
		base.append(ET.Element("FRBRthis", {"value": "/rs/act/"+date+"/"+version+"/main"}))
		base.append(ET.Element("FRBRuri", {"value": "/rs/act/" + date + "/" + version}))
		base.append(ET.Element("FRBRdate", {"date": date, "name": "Generation"}))
		base.append(ET.Element("FRBRauthor", {"href": "#"+author, "as": "#author"}))
		base.append(ET.Element("FRBRcountry", {"value": "rs"}))
		return base


	def frbrexpression(self, date, version, editor):
		base = ET.Element("FRBRExpression")

		base.append(ET.Element("FRBRthis", {"value": "/rs/act/" + date + "/" + version  +"/srp@/main"}))
		base.append(ET.Element("FRBRuri", {"value": "/rs/act/" + date + "/" + version+"/srp@"}))
		self.expressionuri = "/rs/act/" + date + "/" + version+"/srp@"
		base.append(ET.Element("FRBRdate", {"date": date, "name": "Generation"}))
		base.append(ET.Element("FRBRauthor", {"href": "#" + editor, "as": "#editor"}))
		base.append(ET.Element("FRBRlanguage", {"language": "srp"}))

		return base


	def frbrmanifestation(self, date, version, editor):
		base = ET.Element("FRBRManifestation")

		base.append(ET.Element("FRBRthis", {"value": "/rs/act/" + date + "/" + version +"/srp@/main.xml"}))
		base.append(ET.Element("FRBRuri", {"value": "/rs/act/" + date + "/" + version+"/srp@.akn"}))

		base.append(ET.Element("FRBRdate", {"date": date, "name": "Generation"}))
		base.append(ET.Element("FRBRauthor", {"href": "#" + editor, "as": "#editor"}))
		base.append(ET.Element("FRBRformat", {"value": "xml"}))

		return base

	def publication(self, publication):
		base = ET.Element("publication", {"date": publication["date"], "name": publication["journal"].lower(),
										  "showAs": publication["journal"], "number": publication["number"]})
		return base
	"""
		[{"id": "vrsta", value: "Zakon"},
		{"id": "oblast", ...},
		{"id": "grupa", ...}
		]
	"""
	def clssification(self, clssifications):
		base = ET.Element("classification", {"source": SOURCE })
		for dict in clssifications:
			newk = ET.Element("keyword", {"id": dict["id"], "value": dict["value"].lower(), "showAs":dict["value"]})
			base.append(newk)
		return base
	"""
		[{"id": "usvajanje", date: "2018-12-21"},
		{"id": "stupanje na snagu", date: "2018-12-21"},
		"id": "primena", date: "2018-12-21"},
		]
	"""
	def workflow(self, workflows):
		base = ET.Element("workflow", {"source": SOURCE })
		for dict in workflows:
			newk = ET.Element("step", {"id": dict["id"], "date": dict["date"]})
			base.append(newk)
		return base

	def lifecycle(self, lifecycles):
		base = ET.Element("lifecycle", {"source": SOURCE })
		cnt = 1
		for date in lifecycles:
			if cnt == 1:
				newk = ET.Element("eventRef", {"id": "e"+str(cnt),"date":date, "type": "generation"})
			else:
				newk = ET.Element("eventRef", {"id": "e"+str(cnt),"date":date, "type": "amendment"})
			base.append(newk)
			cnt += 1
		return base

	def notes(self, notes1, notes2):
		base = ET.Element("notes", {"source": SOURCE})
		if notes1 != "":
			newk = ET.Element("note", {"id": "not1"})
			p = ET.Element("p")
			p.text = notes1
			newk.append(p)
			base.append(newk)
		if notes2 != "":
			if notes1 != "":
				newk = ET.Element("note", {"id": "not2"})
			else:
				newk = ET.Element("note", {"id": "not1"})
			p = ET.Element("p")
			p.text = notes1
			newk.append(p)
			base.append(newk)
		return base




	#SUMA = []
	def build(self, filename, akomaroot):

		meta = list(akomaroot)[0].find(PREFIX + "meta")

		metainfo = None
		#print(csv.read())
		for line in self.csv.readlines():
			values = line.strip().split("#")
			if filename == values[14]:

				metainfo = Metadata(values)
				break
		if metainfo is None:
			print(filename)
			print("Fajl nije pronadjen u metadata.csv")
			return
		if metainfo.work is not None:
			meta.append(self.identification({"work": metainfo.work, "manifest": metainfo.manifest,
											 "author": "somebody", "editor": "somebody"}))
		else:
			print(filename, metainfo.act_name)
			dict = {"date": metainfo.datum_usvajanja, "version": metainfo.version}
			meta.append(self.identification({"work":dict, "manifest": dict,
											 "author": "somebody", "editor":"somebody"}))


		if metainfo.publication != False and metainfo.publication != None:
			meta.append(self.publication(metainfo.publication))
		else:
			pass
			#print(filename, metainfo.publication)
			#SUMA.append(0)#sluzi za brojanje koliko njih ukupno ima neuspesno parsiranu publikaciju, nista vise

		if len(metainfo.classifications) > 0:
			meta.append(self.clssification(metainfo.classifications))

		if len(metainfo.workflow) > 0:
			meta.append(self.workflow(metainfo.workflow))

		if metainfo.lifecycle is not None and len(metainfo.lifecycle)>1:
			meta.append(self.lifecycle(metainfo.lifecycle))

		if metainfo.napomena_izdavaca != "" or metainfo.dodatne_informacije != "":
			meta.append(self.notes(metainfo.napomena_izdavaca, metainfo.dodatne_informacije))

if __name__=="__main__":
	akoma_root = preprocessing.init_akoma.init_xml("act")

	for fajl in os.listdir("../data/aktovi_html"):
		metabuilder = MetadataBuilder("../data/metadata.csv")
		metabuilder.build(fajl, akoma_root)
	#print(len(SUMA))