import os
import sys
import subprocess
import io

debug = False


def tokenize(string_data):  # Only to tokenize data
    python2_command_token = "python2 ..\\reldi-tagger-master\\tokeniser\\tokeniser.py sr --file ..\\sub\\tokenize.txt"

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
    relative_file = "-f ..\\sub\\{}".format(data_file)
    python2_command = "python2 ..\\reldi-tagger-master\\tagger.py sr -l {}".format(relative_file)
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


if __name__ == "__main__":
    #tokenize_pos("Ovo je nesto sto bi trebalo biti tokenizovani. Ali pitanje je da li ce andrija primetiti nesto. Da je ...")
    #pos_lem('text.txt')
    print(only_lam("Ovo je nesto sto bi trebalo raditi."))
