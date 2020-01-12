from io import open


file = open("dataset.csv", "r", encoding="utf-8")
alltypes = set()
next(file)
for line in file:
    alltypes.add(line.split(";")[1].strip())

new_file = open("enum.txt", "w", encoding="utf-8")

for b in alltypes:
    new_file.write("{0}\n".format(b))
