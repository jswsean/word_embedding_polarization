# Script to train Doc2Vec model on party_congress_topic metadata indicators.
# Adapted from Rheault & Cochrane (2020).

import gensim
from gensim.models.doc2vec import Doc2Vec
from gensim.models.phrases import Phrases, Phraser
from collections import namedtuple
import logging
import re

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
assert gensim.models.doc2vec.FAST_VERSION > -1

class corpusIterator(object):

    def __init__(self, inpath, house, bigram=None, trigram=None):
        if bigram:
            self.bigram = bigram
        else:
            self.bigram = None
        if trigram:
            self.trigram = trigram
        else:
            self.trigram = None
        self.house = house
        self.inpath = inpath

    def __iter__(self):
        self.speeches = namedtuple('speeches', 'words tags')
        with open(self.inpath, 'r') as f:
            for line in f:
                ls = line.split('\t')
                chamber = ls[4]
                if chamber==self.house:
                    text = ls[9].replace('\n','')
                    congress = str(ls[0])
                    party = ls[6]

                    # ------------------------------------------
                    # IMMIGRATION TOPICS
                    # ------------------------------------------
                    # Republicans
                    match = re.search(r'\bimmigr\w*', text, re.IGNORECASE)
                    if (match and party == 'R' and congress == '107'):
                        R_107_immigration = "R_107_immigration"
                    else: 
                        R_107_immigration = "R_107_non_immigration"

                    if (match and party == 'R' and congress == '108'):
                        R_108_immigration = "R_108_immigration"
                    else: 
                        R_108_immigration = "R_108_non_immigration"

                    if (match and party == 'R' and congress == '109'):
                        R_109_immigration = "R_109_immigration"
                    else: 
                        R_109_immigration = "R_109_non_immigration"

                    if (match and party == 'R' and congress == '110'):
                        R_110_immigration = "R_110_immigration"
                    else: 
                        R_110_immigration = "R_110_non_immigration"

                    if (match and party == 'R' and congress == '111'):
                        R_111_immigration = "R_111_immigration"
                    else: 
                        R_111_immigration = "R_111_non_immigration"

                    if (match and party == 'R' and congress == '112'):
                        R_112_immigration = "R_112_immigration"
                    else: 
                        R_112_immigration = "R_112_non_immigration"

                    if (match and party == 'R' and congress == '113'):
                        R_113_immigration = "R_113_immigration"
                    else: 
                        R_113_immigration = "R_113_non_immigration"

                    if (match and party == 'R' and congress == '114'):
                        R_114_immigration = "R_114_immigration"
                    else: 
                        R_114_immigration = "R_114_non_immigration"


                    # Democrats
                    if (match and party == 'D' and congress == '107'):
                        D_107_immigration = "D_107_immigration"
                    else: 
                        D_107_immigration = "D_107_non_immigration"

                    if (match and party == 'D' and congress == '108'):
                        D_108_immigration = "D_108_immigration"
                    else: 
                        D_108_immigration = "D_108_non_immigration"

                    if (match and party == 'D' and congress == '109'):
                        D_109_immigration = "D_109_immigration"
                    else: 
                        D_109_immigration = "D_109_non_immigration"

                    if (match and party == 'D' and congress == '110'):
                        D_110_immigration = "D_110_immigration"
                    else: 
                        D_110_immigration = "D_110_non_immigration"

                    if (match and party == 'D' and congress == '111'):
                        D_111_immigration = "D_111_immigration"
                    else: 
                        D_111_immigration = "D_111_non_immigration"

                    if (match and party == 'D' and congress == '112'):
                        D_112_immigration = "D_112_immigration"
                    else: 
                        D_112_immigration = "D_112_non_immigration"

                    if (match and party == 'D' and congress == '113'):
                        D_113_immigration = "D_113_immigration"
                    else: 
                        D_113_immigration = "D_113_non_immigration"

                    if (match and party == 'D' and congress == '114'):
                        D_114_immigration = "D_114_immigration"
                    else: 
                        D_114_immigration = "D_114_non_immigration"




                    # ------------------------------------------
                    # ABORTION TOPICS
                    # ------------------------------------------
                    # Republicans
                    match = re.search(r'\b(abortion\w*|reproducti\w*)', text, re.IGNORECASE)
                    if (match and party == 'R' and congress == '107'):
                        R_107_abortion = "R_107_abortion"
                    else: 
                        R_107_abortion = "R_107_non_abortion"

                    if (match and party == 'R' and congress == '108'):
                        R_108_abortion = "R_108_abortion"
                    else: 
                        R_108_abortion = "R_108_non_abortion"

                    if (match and party == 'R' and congress == '109'):
                        R_109_abortion = "R_109_abortion"
                    else: 
                        R_109_abortion = "R_109_non_abortion"

                    if (match and party == 'R' and congress == '110'):
                        R_110_abortion = "R_110_abortion"
                    else: 
                        R_110_abortion = "R_110_non_abortion"

                    if (match and party == 'R' and congress == '111'):
                        R_111_abortion = "R_111_abortion"
                    else: 
                        R_111_abortion = "R_111_non_abortion"

                    if (match and party == 'R' and congress == '112'):
                        R_112_abortion = "R_112_abortion"
                    else: 
                        R_112_abortion = "R_112_non_abortion"

                    if (match and party == 'R' and congress == '113'):
                        R_113_abortion = "R_113_abortion"
                    else: 
                        R_113_abortion = "R_113_non_abortion"

                    if (match and party == 'R' and congress == '114'):
                        R_114_abortion = "R_114_abortion"
                    else: 
                        R_114_abortion = "R_114_non_abortion"


                    # Democrats
                    if (match and party == 'D' and congress == '107'):
                        D_107_abortion = "D_107_abortion"
                    else: 
                        D_107_abortion = "D_107_non_abortion"

                    if (match and party == 'D' and congress == '108'):
                        D_108_abortion = "D_108_abortion"
                    else: 
                        D_108_abortion = "D_108_non_abortion"

                    if (match and party == 'D' and congress == '109'):
                        D_109_abortion = "D_109_abortion"
                    else: 
                        D_109_abortion = "D_109_non_abortion"

                    if (match and party == 'D' and congress == '110'):
                        D_110_abortion = "D_110_abortion"
                    else: 
                        D_110_abortion = "D_110_non_abortion"

                    if (match and party == 'D' and congress == '111'):
                        D_111_abortion = "D_111_abortion"
                    else: 
                        D_111_abortion = "D_111_non_abortion"

                    if (match and party == 'D' and congress == '112'):
                        D_112_abortion = "D_112_abortion"
                    else: 
                        D_112_abortion = "D_112_non_abortion"

                    if (match and party == 'D' and congress == '113'):
                        D_113_abortion = "D_113_abortion"
                    else: 
                        D_113_abortion = "D_113_non_abortion"

                    if (match and party == 'D' and congress == '114'):
                        D_114_abortion = "D_114_abortion"
                    else: 
                        D_114_abortion = "D_114_non_abortion"


                    # ------------------------------------------
                    # GUN TOPICS
                    # ------------------------------------------
                    # Republicans
                    match = re.search(r'\b(guns?|firearms?)\b', text, re.IGNORECASE)
                    if (match and party == 'R' and congress == '107'):
                        R_107_guns = "R_107_guns"
                    else: 
                        R_107_guns = "R_107_non_guns"

                    if (match and party == 'R' and congress == '108'):
                        R_108_guns = "R_108_guns"
                    else: 
                        R_108_guns = "R_108_non_guns"

                    if (match and party == 'R' and congress == '109'):
                        R_109_guns = "R_109_guns"
                    else: 
                        R_109_guns = "R_109_non_guns"

                    if (match and party == 'R' and congress == '110'):
                        R_110_guns = "R_110_guns"
                    else: 
                        R_110_guns = "R_110_non_guns"

                    if (match and party == 'R' and congress == '111'):
                        R_111_guns = "R_111_guns"
                    else: 
                        R_111_guns = "R_111_non_guns"

                    if (match and party == 'R' and congress == '112'):
                        R_112_guns = "R_112_guns"
                    else: 
                        R_112_guns = "R_112_non_guns"

                    if (match and party == 'R' and congress == '113'):
                        R_113_guns = "R_113_guns"
                    else: 
                        R_113_guns = "R_113_non_guns"

                    if (match and party == 'R' and congress == '114'):
                        R_114_guns = "R_114_guns"
                    else: 
                        R_114_guns = "R_114_non_guns"


                    # Democrats
                    if (match and party == 'D' and congress == '107'):
                        D_107_guns = "D_107_guns"
                    else: 
                        D_107_guns = "D_107_non_guns"

                    if (match and party == 'D' and congress == '108'):
                        D_108_guns = "D_108_guns"
                    else: 
                        D_108_guns = "D_108_non_guns"

                    if (match and party == 'D' and congress == '109'):
                        D_109_guns = "D_109_guns"
                    else: 
                        D_109_guns = "D_109_non_guns"

                    if (match and party == 'D' and congress == '110'):
                        D_110_guns = "D_110_guns"
                    else: 
                        D_110_guns = "D_110_non_guns"

                    if (match and party == 'D' and congress == '111'):
                        D_111_guns = "D_111_guns"
                    else: 
                        D_111_guns = "D_111_non_guns"

                    if (match and party == 'D' and congress == '112'):
                        D_112_guns = "D_112_guns"
                    else: 
                        D_112_guns = "D_112_non_guns"

                    if (match and party == 'D' and congress == '113'):
                        D_113_guns = "D_113_guns"
                    else: 
                        D_113_guns = "D_113_non_guns"

                    if (match and party == 'D' and congress == '114'):
                        D_114_guns = "D_114_guns"
                    else: 
                        D_114_guns = "D_114_non_guns"




                    # ------------------------------------------
                    # CLIMATE CHANGE TOPICS
                    # ------------------------------------------
                    # Republicans
                    match = re.search(r'\b(climate change|emission|global warming|climate)\b', 
                                      text, re.IGNORECASE)
                    if (match and party == 'R' and congress == '107'):
                        R_107_climate = "R_107_climate"
                    else: 
                        R_107_climate = "R_107_non_climate"

                    if (match and party == 'R' and congress == '108'):
                        R_108_climate = "R_108_climate"
                    else: 
                        R_108_climate = "R_108_non_climate"

                    if (match and party == 'R' and congress == '109'):
                        R_109_climate = "R_109_climate"
                    else: 
                        R_109_climate = "R_109_non_climate"

                    if (match and party == 'R' and congress == '110'):
                        R_110_climate = "R_110_climate"
                    else: 
                        R_110_climate = "R_110_non_climate"

                    if (match and party == 'R' and congress == '111'):
                        R_111_climate = "R_111_climate"
                    else: 
                        R_111_climate = "R_111_non_climate"

                    if (match and party == 'R' and congress == '112'):
                        R_112_climate = "R_112_climate"
                    else: 
                        R_112_climate = "R_112_non_climate"

                    if (match and party == 'R' and congress == '113'):
                        R_113_climate = "R_113_climate"
                    else: 
                        R_113_climate = "R_113_non_climate"

                    if (match and party == 'R' and congress == '114'):
                        R_114_climate = "R_114_climate"
                    else: 
                        R_114_climate = "R_114_non_climate"


                    # Democrats
                    if (match and party == 'D' and congress == '107'):
                        D_107_climate = "D_107_climate"
                    else: 
                        D_107_climate = "D_107_non_climate"

                    if (match and party == 'D' and congress == '108'):
                        D_108_climate = "D_108_climate"
                    else: 
                        D_108_climate = "D_108_non_climate"

                    if (match and party == 'D' and congress == '109'):
                        D_109_climate = "D_109_climate"
                    else: 
                        D_109_climate = "D_109_non_climate"

                    if (match and party == 'D' and congress == '110'):
                        D_110_climate = "D_110_climate"
                    else: 
                        D_110_climate = "D_110_non_climate"

                    if (match and party == 'D' and congress == '111'):
                        D_111_climate = "D_111_climate"
                    else: 
                        D_111_climate = "D_111_non_climate"

                    if (match and party == 'D' and congress == '112'):
                        D_112_climate = "D_112_climate"
                    else: 
                        D_112_climate = "D_112_non_climate"

                    if (match and party == 'D' and congress == '113'):
                        D_113_climate = "D_113_climate"
                    else: 
                        D_113_climate = "D_113_non_climate"

                    if (match and party == 'D' and congress == '114'):
                        D_114_climate = "D_114_climate"
                    else: 
                        D_114_climate = "D_114_non_climate"




                    # ------------------------------------------
                    # TAXATION TOPICS
                    # ------------------------------------------
                    # Republicans
                    match = re.search(r'\b(tax|taxes|taxation)\b', 
                                      text, re.IGNORECASE)
                    if (match and party == 'R' and congress == '107'):
                        R_107_tax = "R_107_tax"
                    else: 
                        R_107_tax = "R_107_non_tax"

                    if (match and party == 'R' and congress == '108'):
                        R_108_tax = "R_108_tax"
                    else: 
                        R_108_tax = "R_108_non_tax"

                    if (match and party == 'R' and congress == '109'):
                        R_109_tax = "R_109_tax"
                    else: 
                        R_109_tax = "R_109_non_tax"

                    if (match and party == 'R' and congress == '110'):
                        R_110_tax = "R_110_tax"
                    else: 
                        R_110_tax = "R_110_non_tax"

                    if (match and party == 'R' and congress == '111'):
                        R_111_tax = "R_111_tax"
                    else: 
                        R_111_tax = "R_111_non_tax"

                    if (match and party == 'R' and congress == '112'):
                        R_112_tax = "R_112_tax"
                    else: 
                        R_112_tax = "R_112_non_tax"

                    if (match and party == 'R' and congress == '113'):
                        R_113_tax = "R_113_tax"
                    else: 
                        R_113_tax = "R_113_non_tax"

                    if (match and party == 'R' and congress == '114'):
                        R_114_tax = "R_114_tax"
                    else: 
                        R_114_tax = "R_114_non_tax"


                    # Democrats
                    if (match and party == 'D' and congress == '107'):
                        D_107_tax = "D_107_tax"
                    else: 
                        D_107_tax = "D_107_non_tax"

                    if (match and party == 'D' and congress == '108'):
                        D_108_tax = "D_108_tax"
                    else: 
                        D_108_tax = "D_108_non_tax"

                    if (match and party == 'D' and congress == '109'):
                        D_109_tax = "D_109_tax"
                    else: 
                        D_109_tax = "D_109_non_tax"

                    if (match and party == 'D' and congress == '110'):
                        D_110_tax = "D_110_tax"
                    else: 
                        D_110_tax = "D_110_non_tax"

                    if (match and party == 'D' and congress == '111'):
                        D_111_tax = "D_111_tax"
                    else: 
                        D_111_tax = "D_111_non_tax"

                    if (match and party == 'D' and congress == '112'):
                        D_112_tax = "D_112_tax"
                    else: 
                        D_112_tax = "D_112_non_tax"

                    if (match and party == 'D' and congress == '113'):
                        D_113_tax = "D_113_tax"
                    else: 
                        D_113_tax = "D_113_non_tax"

                    if (match and party == 'D' and congress == '114'):
                        D_114_tax = "D_114_tax"
                    else: 
                        D_114_tax = "D_114_non_tax"




                    # ------------------------------------------
                    # RACIAL JUSTICE TOPICS
                    # ------------------------------------------
                    # Republicans
                    match = re.search(r'\b(race|minority|people color|racism|racist|racial)\b', 
                                      text, re.IGNORECASE)
                    if (match and party == 'R' and congress == '107'):
                        R_107_race = "R_107_race"
                    else: 
                        R_107_race = "R_107_non_race"

                    if (match and party == 'R' and congress == '108'):
                        R_108_race = "R_108_race"
                    else: 
                        R_108_race = "R_108_non_race"

                    if (match and party == 'R' and congress == '109'):
                        R_109_race = "R_109_race"
                    else: 
                        R_109_race = "R_109_non_race"

                    if (match and party == 'R' and congress == '110'):
                        R_110_race = "R_110_race"
                    else: 
                        R_110_race = "R_110_non_race"

                    if (match and party == 'R' and congress == '111'):
                        R_111_race = "R_111_race"
                    else: 
                        R_111_race = "R_111_non_race"

                    if (match and party == 'R' and congress == '112'):
                        R_112_race = "R_112_race"
                    else: 
                        R_112_race = "R_112_non_race"

                    if (match and party == 'R' and congress == '113'):
                        R_113_race = "R_113_race"
                    else: 
                        R_113_race = "R_113_non_race"

                    if (match and party == 'R' and congress == '114'):
                        R_114_race = "R_114_race"
                    else: 
                        R_114_race = "R_114_non_race"


                    # Democrats
                    if (match and party == 'D' and congress == '107'):
                        D_107_race = "D_107_race"
                    else: 
                        D_107_race = "D_107_non_race"

                    if (match and party == 'D' and congress == '108'):
                        D_108_race = "D_108_race"
                    else: 
                        D_108_race = "D_108_non_race"

                    if (match and party == 'D' and congress == '109'):
                        D_109_race = "D_109_race"
                    else: 
                        D_109_race = "D_109_non_race"

                    if (match and party == 'D' and congress == '110'):
                        D_110_race = "D_110_race"
                    else: 
                        D_110_race = "D_110_non_race"

                    if (match and party == 'D' and congress == '111'):
                        D_111_race = "D_111_race"
                    else: 
                        D_111_race = "D_111_non_race"

                    if (match and party == 'D' and congress == '112'):
                        D_112_race = "D_112_race"
                    else: 
                        D_112_race = "D_112_non_race"

                    if (match and party == 'D' and congress == '113'):
                        D_113_race = "D_113_race"
                    else: 
                        D_113_race = "D_113_non_race"

                    if (match and party == 'D' and congress == '114'):
                        D_114_race = "D_114_race"
                    else: 
                        D_114_race = "D_114_non_race"
                    
                    tokens = text.split()
                    if self.bigram and self.trigram:
                        self.words = self.trigram[self.bigram[tokens]]
                    elif self.bigram and not self.trigram:
                        self.words = self.bigram[tokens]
                    else:
                        self.words = tokens
                    self.tags = [

                        R_107_immigration, R_108_immigration, R_109_immigration, 
                            R_110_immigration, R_111_immigration, R_112_immigration, 
                            R_113_immigration, R_114_immigration,
                        D_107_immigration, D_108_immigration, D_109_immigration, 
                            D_110_immigration, D_111_immigration, D_112_immigration, 
                            D_113_immigration, D_114_immigration,

                        R_107_abortion, R_108_abortion, R_109_abortion, 
                            R_110_abortion, R_111_abortion, R_112_abortion, 
                            R_113_abortion, R_114_abortion,
                        D_107_abortion, D_108_abortion, D_109_abortion, 
                            D_110_abortion, D_111_abortion, D_112_abortion, 
                            D_113_abortion, D_114_abortion,

                        R_107_guns, R_108_guns, R_109_guns, 
                            R_110_guns, R_111_guns, R_112_guns, 
                            R_113_guns, R_114_guns,
                        D_107_guns, D_108_guns, D_109_guns, 
                            D_110_guns, D_111_guns, D_112_guns, 
                            D_113_guns, D_114_guns,

                        R_107_climate, R_108_climate, R_109_climate, 
                            R_110_climate, R_111_climate, R_112_climate, 
                            R_113_climate, R_114_climate,
                        D_107_climate, D_108_climate, D_109_climate, 
                            D_110_climate, D_111_climate, D_112_climate, 
                            D_113_climate, D_114_climate,

                        R_107_tax, R_108_tax, R_109_tax, 
                            R_110_tax, R_111_tax, R_112_tax, 
                            R_113_tax, R_114_tax,
                        D_107_tax, D_108_tax, D_109_tax, 
                            D_110_tax, D_111_tax, D_112_tax, 
                            D_113_tax, D_114_tax,

                        R_107_race, R_108_race, R_109_race, 
                            R_110_race, R_111_race, R_112_race, 
                            R_113_race, R_114_race,
                        D_107_race, D_108_race, D_109_race, 
                            D_110_race, D_111_race, D_112_race, 
                            D_113_race, D_114_race
                    ]
                    yield self.speeches(self.words, self.tags)

class phraseIterator(object):

    def __init__(self, inpath, house):
        self.inpath = inpath
        self.house = house

    def __iter__(self):
        with open(self.inpath, 'r') as f:
            for line in f:
                ls = line.split('\t')
                chamber = ls[4]
                if chamber==self.house:
                    text = ls[9].replace('\n','')
                    yield text.split()

if __name__=='__main__':

    # Fill in the paths to desired location.
    # Corpus is expected to be in tab-separated format with column ordering specified in
    # reformat_congress.py, and clean text in column #10.

    inpath = '2_build/preprocessed_congress.txt'
    savepath = '2_build/'

    phrases = Phrases(phraseIterator(inpath, house='S'))
    bigram = Phraser(phrases)
    tphrases = Phrases(bigram[phraseIterator(inpath, house='S')])
    trigram = Phraser(tphrases)

    # To save phraser objects for future usage.
    # bigram.save('.../phraser_bigrams')
    # trigram.save('.../phraser_trigrams')

    model0 = Doc2Vec(vector_size=300, window=20, min_count=50, workers=8, epochs=15)
    model0.build_vocab(corpusIterator(inpath, house='H', bigram=bigram, trigram=trigram))
    model0.train(corpusIterator(inpath, house='H', bigram=bigram, trigram=trigram), total_examples=model0.corpus_count, epochs=model0.epochs)
    model0.save(savepath + 'house')
