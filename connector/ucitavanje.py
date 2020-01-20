data_file = open("NER\\hr500k.conll", "r", encoding="utf-8")
#data_file = open("NER\\dev_ner.conllu", "r", encoding="utf-8")
list = []
write_next = True
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
    # possplit = split[3] #drugi
    # possplit = split[4]  #reldi
    # tagsplit = split[9]  #drugi
    # tagsplit = split[10]  #reldi

    possplit = split[4]  # hr500k
    tagsplit = split[10]  # hr500k


    t = (wordsplit.rsplit(), lemmasplit.rsplit(), possplit.rsplit(), tagsplit.rsplit())
    # if not list.__contains__(t):
    list.append(t)
    # except:
    #    print(line.strip())  # if this comes to show, it means there was a error

i = 1
new_file = open("datasetHr.csv", "w+", encoding="utf-8")  # reldi
# new_file = open("datasetDrugi.csv", "w+", encoding="utf-8") # drugi
new_file.write("Sentence #\tWord\tPos\tTag\n")
for a, b, c, d in list:
    if a == "":
        write_next = True
        i = i + 1
    else:
        if write_next:
            write_next = False
            new_file.write("Sentence: {3}\t{0}\t{1}\t{2}\n".format(str(a[0]), str(c[0]), str(d[0]), i))
        else:
            new_file.write("\t{0}\t{1}\t{2}\n".format(str(a[0]), str(c[0]), str(d[0])))
new_file.close()
print("Done")


