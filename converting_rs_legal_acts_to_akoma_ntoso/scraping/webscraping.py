import io
import re

f = io.open("RezultatiPretrage.xml", mode="r", encoding="utf-8")
lines = f.read()
#found = lines.find_all("href")
found = [m.start() for m in re.finditer('href', lines)]
#[0, 5, 10, 15]
f.close()
f1 = open("adrese1.txt", "w")
for i in found:
    
    if(lines[i+71]!='"'):
        
        continue
    f1.write(lines[i+6:i+71]+"\n")
f1.close()
