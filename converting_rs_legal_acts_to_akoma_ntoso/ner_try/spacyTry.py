# pip install spacy
# python -m spacy download en_core_web_sm
import spacy
# Load MultiLang tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("xx_ent_wiki_sm")
# Process whole documents
text = ("Veliki grb jeste crveni štit na kojem je, između dva zlatna krina u podnožju, dvoglavi srebrni orao, zlatno oružan i istih takvih jezika i nogu, sa crvenim štitom na grudima na kojem je srebrni krst između četiri ista takva ocila bridovima okrenutih ka vertikalnoj gredi krsta. Štit je krunisan zlatnom krunom i zaogrnut porfirom vezenom zlatom, ukrašenom zlatnim resama, uvezanom zlatnim gajtanom sa istim takvim kićankama, postavljenom hermelinom i krunisanom zlatnom krunom. Izgled Malog grba ")
doc = nlp(text)
# Analyze syntax
#print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
#print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)
#print([(w.text, w.pos_) for w in doc])