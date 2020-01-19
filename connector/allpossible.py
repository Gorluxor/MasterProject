from io import open


file = open("datasetDrugi.csv", "r", encoding="utf-8")
alltypes = set()
next(file)
for line in file:
    if line.__len__() > 1:
        dat = line.split("\t")
        info = dat[3].strip()
        alltypes.add(info)

new_file = open("enumDrugi.txt", "w", encoding="utf-8")

for b in alltypes:
    new_file.write("{0}\n".format(b))
