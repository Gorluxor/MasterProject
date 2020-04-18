import pickle
try:
    import Akoma
    from Akoma.named_enitity_recognition.readutils import SentenceGetter, word2features, read_and_prepare_csv, \
        sent2features, sent2labels, sent2tokens
    from Akoma.connector.connector import tokenize_pos
    from Akoma.named_enitity_recognition.readutils import SentenceGetter, word2features, read_and_prepare_csv, \
        sent2features, sent2labels, sent2tokens
except ModuleNotFoundError as sureError:
    try:
        from named_enitity_recognition.readutils import SentenceGetter, word2features, read_and_prepare_csv, \
            sent2features, sent2labels, sent2tokens
        from connector.connector import tokenize_pos
        from named_enitity_recognition.readutils import SentenceGetter, word2features, read_and_prepare_csv, \
            sent2features, sent2labels, sent2tokens
    except ModuleNotFoundError as newError:
        if not sureError.name == "Akoma" or not newError.name == "Akoma":
            print(newError)
            print("Error")
            exit(-1)

import  os

def do_ner_on_sentence(sentence):
    # sentence = tokenize_pos("Престали су да важе (види члан 80. Закона - 104/2016-34)")
    w = tokenize_pos(sentence)
    df = [(x, y) for x, y, z in tokenize_pos(w)]

    X = [sent2features(df)]
    X_test = X

    filename = 'data/ner/modelReldiD.sav'
    #ROOT_DIR = os.path.dirname(os.path.basename(__file__))
    #filename = ROOT_DIR + "/data/ner/modelReldiD.sav"

    crf = loaded_model = pickle.load(open(filename, 'rb'))
    y_pred = crf.predict(X_test)

    # print("Overall: ", str(y_pred))
    return y_pred