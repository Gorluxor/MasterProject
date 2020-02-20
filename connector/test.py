#!/usr/bin/env python3
import subprocess
import sys
import os
import io
from _signal import CTRL_BREAK_EVENT

#python3_command = "python2 ..\\reldi-tagger-master\\tagger.py sr -l"  # launch your python2 script using bash

#process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE, stdin=subprocess.)
#process = subprocess.Popen(python3_command.split(), shell=True, stdout=sys.stdout, stdin=subprocess.PIPE, stderr=sys.stdout, bufsize=1, universal_newlines=True, encoding='utf-8')
# process = os.popen(python3_command) #RADI
# # process.stdin.write('\nOvo\nje\nNesto\n.\n')
# # #process.stdin.close()
# # process.stdin.close()
# # process.write('Ovo\nje\nnesto\n.')
# # process.write(chr(28))
#
# instream, output = os.popen2('ls -la')
# instream.write(b'Ovo\nje\nnesto\n.')
# ovo = chr(28)
# instream.write(str.encode(ovo))
# print(output.read())
#
#
# print(process.read()) #RADI
# while process.returncode is None:
#     try:
#         output = process.stdout.read()
#         print(output)
#     except:
#         process.poll()

# #poruka = "\nOvo\nje\nNesto\n.\n" + chr(28) + "\n" #+ chr(28) + "\n"
# #
# process.stdin.write("Ovo\n")
# process.stdin.write("je\n")
# process.stdin.write("nesto\n")
# process.stdin.write(".\n")
# process.stdin.close()
# process.stdin.close(False)
#
#
# output, error = process.communicate()  # receive output from the python2 script
# #output, error = process.communicate()
# # process.send_signal(CTRL_BREAK_EVENT)
# while process.returncode is None:
#     process.poll()
#
# #output = process.stdout.readlines()
# #for line in output:
# # print(output)
# # #test = process.stdout.read()
# for info in output:
#    print(info)
#
# #print(output)
#
# # for line in io.TextIOWrapper(process.stdout, encoding="utf-8"):
# #     print(line)


from fajl import tokenize
from fajl import only_lam
print(tokenize("Ovo je test"))

print(only_lam("radi"))