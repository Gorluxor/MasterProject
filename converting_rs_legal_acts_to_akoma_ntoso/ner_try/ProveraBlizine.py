# Requires: FastText Model https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.sh.300.bin.gz
# Creates from Word -> Vector , word2vec from fasttext
import fasttext.util
import math
def proveriRazliku(fastText,rec1,rec2):
    lupa_sr = fastText.get_word_vector(rec1.lower())
    lupa_hr = fastText.get_word_vector(rec2.lower())


    #print(lupa_sr)
    #print(lupa_hr)
    lupa = 0
    for i in range(len(lupa_sr)):
        lupa = lupa + math.fabs(math.fabs(lupa_hr[i]) - math.fabs(lupa_sr[i]))
    print("Kvadrat razlika za " + str(rec1) + " i " + str(rec2) + "=" + str(lupa))

filepath = "../../cc.sh.300.bin" # Download: https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.sh.300.bin.gz
print("Start Loading")
ft = fasttext.load_model(filepath)
proveriRazliku(ft,"Lupa","povećalom")
proveriRazliku(ft,"Repriza","Ponovak")
proveriRazliku(ft,"Čovek","Kola")









print("End Loading")


