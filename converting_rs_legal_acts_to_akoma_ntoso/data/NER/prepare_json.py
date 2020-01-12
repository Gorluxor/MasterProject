import io
import json
import os
import xml.etree.ElementTree as ET
from tokenizer.HTMLTokenizer import HTMLTokenizer


fajlovi = os.listdir("../aktovi_raw")

list2 = []
for fajl in fajlovi:
    f = io.open("../aktovi_raw/"+fajl, mode="r", encoding="utf-8")
    stringo = f.read()
    #print(stringo)
    html_root = ET.fromstring("<article>" + stringo + "</article>")
    tokenizer = HTMLTokenizer(html_root)
    while(True):
        token = tokenizer.get_next_token()

        if (token is None):
            break
        elif token.type > 4:
            list2.append({"text": token.value})
    print(fajl)
    if len(list2)>1000:
        break


for i in list2:
    print(i["text"])

#with io.open('train.json', 'w', encoding='utf8') as json_file:
#    json.dump(list2, json_file, ensure_ascii=False)
#f = io.open("train.json", mode="w", encoding="utf-8")
#f.write(json.dumps(list2, ensure_ascii=False).encode('utf8'))
#f.close()
print(len(list2))


