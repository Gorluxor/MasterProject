import subprocess

debug = False


def tokenize(string_data):  # Only to tokenize data
    # noinspection SpellCheckingInspection,SpellCheckingInspection
    python2_command_token = "python2 ..\\reldi-tagger\\tokeniser\\tokeniser.py sr --file ..\\connector\\tokenize.txt"

    to_file("tokenize.txt", string_data)

    process = subprocess.Popen(python2_command_token.split(), stdout=subprocess.PIPE, bufsize=1, universal_newlines=True, encoding='utf-8')

    output, error = process.communicate()

    lines = output.split('\n')

    info = [s.split('\t') for s in lines if s.strip() != '']
    if debug:
        print(output)
        print(info)
    return info


def pos_lem(data_file):  # POS and Lam
    relative_file = "-f ..\\connector\\{}".format(data_file)
    # noinspection SpellCheckingInspection
    python2_command = "python2 ..\\reldi-tagger\\tagger.py sr -l {}".format(relative_file)
    print(python2_command)
    process = subprocess.Popen(python2_command.split(), stdout=subprocess.PIPE, bufsize=1, universal_newlines=True,
                               encoding='utf-8')

    output, error = process.communicate()
    if debug:
        print(output)

    lines = output.split('\n')

    info = [s.split('\t') for s in lines if s.strip() != '']
    if debug:
        print(info)
    return info


def to_file(filename, content):
    f = open(filename, "w+", encoding='utf-8')
    f.write(content)
    f.write("\n\n")
    f.close()


def tokenize_pos(string_data):
    info = tokenize(string_data)
    to_file('text.txt', "\n".join(s[1] for s in info))
    pos_info = pos_lem('text.txt')
    if debug:
        print(pos_info)
    return pos_info


def only_lam(string_data):
    info = tokenize_pos(string_data)
    return [s[2] for s in info]


def listToString(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for i in range(0, len(s)):
        if s[i] == ".":
            str1 += s[i] + "\n"
        else:
            if (s[i] == "član" or s[i] == "члан") and '.' in s[i+1]:
              str1 += "\n" + s[i] + " "
            else:
                if "." in s[i]:
                    if checkIfRomanNumeral(s[i].replace('.','')):
                        str1 += "\n" + s[i] + " "
                    else:
                        str1 += s[i] + " "
                else:
                    str1 += s[i] + " "
        # return string
    return str1


def checkIfRomanNumeral(numeral):
    numeral = {c for c in numeral.upper()}
    validRomanNumerals = {c for c in "MDCLXVI()"}
    return not numeral - validRomanNumerals


# noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection
if __name__ == "__main__":
    #tokenize_pos("Ovo je nesto sto bi trebalo biti tokenizovani. Ali pitanje je da li ce andrija primetiti nesto. Da je ...")
    #pos_lem('text.txt')
    # noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection

    #vrati = only_lam("Vudu magija je nesto sto bi trebalo raditi.")
    sanityCheck = only_lam('Жабци \n')
    sanityCheckLat = only_lam("Žabci \n")

    if sanityCheck.__len__() !=1 and sanityCheckLat.__len__() != 1:
        print("ReLDI library failed")
        exit(-1)

    from os import listdir
    from os import path
    from os.path import isfile, join

    basePath = path.dirname(__file__)
    # noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection
    filePath = path.abspath(path.join(basePath, "..","converting_rs_legal_acts_to_akoma_ntoso","data", "aktovi_raw_lat"))
    fileOut = path.abspath(path.join(basePath, "out"))
    # noinspection SpellCheckingInspection
    filenames = [f for f in listdir(filePath) if isfile(join(filePath, f))]
    # noinspection SpellCheckingInspection
    extens = ".txt"
    for filename in filenames:
        check = path.join(filePath, filename);
        # noinspection SpellCheckingInspection
        outputApsolute = path.join(fileOut, filename);
        file = open(check, encoding="utf8")
        outputFile = open(outputApsolute, mode="w+", encoding="utf8")
        textToSend = file.read()
        list_lem = only_lam(textToSend)
        listToStr = listToString(list_lem)
        outputFile.write(listToStr)
        outputFile.flush()
        file.close()
        outputFile.close()


