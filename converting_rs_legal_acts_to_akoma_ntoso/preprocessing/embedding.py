from gensim.utils import simple_preprocess
from nltk.tokenize import sent_tokenize
#from preprocessing.embedding_network import load_model, find_similar
import io
from gensim.models import Word2Vec
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# define training data
def load_sentences(path):
	sentences = []
	words = []
	for i in range(1,3):
		try:
			f = io.open(path + str(i) + ".txt", mode="r", encoding="utf-8")
			stringo = f.read()
			stringo = sent_tokenize(stringo)
			# sentences.append(stringo[0])
			for sentence in range(len(stringo)):
				wordsProcess = simple_preprocess(stringo[sentence])

				pom = ""

				for j in range(len(wordsProcess)):
					pom += wordsProcess[j] + " "

				sentences.append(pom)
				# print(words)
				words.append(wordsProcess)
		except FileNotFoundError:
			continue
	return sentences, words

def load_words(path):
	sentences = []
	words = []
	f = io.open(path, mode="r", encoding="utf-8")
	stringo = f.read().split("\n")
	for i in range(len(stringo)):
		if(stringo[i] == "Član" or ("NOV_ZAKON" in stringo[i])):
			sentences.append(words)
			words = []
			continue
		if(len(stringo[i]) > 3 and not(stringo[i].isdigit())):
			words.append(stringo[i])
	return list(set(words)), sentences

#sentences, words = load_sentences("../data/aktovi_raw_lat/")

#words, sentences = load_words("../data/outputFile.txt")
#words, sentences = load_words("../data/akotovi_raw_lat/1.txt")
sentences, words = load_words("1.txt")
print(words)

model = Word2Vec(sentences,size=150,window=10,min_count=2,workers=10,iter=10)

# model = load_model("", 3)

#most_similar = find_similar(model, "zakon", 10)
#print(most_similar)

vectorizer = TfidfVectorizer()
result = vectorizer.fit_transform(list(sentences))

print(vectorizer.get_feature_names())

print(result)

# get the first vector out (for the first document)
first_vector_tfidfvectorizer = result[0]

# place tf-idf values in a pandas data frame
df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=vectorizer.get_feature_names(), columns=["tfidf"])
df.sort_values(by=["tfidf"], ascending=False)