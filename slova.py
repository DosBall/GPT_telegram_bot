#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import chardet
import config
import string
import re
import pickle
#import emoji
from operator import itemgetter
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import fasttext
import fasttext.util
import enchant
import difflib
from langdetect import detect, DetectorFactory, detect_langs
from scipy import spatial
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter, HashtagFilter, WikiWordFilter, MentionFilter, Filter
fasttext.FastText.eprint = lambda x: None
from textblob.en import Spelling
from Levenshtein import ratio
from transliterate import translit as trans1
from pytils import translit as trans2
from guess_language import guess_language
#from textblob import TextBlob
#import textblob


#fasttext.util.download_model('ru', if_exists='ignore')
#fasttext.util.download_model('kk', if_exists='ignore')
#import pypandoc
#from pypandoc.pandoc_download import download_pandoc
#download_pandoc()

#ft_ru = fasttext.load_model('cc.ru.300.bin')
#ft_kk = fasttext.load_model('cc.kk.300.bin')
lemmatizer = WordNetLemmatizer()
stop_words_r = set(stopwords.words('russian'))
stop_words_k = set(stopwords.words('kazakh'))
stemmer = SnowballStemmer("russian")


def deEmojify(text):
    regrex_pattern = re.compile(pattern="["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'', text)


def slovar(file):
    start = time.time()
    d = {}
    i = 0
    with open(config.smart_chat + file, "r", encoding="utf-8") as f:
        while True:
            s1, s = f.readline().lower(), ""
            if not s1:
                break
            for c in s1:
                #if c not in string.punctuation and c not in emoji.EMOJI_DATA:
                if c in string.whitespace or c.isalnum():
                    s += c
                else:
                    s += ' '
            #s = deEmojify(s)
            cs = word_tokenize(s)
            #print(cs)
            for iii in cs:
                c = stemmer.stem(iii)
                if c in d.keys():
                    d[c] += 1
                else:
                    d[c] = 1
            i += 1
    dd = dict(sorted(d.items(), key=itemgetter(1), reverse=True))
    #dd = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
    print("Время = " + str(time.time() - start))
    return dd


def dict_to_txt(d, file):
    with open(config.smart_chat + file, "a", encoding="utf-8") as f:
        for i in d.keys():
            f.write(str(i) + " " + str(d[i]) + '\n')
    return 1


#d1 = slovar("book.txt")
#d2 = slovar("data1.txt")
#print(dict_to_txt(d1, "slova1.txt"))
'''
start1 = time.time()
word = stemmer.stem('замрозка')
print(word)
#print(ft_ru.get_word_vector('печь')[:10])
print(ft_ru.get_nearest_neighbors(word)[:10])
#print(ft_kk.get_word_vector('мен')[:10])
print(ft_kk.get_nearest_neighbors(word)[:10])

word = stemmer.stem('запчесть')
print(word)
print(ft_ru.get_nearest_neighbors(word)[:10])
print(ft_kk.get_nearest_neighbors(word)[:10])

print("Время " + str(time.time() - start1))
'''
def slovarkz(file1, file2):
    start1 = time.time()
    f1 = open(config.smart_chat + file1, "r", encoding="utf-8")
    f2 = open(config.smart_chat + file2, "a", encoding="utf-8")
    abc = []
    aa = 'а'
    while True:
        s = f1.readline()
        if not s:
            break
        s = s.lower()
        ch = s.find("4")
        if ch > 0 and len(s) >= ch + 3 and s[ch + 2] == "\n":
            aaa = s[ch + 1]
            s = f1.readline()
            s = s.lower()
            if s[0] != aa and s[0] == aaa:
                aa = s[0]
                print(aa)
        if s[0] != aa:
            continue
        t = s.find("\t")
        if t < 0:
            continue
        s = s[:t]
        p = s.find(" ")
        if p >= 0:
            s = s[:p]
        if len(s) <= 2:
            continue
        if s not in abc:
            f2.write(s + "\n")
            abc.append(s)
    f1.close()
    f2.close()
    print("Время " + str(time.time() - start1))
    print(len(abc))


def slovarru(file1, file2):
    start1 = time.time()
    f1 = open(config.smart_chat + file1, "r", encoding="utf-8")
    f2 = open(config.smart_chat + file2, "a", encoding="utf-8")
    abc = []
    no_accent = ['а', 'я', 'у', 'ю', 'о', 'е', 'э', 'и', 'ы']
    accent = ['а́', 'я́', 'у́', 'ю́', 'о́', 'е́', 'э́', 'и́', 'ы́']
    #aa = 'а'
    while True:
        s = f1.readline()
        if not s:
            break
        s = s.lower()
        #if len(s) == 2:
        #    aa = s[0]
        #    print(aa)
        #    continue
        for i in range(len(accent)):
            s = s.replace(accent[i], no_accent[i])
        j = 0
        for b in s:
            if not b.isalpha() and b != '-':
                s = s[:j]
                break
            else:
                j += 1
        if len(s) <= 1:
            continue
        if s not in abc:
            f2.write(s + "\n")
            abc.append(s)
    f1.close()
    f2.close()
    print("Время " + str(time.time() - start1))
    print(len(abc))


#slovarkz("slovar_kz0.txt", "slovar_kz.txt")
#slovarru("slovar_ru0.txt", "slovar_ru.txt")
import gensim
from gensim.models import FastText
from keras.preprocessing.text import text_to_word_sequence
import pymorphy2
from tqdm import tqdm

morph = pymorphy2.MorphAnalyzer()


def make_model(file1="slovar.txt"):
    start = time.time()
    necessary_part = {"NOUN", "ADJF", "ADJS", "VERB", "INFN", "PRTF", "PRTS", "GRND"}
    with open(config.smart_chat + file1, 'r', encoding='utf8') as f:
        #sentences = f.read().split('\n')
        text1 = f.read().lower().replace("\n", ". ")
        split_regex = re.compile(r'[.|!|?|…|;|"|»|«|“|„]')
        text = [t.strip() for t in split_regex.split(text1)]
        #fil = filter(lambda t: t, [t.strip() for t in split_regex.split(text1)])
        sentences = []
        # Normalization
        for line in text:
            s = ""
            line.replace("-с", "")
            line.replace("-", "")
            for c in line:
                #if c not in string.punctuation and c not in emoji.EMOJI_DATA:
                if c in string.whitespace or c.isalpha():#c.isalnum()
                    s += c
                else:
                    s += ' '
            #sentences.append(text_to_word_sequence(s))
            if s == "":
                continue
            cs = word_tokenize(s)
            #ss = []
            #for iii in cs:
            #    ss.append(stemmer.stem(iii))
            if len(cs) > 0:
                sentences.append(cs)
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
        sentences = [x for x in sentences if x]
    print(sentences[:100])
    time.sleep(3)
    # Training
    #model = gensim.models.FastText(sentences, vector_size=100, window=5, min_count=1)
    #model = gensim.models.FastText(sentences, vector_size=200, window=3, min_count=2, epochs=35)
    model = gensim.models.FastText(sentences, vector_size=100, window=3, min_count=2, sg=1, epochs=35)
    #model.init_sims(replace=True)
    #model.save("model1.model")
    model.save("model4.bin")
    print(len(model.wv.index_to_key))
    print(model.wv.most_similar("чиловек")[:10])
    print(model.wv.most_similar("замарозка")[:10])
    print(model.wv.most_similar("салем")[:10])
    print("Время на обучение: " + str(time.time() - start))


def proverka(mas1, mas2, mymodel):
    start = time.time()
    model = gensim.models.FastText.load(mymodel)
    #model = gensim.models.FastText.load_fasttext_format(mymodel)
    #model.init_sims(replace=True)
    for index, word in enumerate(mas1):
        if word in model.wv:
            print(word + "      " + str(model.wv.similarity(word, mas2[index])))
            print('----------------')

            for i in model.wv.most_similar(positive=[word], topn=5):
                print(i[0], i[1])

            print("\n")
    print("Время на исправление: " + str(time.time() - start))


mas1 = ['замарозка', 'замрозка', 'щамарозка', 'челавек',  'стулент', 'студечнеский', 'учениу',
        'бугин', 'bugin', 'men', 'меен', 'мен', 'зделать',  'сматреть', 'алгаритм']
mas2 = ['заморозка', 'заморозка', 'заморозка', 'человек', 'студент', 'студенческий', 'ученик',
        'бүгін', 'бүгін', 'мен', 'мен', 'мен', 'сделать', 'смотреть', 'алгоритм']

#make_model("zhaina.txt")#book.txt
#proverka(mas1, mas2, "model4.bin")
#proverka(mas1, mas2, "model1.bin")
#proverka(mas1, mas2, "model3.bin")


def proverkacc(mas1, mas2):
    start = time.time()
    model_ru = fasttext.load_model("cc.ru.300.bin")
    model_kk = fasttext.load_model("cc.kk.300.bin")
    for index, word in enumerate(mas1):
        lang = str(detect(word))
        if lang == "kk":
            model = model_kk
        else:
            model = model_ru
        if word in model:
            w1 = model.get_word_vector(word)
            w2 = model.get_word_vector(mas2[index])
            print(word + "      " + str(spatial.distance.euclidean(w1, w2)) + lang)
            print('----------------')

            for i in model.get_nearest_neighbors(word, k=5):
                print(i[0], i[1])

            print("\n")
        else:
            print("Слово не найдено в модели: " + word)
    print("Время на исправление: " + str(time.time() - start))


#proverkacc(mas1, mas2)


def zamena(text1, mymodel):
    start = time.time()
    model = gensim.models.FastText.load(mymodel)
    ans = ""
    split_regex = re.compile(r'[.|!|?|…|;|"|»|«|“|„]')
    text = [t.strip() for t in split_regex.split(text1)]
    for line in text:
        line1 = word_tokenize(line)
        for word in line1:
            good = model.wv.most_similar(positive=[word], topn=1)[0]
            ans += str(good[0]) + " "
        ans += ". "
    print("Время на исправление: " + str(time.time() - start))
    return ans


#print(zamena('Саламатсызба ! Дана кеше ауырды , высокая температура . Бугин жасайды тапсырмаларды', "model1.bin"))


def myenchant(lang, str0):
    dic_en = enchant.Dict(lang)
    checker_en = SpellChecker(lang, filters=[EmailFilter, URLFilter, HashtagFilter])
    checker_en.set_text(str0)
    wrong_en = [i.word for i in checker_en]
    print(wrong_en)
    for i1 in wrong_en:
        sim_en = dict()
        sug_en = set(dic_en.suggest(i1))
        for j1 in sug_en:
            measure = difflib.SequenceMatcher(None, i1, j1).ratio()
            sim_en[measure] = j1
        print("Correct word is:", sim_en[max(sim_en.keys())])


#myenchant("en_US", "I have got a new carr and it is ameizing.")
#myenchant("ru_RU", "Я купил новуюю мащину вчера. Здравствуйте, можете паставить мне замрозку на сегодня?")
#myenchant("kk_KZ", "Мен бугін жаңа машинаны сатп алдым. Саламатсыз ба, маган бугин замарозка коясыз ба?")


def zamena1(mas, mymodel):
    start = time.time()
    for i, text in enumerate(mas):
        model = gensim.models.FastText.load(mymodel)
        chkr = SpellChecker("kk_KZ", text.lower())
        for err in chkr:
            word = err.word
            ans = model.wv.most_similar(positive=[word], topn=5)
            if ans[0][1] > 0.9:
                err.replace(str(ans[0][0]))
                print(word + " -> " + str(ans[0][0]) + ", ", ans)
            else:
                print("Замена не найдена: '" + str(word) + "', соседи: " + str(ans))
        mas[i] = str(chkr.get_text())
        print("##orig: " + text)
        print("##zam1: " + str(chkr.get_text()))

    print("Время на исправление: " + str(time.time() - start))
    return mas


def myblob(text, slovar1):
    spelling = Spelling(path=config.smart_chat + slovar1)
    #spelling.train(config.temp_str1(config.smart_chat + "book.txt"), config.smart_chat + "slova1.txt")
    words = text.lower().split()
    #words = word_tokenize(text)
    corrected = " "
    for i in words:
        corrected += " " + spelling.suggest(i)[0][0]# Spell checking word by word
    return(corrected[2:])


#spelling = Spelling(path=config.smart_chat + "slova1.txt")
#spelling.train(config.temp_str1(config.smart_chat + "book.txt"), config.smart_chat + "slova1.txt")
#print(myblob("Мен бугін жаңа машинаны сатп алдым. Саламатсыз ба, маган бугин замарозка коясыз ба?", "slova1.txt"))


from autocorrect import Speller
#from autocorrect.word_count import count_words
#count_words('kkwiki-latest-pages-articles.xml', 'kk')
autospell_ru, autospell_kk = Speller("ru"), Speller("kk")
import langid
model123 = fasttext.load_model('lid.176.ftz')


def whatlang(word):
    lang = str(config.mylang(word))  # по каз символам
    if lang == "en" or lang == "kk":
        return lang
    else:
        # lang = str(detect(word))
        lang = str(guess_language(word))
        # lang = str(textblob.TextBlob(word).detect_language())
        if lang == "ru" or lang == "kk":
            return lang
        else:
            lang = str(model123.predict(word, k=2)[0][1][-2:])
            #if lang in ["kk", "ky", "tr", "uz", "tt", "uk"]:

            #elif lang in ["ru", "uk", "be", "pl", "bg", "mk", "sr", "hr", "bs", "sl", "cs", "sk"]:

            #else:

    return lang


def myautocorrect(text1):
    #start = time.time()
    text2 = word_tokenize(text1)
    errmas, kkmas, rumas = [], [], []
    s = ""
    #print(text1)
    for word in text2:
        #if not word.isalpha():
        if len(word) < 3:
            s += word + " "
            errmas.append(word)
            continue
        lang = whatlang(word)
        # if lang != "en" and word in dzamen.keys(): word = []
        if lang == "kk":
            s += autospell_kk(word) + " "
            kkmas.append(word)
        elif lang == "ru":
            s += autospell_ru(word) + " "
            rumas.append(word)
        else:
            s += autospell_kk(word) + " "
            kkmas.append(word)
            #print("#lang: " + lang + ", word: " + word)
        """
        else:
            newword = ""
            for j in word:
                if j in config.rukkzamena.keys():
                    newword += config.rukkzamena[j]
                else:
                    newword += j
            print("#lang: " + lang + ", word: " + word + ", newword: " + newword)
            s += autospell_kk(newword) + " "
        """
    #print("Err words:", errmas)
    #print("KZ words:", kkmas)
    #print("RU words:", rumas)
    #print("Время: " + str(time.time() - start))
    return(s)


def proverka1(fmas1, fmas2, ii):
    start = time.time()
    pr0, pr1 = 0, 0
    f1, f2 = open(fmas1, "r", encoding="utf-8"), open(fmas2, "r", encoding="utf-8")
    for i in range(ii):
        s1, s2 = f1.readline(), f2.readline()
        if len(s2) < 3 or len(s1) < 3: continue
        print("Строка ", i + 1)
        ss = myautocorrect(s1)
        sim0 = ratio(s1.lower(), s2.lower())
        sim1 = ratio(ss.lower(), s2.lower())
        print("Similarity до" + str(sim1) + "\n")
        print("Similarity после" + str(sim1) + "\n")
        pr0 += sim0
        pr1 += sim1

    f1.close()
    f2.close()
    print("\nВремя проверки: " + str(time.time() - start))
    print("Процент схожести до исправления", pr0 / ii)
    print("Процент схожести после исправления", pr1 / ii)
    return pr1 / ii


#print(myautocorrect("Проверкка текчта на каккие-то ашибки. Бүгің мең мүздатуды қабылдймын!"))
#print(myautocorrect("Саламатсыз ба. Қазыбекті бүгінгі күннен заморозкадан шығара аласыз ба"))
#proverka1(config.smart_chat + "big_test5.txt", config.smart_chat + "zhaina.txt", 1000)

#print(translit("Lorem ipsum dolor sit amet", 'ru'))
#print(translit("zdravstwuite, ya hochu postavit' zamorozku. Shutka", 'ru'))
'''
aa = trans1("zdravstwuite, ya hochu postavit' zamorozku. Shutka", 'ru')
print(aa)
print(myautocorrect(aa))
aaa = trans1("Salam aleikum, men bugin zamarozkany kojamyn", 'ru')
print(aaa)
print(myautocorrect(aaa))

bb = trans2.detranslify("zdravstwuite, ya hochu postavit' zamorozku. Shutka")
bbb = trans2.detranslify("Salam aleikum, men bugin zamarozkany koyamyn")
print(bb)
print(myautocorrect(bb))
print(bbb)
print(myautocorrect(bbb))
'''

'''
sss = ("Салам алеикум алеиқум, маган мағаң бугин буғиң замарозканы замарозқаңы коясыз қоясыз ба? кымге қымғе сурак сурақ керек қереқ? " +
       "сегодня кто меня будни калаш қалаш когда сука бля ура урок магжан досбол уалихан жайна часПроведите есептер есептр есеп есптер")
for word in word_tokenize(sss):
    if len(word) < 3: continue
    print("\nWord: " + word + "\nLang: mylang=" + str(config.mylang(word)) + ", guess=" + str(guess_language(word)) +
          ", detect=" + str(detect(word)) + ", langid=" + str((langid.classify(word)[0])) +
          ", fasttext=" + str(model123.predict(word, k=2)[0][1][-2:]))
    print("kk: " + str(autospell_kk(word)) + "\nru: " + str(autospell_ru(word)))
'''


def textautocorrect(file1, file2):
    f1, f2 = open(file1, "r", encoding="utf-8"), open(file2, "a", encoding="utf-8")
    i = 0
    while True:
        s = f1.readline()
        if not s:
            break
        ss = myautocorrect(s[:-1])
        f2.write(ss + "\n")
        i += 1
    return i


#textautocorrect(config.smart_chat + "vect_text1.txt", config.smart_chat + "vect_good_text1.txt")





