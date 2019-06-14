import re  # For preprocessing
import pandas as pd  # For data handling
from time import time  # To time our operations
from collections import defaultdict  # For word frequency
import spacy  # For preprocessing
import logging  # Setting up the loggings to monitor gensim
import os
from gensim.models.phrases import Phrases, Phraser
import multiprocessing
from gensim.models import Word2Vec

logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)
df = pd.read_csv('descriptions.txt', sep = '\n', names = ['description'])

#df = df.dropna().reset_index(drop=True)
#df.isnull().sum()

nlp = spacy.load('en', disable=['ner', 'parser']) # disabling Named Entity Recognition for speed

def cleaning(doc):
    # Lemmatizes and removes stopwords
    # doc needs to be a spacy Doc object
    txt = [token.lemma_ for token in doc if not token.is_stop]
    # Word2Vec uses context words to learn the vector representation of a target word,
    # if a sentence is only one or two words long,
    # the benefit for the training is very small
    if len(txt) > 2:
        return ' '.join(txt)

brief_cleaning = (re.sub("[^A-Za-z']+", ' ', str(row)).lower() for row in df['description'])

t = time()
txt = [cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=5000, n_threads=-1)]
print('Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))

df_clean = pd.DataFrame({'clean': txt})
df_clean = df_clean.dropna().drop_duplicates()
print('Clean datafram shape: ', df_clean.shape)

sent = [row.split() for row in df_clean['clean']]

print("Example row: ")
print(sent[0])

phrases = Phrases(sent, min_count=2, progress_per=10000)
bigram = Phraser(phrases)

sentences = bigram[sent]

word_freq = defaultdict(int)
for sent in sentences:
    for i in sent:
        word_freq[i] += 1
len(word_freq)

test = sorted(word_freq, key=word_freq.get, reverse=True)[:10]
for t in test:
    print(t)

cores = multiprocessing.cpu_count()

w2v_model = Word2Vec(min_count=2, #min number of occurrences
                     window=10, #how far to left or to right to look 
                     size=300,
                     sample=6e-5, 
                     alpha=0.03, 
                     min_alpha=0.0007, 
                     negative=20,
                     workers=cores-1)

# build the vocabulary for the model
t = time()
w2v_model.build_vocab(sentences, progress_per=10000)
print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))


# Train the model
t = time()
w2v_model.train(sentences, total_examples=w2v_model.corpus_count, epochs=500, report_delay=1)
print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))


# Omit this if we plan to further continue training
w2v_model.init_sims(replace=True)

# interesting queries
hospital = w2v_model.wv.most_similar(positive=["hospital"])
print('\nmost similar to hospital: ')
for h in hospital:
    print(h)
print('\nMost similar to breast cancer')
bcancer = w2v_model.wv.most_similar(positive=["breast_cancer"])
for b in bcancer:
    print(b)
print('\n Most similar to mammogram')
mam = w2v_model.wv.most_similar(positive=["mammogram"])
for m in mam:
    print(m)
print('\n Most similar to Cancer')
cancer = w2v_model.wv.most_similar(positive=['cancer'])
for c in cancer:
    print(c)

sim = w2v_model.wv.similarity('breast', 'cancer')
print('\n Similarity of breast and cancer: ', sim)

ooo = w2v_model.wv.doesnt_match(['nurse', 'patient', 'skin'])
print('\nOdd one out of nurse, patient and hospital: ', ooo)

w2v_model.save("descriptionW2V.model")







