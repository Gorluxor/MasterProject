# from tei_reader import TeiReader
# reader = TeiReader()
# corpora = reader.read_file("NER\\setimes-sr.TEI\\setimes-sr.body.xml") # or read_string
# print(corpora.text)
#
# print(corpora.tostring(lambda x, text: str(list(a.key + '=' + a.text for a in x.attributes)) + text))
from conllu import parse
from io import open
from conllu import parse_incr
data_file = open("NER\\setimes-sr.conll\\set.sr.conll", "r", encoding="utf-8")
for tokenlist in parse_incr(data_file):
    print(tokenlist)
    print("---------------------")
