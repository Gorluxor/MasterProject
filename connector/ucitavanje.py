data_file = open("NER\\setimes-sr.conll\\set.sr.conll", "r", encoding="utf-8")
list = []
for line in data_file:
    if line.strip().__len__() < 1:
        continue
    elif line[0] == '#':
        continue

    #try:
    split = line.strip().replace('\t', " ").split(" ")
    wordsplit = split[1]
    tagsplit = split[10]
    if wordsplit.__contains__(',') or wordsplit.__contains__(";"):
        continue
    t = (wordsplit.rsplit(), tagsplit.rsplit())
    if not list.__contains__(t):
        list.append(t)
    #except:
    #    print(line.strip())  # if this comes to show, it means there was a error


new_file = open("dataset.csv", "w+", encoding="utf-8")
new_file.write("Word, Ner-Tag\n")
for a, b in list:
    new_file.write("{0};{1}\n".format(str(a[0]), str(b[0])))
new_file.close()
print("Done")


