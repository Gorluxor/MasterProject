from io import open
from conllu import parse

data_file = open("NER\\setimes-sr.conll\\set.sr.conll", "r", encoding="utf-8")
data = parse(data_file)
sentence = data[0]
print(data.metadata)
# for tokenlist in parse(data_file):
#     print(tokenlist)
#     token = tokenlist[0]
#     print(token)
#     token.metadata