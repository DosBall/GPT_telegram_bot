#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import config
import string
import re
from nltk.tokenize import word_tokenize
import gensim
from gensim.models import FastText


def make_model(file1, file2, modelname):
    f2 = open(file2, 'a', encoding='utf8')
    start = time.time()
    #necessary_part = {"NOUN", "ADJF", "ADJS", "VERB", "INFN", "PRTF", "PRTS", "GRND"}
    with open(file1, 'r', encoding='utf8') as f:
        #text = f.read().lower().split('\n')
        sentences = []
        masskip = []
        i = 0
        # Normalization
        while True:
            line = f.readline()
            if not line:
                break
            i += 1
            line = line.lower()
            skipp = 0
            for iii in "abcdefghijklmnopqrstuvwxyz":
                if iii in line:
                    skipp = 1
                    break
            if skipp:
                masskip.append(i)
                f2.write("\n")
                continue
            s = ""
            line.replace("-с", "")
            #line.replace("-", "")
            for c in line:
                #if c not in string.punctuation and c not in emoji.EMOJI_DATA:
                if c in string.whitespace or c.isalnum():#c.isalnum() #c.isalpha()
                    s += c
                else:
                    s += ' '
            #sentences.append(text_to_word_sequence(s))
            if len(s) < 10:
                masskip.append(i)
                f2.write("\n")
                continue
            cs = word_tokenize(s)
            if len(cs) < 2:
                masskip.append(i)
                f2.write("\n")
                continue
            sentences.append(cs)
            f2.write(s)


        """
        for i in tqdm(range(len(sentences))):
            sentence = []
            for el in sentences[i]:
                if el in stop_words_r or el in stop_words_k:
                    continue
                #p = morph.parse(el)[0]
                #if p.tag.POS in necessary_part:
                #    sentence.append(p.normal_form)
                sentence.append(stemmer.stem(el))
            sentences[i] = sentence
        """
        #sentences = [x for x in sentences if x]
        print(len(sentences), sentences[:100])
        time.sleep(3)
        # Training
        #model = gensim.models.FastText(sentences, vector_size=100, window=5, min_count=1)
        #model = gensim.models.FastText(sentences, vector_size=200, window=3, min_count=2, epochs=35)
        #model = gensim.models.FastText(sentences, vector_size=100, window=3, min_count=2, sg=1, epochs=35)
        model = gensim.models.FastText(sentences, vector_size=100, window=3, min_count=2, epochs=35)
        #model.init_sims(replace=True)
        #model.save("model1.model")
        model.save(modelname)
        print(len(model.wv.index_to_key), model.wv.index_to_key[:10])
        #print(model.wv.most_similar("чиловек")[:10])
        #print(model.wv.most_similar("замарозка")[:10])
        #print(model.wv.most_similar("салем")[:10])
        print("Время на обучение: " + str(time.time() - start))
        f2.close()
        return (len(masskip), masskip)


def proverka(mas1, mymodel):
    start = time.time()
    model = gensim.models.FastText.load(mymodel)
    #model = gensim.models.FastText.load_fasttext_format(mymodel)
    #model.init_sims(replace=True)
    for index, word in enumerate(mas1):
        #if word in model.wv:
        #print(word + "      " + str(model.wv.similarity(word, mas2[index])))
        print(word)
        print('----------------')

        for i in model.wv.most_similar(positive=[word], topn=5):
            print(i[0], i[1])

        print("\n")
    print("Время на исправление: " + str(time.time() - start))


mas1 = [
    "Замарозка қойып бере аласыздар ма менде таусылып қалған",
    "Замарозканы койынышы себеби сет устамай жатыр 02.02.24ж-10.02.24ж аралыгына койынышы",
    "Ақша толегенде мартка дейін кіре алмаймыз деп айтқан едім жарайды ақпанның 29на дейін замарозка жасап қойдым деп еді ғой звондаған қыз",
    "А почему у меня тогда в Qalan показывает за прошлый месяц(кэшбек)\n",
    "Мұғалім кешбэк алу үшін ата — анаың қандай нөмірі керек каспи ма? \n",
    "Извините пожалуйста что не делала qalan так долго просто были дела и была очень занята",
    "Салеметсиз бе! Мее кэшбэкты алайын деп едым!  4 сандык кодты  тыркелып турган номерге емес +7 775 884 34 41 деген номерге жыбересыздер",
]


#./fasttext sent2vec -input C:/Users/ITQALAN12/Documents/smart_chat/big_test4.txt -output ft_s2v_model1 -minCount 8 -dim 100 -epoch 10 -lr 0.2 -wordNgrams 2 -loss ns -neg 10 -thread 2 -maxVocabSize 750000

#print(make_model(config.smart_chat + "vect_good_text1.txt", config.smart_chat + "vect_trained_text1.txt", "sentense_bad_model1.bin"))
#proverka(mas1, "sentense_bad_model1.bin")
#proverka(mas1, mas2, "model1.bin")
#proverka(mas1, mas2, "model3.bin")

from sent2vec.vectorizer import Vectorizer
import sent2vec
import numpy as np
from scipy import spatial
import csv
import os
os.environ['TRANSFORMERS_CACHE'] = 'C:/Users/****/gpt_chat/cache/'
os.environ['HF_HOME'] = 'C:/Users/****/gpt_chat/cache/'
#vectorizer1 = Vectorizer()
vectorizer1 = Vectorizer(pretrained_weights='distilbert-base-multilingual-cased', ensemble_method='average')


def mysent2vec(file1, file2, outfile):
    f2 = open(file2, 'a', encoding='utf8')
    start = time.time()
    with open(file1, 'r', encoding='utf8') as f:
        sentences = f.read().lower().split('\n')

    #vectorizer1.run(sentences)
    vectorizer1.run(mas1)
    vectors = vectorizer1.vectors

    dist_1 = spatial.distance.cosine(vectors[0], vectors[1])
    dist_2 = spatial.distance.cosine(vectors[0], vectors[3])
    print('dist_1: {0}, dist_2: {1}'.format(dist_1, dist_2))
    #print(sentences[:10])
    #print(vectors[:2])

    header1 = ['sentences', 'vectors', 'closest']
    with open(outfile, 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        #writer.writerow(header1)
        data1 = []
        for sens, vecs in zip(sentences, vectors):
            data1.append([sens, vecs[0]])
        #writer.writerow(data1)

    #np.save(outfile, vectors)
    #np.savetxt(outfile, vectors, delimiter=",")
    #np.savetxt(outfile, vectors)

    f2.close()
    print("Время: " + str(time.time() - start))
    return 1


#print(mysent2vec(config.smart_chat + "vect_good_text1.txt", config.smart_chat + "vect_trained_text1.txt", 'embeddings1.csv'))


def mysent2vec2(model1):
    model = sent2vec.Sent2vecModel()
    model.load_model(model1)#, inference_mode=True)
    emb = model.embed_sentence("once upon a time .")
    embs = model.embed_sentences(["first sentence .", "another sentence"])


#print(mysent2vec2("sentense_bad_model1.bin"))

'''
import openai
import pandas as pd
openai.api_key = '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'
client = openai.OpenAI()

response = client.embeddings.create(
    input="Your text string goes here",
    model="text-embedding-3-small"
)
print(response.data[0].embedding)

def get_embedding1(file1, model="text-embedding-3-small"):
    f1 = open(file1, "r", encoding="utf-8")
    text = f1.read().split('\n')
    emb = client.embeddings.create(input=[text], model=model).data[0].embedding

    f1.close()
    return


#df['ada_embedding'] = df.combined.apply(lambda x: get_embedding1(x, model='text-embedding-3-small'))
#df.to_csv('output/embedded_1k_reviews.csv', index=False)

#df = pd.read_csv('output/embedded_1k_reviews.csv')
#df['ada_embedding'] = df.ada_embedding.apply(eval).apply(np.array)

'''





