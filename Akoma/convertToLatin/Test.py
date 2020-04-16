import os

try:
    from utilities import utilities
except ModuleNotFoundError:
    try:
        from Akoma.utilities import utilities
    except ModuleNotFoundError:
        print("Import error")
        exit(-1)

import xmlschema

schema = xmlschema.XMLSchema11('../schema/akn3.0_schema1.1_Republic_Serbia.xsd')

fajls = utilities.sort_file_names(os.listdir("../data/akoma_result"))
f = open("../data/za_andriju.txt", mode="a+", encoding="UTF-8")
for i in range(0, len(fajls)):
    try:
        if schema.is_valid('../data/akoma_result/' + fajls[i]) is False:
            print("Schema error :" + fajls[i])
            f.write(fajls[i] + " : Not valid with schema + \n")
        #else:
            #print("No problem :" + fajls[i])
    except Exception as e:
        print("Not well formed " + fajls[i])
        f.write(fajls[i] + " : Not well formed xml document +\n")
f.close()
# xml_file = etree.parse("sample.xml")
# is_valid = xml_validator.validate(xml_file)
