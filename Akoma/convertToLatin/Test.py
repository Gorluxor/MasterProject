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


if __name__ == "__main__":
    # schema = xmlschema.XMLSchema11('../schema/akn3.0_schema1.1_Republic_Serbia.xsd')
    schema = xmlschema.XMLSchema11('../schema/akoma30.xsd')

    fajls = utilities.sort_file_names(os.listdir("../data/akoma_result"))
    f = open("../data/sanity_schema.txt", mode="a+", encoding="UTF-8")
    for i in range(0, len(fajls)):
        try:
            try:
                schema.validate('../data/akoma_result/' + fajls[i])
            except Exception as e1:
                print("Schema validation error :" + fajls[i] + " MES:" + e1.message)
                f.write(fajls[i] + " : Not valid with schema " + e1.message + "\n")
        except Exception as e:
            print("Not well formed " + fajls[i])
            f.write(fajls[i] + " : Not well formed xml document " + "\n")
    f.close()
