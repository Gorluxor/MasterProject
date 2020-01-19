data_file = open("NER\\setimes-sr.conll\\set.sr.conll", "r", encoding="utf-8")
list = []
for line in data_file:
    if line.strip().__len__() < 1:
        list.append(("","","",""))
        continue
    elif line[0] == '#':
        continue

    #try:
    split = line.strip().replace('\t', " ").split(" ")
    wordsplit = split[1]
    lemmasplit = split[2]
    possplit = split[4]
    tagsplit = split[10]
    t = (wordsplit.rsplit(), lemmasplit.rsplit(), possplit.rsplit(),tagsplit.rsplit())
    #if not list.__contains__(t):
    list.append(t)
    #except:
    #    print(line.strip())  # if this comes to show, it means there was a error


new_file = open("datasetReldi.csv", "w+", encoding="utf-8")
new_file.write("Word, Lemma, Pos-Tag, Ner-Tag\n")
for a, b, c, d in list:
    if a == "":
        new_file.write("\n")
    else:
        new_file.write("{0}\t{1}\t{2}\t{3}\n".format(str(a[0]), str(b[0]), str(c[0]), str(d[0])))
new_file.close()
print("Done")


