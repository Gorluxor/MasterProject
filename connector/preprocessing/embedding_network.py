from gensim.models import Word2Vec
from keras.layers import Input, Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
from keras.models import Model
from keras.preprocessing.sequence import pad_sequences

def preprocess_data(train_df, vocab, comments, list_sentences_train):

    word_index = {t[0]: i + 1 for i, t in enumerate(vocab.most_common(50))}
    sequences = [[word_index.get(t, 0) for t in comment]
                 for comment in comments[:len(list_sentences_train)]]
    test_sequences = [[word_index.get(t, 0) for t in comment]
                      for comment in comments[len(list_sentences_train):]]

    # pad
    data = pad_sequences(sequences, maxlen=20,
                         padding="pre", truncating="post")
    list_classes = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
    y = train_df[list_classes].values

    test_data = pad_sequences(test_sequences, maxlen=20, padding="pre",
                              truncating="post")
    return data, test_data,y

def embedding_model(input_size, dimension = 3, word_dimension = 50, output_size = 5):
    input = Input(shape=(input_size,), dtype='float32')
    encoder = Embedding(input_size, word_dimension, input_length=dimension, trainable=True)(input)
    bigram_conv = Conv1D(filters=10, kernel_size=2, padding='valid', activation='relu', strides=1)(encoder)
    bigram_pooling = GlobalMaxPooling1D()(bigram_conv)
    flatten = Dense(30, activation='relu')(bigram_pooling)
    dropout = Dropout(0.2)(flatten)
    out = Dense(input_size, activation='softmax')(dropout)
    model = Model(inputs=input, outputs=out)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def fit(model, data, y):
     model.fit([data], y, validation_split=0.1, epochs=10, batch_size=256, shuffle=True)
     return model

def load_model(path, window_size = 1):
    model = Word2Vec.load('embedding_models/model' + str(window_size) + '.bin')
    return model

def find_similar(model , word, number_of_samples):
    return model.wv.most_similar(positive=[word], topn=number_of_samples)

def tf_idf(sentences):
    print(sentences)

    # vectorizer = TfidfVectorizer()
    # result = vectorizer.fit_transform(list(sentences))

    # print(vectorizer.get_feature_names())
    #
    # print(result)

    # get the first vector out (for the first document)
    # first_vector_tfidfvectorizer = result[0]

    # place tf-idf values in a pandas data frame
    # df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=vectorizer.get_feature_names(),
    # 				  columns=["tfidf"])
    # df.sort_values(by=["tfidf"], ascending=False)