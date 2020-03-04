from owlready2 import *
# onto_path.append("onto")
# onto = get_ontology("eli.rdf")
# onto.load()

# sko = get_ontology("http://www.w3.org/2004/02/skos/core")
# sko.load()
# Drug = onto.LegalResource
#
# test = onto.LegalResource("Test")
#for i in Drug.instances(): print(i)
# test_pizza = onto.Pizza("test")   http://data.europa.eu/eli/ontology#LegalResource
#Concept
#onto.save("onto/output.rdf")

cls_legal_resource = "LegalResource"
cls_legal_resource_sub = "LegalResourceSubdivision"
#http://www.w3.org/2004/02/skos/core#Concept
p_is_about = "is_about"

class OntologyPopulator:

    def __init__(self):
        onto_path.append("onto")
        self.onto = get_ontology("eli.rdf")
        self.onto.load()
        self.skos = self.onto.get_namespace("http://www.w3.org/2004/02/skos/core")
        self.concept_class = [s for s in self.onto.Language.ancestors() if s.name == "Concept"][0]

    def save(self):
        self.onto.save("onto/output.rdf")


    def add_instance(self, class_name, instance_name):
        return eval("self.onto.{0}('{1}')".format(class_name, instance_name))

    @staticmethod
    def add_relation(object_on_which_to_add, property_name, object_to_add):
        return eval("object_on_which_to_add.{0}.__add__(['{1}'])".format(property_name, object_to_add))


    def add_concept(self, name):
        newConcept = eval("self.skos.{0}('{1}') ".format("Concept", name))
        newConcept.is_a.append(self.concept_class)
        return newConcept

#skos = onto.get_namespace("http://www.w3.org/2004/02/skos/core")




#skos = get_namespace("http://www.w3.org/2004/02/skos/core")

#owl = onto.get_namespace("http://www.w3.org/2002/07/owl")

#Ww = owl.Thing("Testimus")
#Ww.is_a.append(skos)

#print(skos)

#t1 = eval("onto('{0}')".format("TestimusMaximus"))
#t2 = Concept("Test")

#a = [s for s in onto.Language.ancestors() if s.name == "Concept"][0]
#t3 = a.__class__("test")

#for qw in onto.Language.ancestors():
#    print(qw)
#qwe = eval("skos.{0}('{1}') ".format("Concept", "Novi"))


#qwe.is_a.append(a)

#print(qwe)
#test.is_about = [qwe]
#onto.save("onto/output.rdf")


if __name__ == "__main__":
    op = OntologyPopulator()
    test = op.add_instance(cls_legal_resource, "Test")
    c1 = op.add_concept("Himna")

    op.add_relation(test, p_is_about, c1)
    #test.is_about = [c1]  # radi ova varijanta
    #test.is_about.
    op.save()
# for q in onto.classes():
#     print(q)