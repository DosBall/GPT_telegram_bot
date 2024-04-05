import json
import pickle
import string
import time
import openai
from datetime import date

from skllm.models.gpt import ZeroShotGPTClassifier, MultiLabelZeroShotGPTClassifier

smart_chat = "C:/Users/ITQALAN12/Documents/smart_chat/"


def thread_by_chat(chatid):
    with open("temp.json", "r", encoding="utf-8") as fr:
        data = json.load(fr)
    minimal = 0
    for i in data["sessions"]:
        if i["chat_id"] == chatid:
            if i["finished"] == 0:
                return i["thread_id"]
            else:
                print("Найден элемент finished=True, chat_id = " + chatid + ", thread_id = " + i['thread_id'])
                with open("finished.json", "r", encoding="utf-8") as f1:
                    data0 = json.load(f1)
                data0["sessions"].append(i)
                with open("finished.json", "w", encoding="utf-8") as f0:
                    json.dump(data0, f0, indent=2, ensure_ascii=False)
                data["sessions"].pop(minimal)
        minimal += 1
    with open("temp.json", "w", encoding="utf-8") as fw:
        json.dump(data, fw, indent=2, ensure_ascii=False)
    return ""


def change_temp(key, value, chatid):
    with open("temp.json", "r", encoding="utf-8") as fr:
        data = json.load(fr)
    minimal = 0
    for i in data["sessions"]:
        if i["chat_id"] == chatid:
            i[key] = value
            with open("temp.json", "w", encoding="utf-8") as fw:
                json.dump(data, fw, indent=2, ensure_ascii=False)
            return minimal
        minimal += 1
    with open("temp.json", "w", encoding="utf-8") as fw:
        json.dump(data, fw, indent=2, ensure_ascii=False)
    print("##### Not Found chatid: " + str(chatid) + ", key: " + str(key) + ", value: " + str(value))
    return -1


def add_msg(key, value, chatid):
    with open("temp.json", "r", encoding="utf-8") as fr:
        data = json.load(fr)
    minimal = 0
    for i in data["sessions"]:
        if i["chat_id"] == chatid:
            #i["msg"].update(json.loads("{'" + str(key) + "': '" + str(value) + "'}"))
            i["msg"].update({key: value})
            with open("temp.json", "w", encoding="utf-8") as fw:
                json.dump(data, fw, indent=2, ensure_ascii=False)
            return minimal
        minimal += 1
    with open("temp.json", "w", encoding="utf-8") as fw:
        json.dump(data, fw, indent=2, ensure_ascii=False)
    print("##### Not Found chatid: " + str(chatid) + ", key: " + str(key) + ", value: " + str(value))
    return -1


example_json = {
    "chat_id": "123",
    "finished": 0, #"False"
    "action": 0,
    "date": "2024-01-18",
    "thread_id": "",
    "msg": ""
}


def count_in_json(key, value, file):
    with open(file, "r", encoding="utf-8") as fr:
        data = json.load(fr)
    ans = 0
    for i in data["sessions"]:
        if i[key] == value:
            ans += 1
    with open(file, "w", encoding="utf-8") as fw:
        json.dump(data, fw, indent=2, ensure_ascii=False)
    return ans


def actions_count(file):
    print("Ответов с 0: " + str(count_in_json("action", 0, file)))
    print("Ответов с 1: " + str(count_in_json("action", 1, file)))
    print("Ответов с 2: " + str(count_in_json("action", 2, file)))
    print("Ответов с 3: " + str(count_in_json("action", 3, file)))
    print("Ответов с 4: " + str(count_in_json("action", 4, file)))
    print("Ответов с 5: " + str(count_in_json("action", 5, file)))
    print("Ответов с 6: " + str(count_in_json("action", 6, file)))
    print("Ответов с 7: " + str(count_in_json("action", 7, file)))
    print("Ответов с 8: " + str(count_in_json("action", 8, file)))
    print("Ответов с 9: " + str(count_in_json("action", 9, file)))
    print("Ответов с 10: " + str(count_in_json("action", 10, file)))
    print("###")

#actions_count(smart_chat + "test1_400.json")

def count_in_txt(file):
    with open(file, "r", encoding="utf-8") as fr:
        s = fr.read()
        a1 = s.count('1')
        a2 = s.count('2')
        a0 = s.count('0')
    return [a1, a2, a0]

#print(count_in_txt(smart_chat + "testout0.txt"))


def add_action_json(file):
    with open(file, "r", encoding="utf-8") as fr:
        data = json.load(fr)
    n = 1
    for i in data["chat_messages"]:
        #i["id"] = n
        n += 1
        if "амаро" in i["text"] or "аморо" in i["text"]:
            i["action"] = 1
    with open(file, "w", encoding="utf-8") as fw:
        json.dump(data, fw, indent=2, ensure_ascii=False)
    return ""
#add_action_json(smart_chat + "chat_messages_1.json")

'''
print("Ответов с 0: " + str(count_in_json("action", 0, smart_chat + "test2_2587.json")))
print("Ответов с 1: " + str(count_in_json("action", 1, smart_chat + "test2_2587.json")))
print("Ответов с 2: " + str(count_in_json("action", 2, smart_chat + "test2_2587.json")))
with open(smart_chat + "chat_messages_1.json", "r", encoding="utf-8") as fr:
    data1 = json.load(fr)
mas1 = []
for i in data1["chat_messages"]:
    if i["action"] == 1:
        mas1.append(int(i["id"]))
with open(smart_chat + "chat_messages_1.json", "w", encoding="utf-8") as fw:
    json.dump(data1, fw, indent=2, ensure_ascii=False)
print(len(mas1))
with open(smart_chat + "test2_2587.json", "r", encoding="utf-8") as fr:
    data = json.load(fr)
ans = []
for i in data["sessions"]:
    if i["action"] == 1 and int(i["chat_id"]) not in mas1:
        ans.append(int(i["chat_id"]))
with open(smart_chat + "test2_2587.json", "w", encoding="utf-8") as fw:
    json.dump(data, fw, indent=2, ensure_ascii=False)
print(len(ans))
print(ans)
ans1 = []
with open(smart_chat + "chat_messages_1.json", "r", encoding="utf-8") as fr:
    data2 = json.load(fr)
for i in data2["chat_messages"]:
    if i["id"] in ans and i["action"] == 0:
        ans1.append(int(i["id"]))
with open(smart_chat + "chat_messages_1.json", "w", encoding="utf-8") as fw:
    json.dump(data2, fw, indent=2, ensure_ascii=False)
print(len(ans1))
print(ans1)
'''
def myclf1(train, test, types0, types1, fileout, mas, modfile, modact):
    start1 = time.time()
    if modact:
        #clf = MultiLabelZeroShotGPTClassifier(openai_model="gpt-4", max_labels=3)#"gpt-3.5-turbo"
        clf = ZeroShotGPTClassifier(openai_model="gpt-4")  # "gpt-3.5-turbo"
        clf.fit(X=train, y=types0)
        predicted = clf.predict(X=test)
        with open(smart_chat + modfile, 'wb') as file12:
            pickle.dump(clf, file12)
    else:
        with open(smart_chat + modfile, 'rb') as file12:
            clf = pickle.load(file12)
        predicted = clf.predict(X=test)
    print("Time for predict = " + str(time.time() - start1))
    with open(smart_chat + fileout, "a", encoding="utf-8") as f0:
        f0.write("\n################\n")
        i, tp, fp, tn, fn, err = 1, 0, 0, 0, 0, 0
        for a, b, c, d in zip(mas, test, predicted, types1):
            #print(f"Message: {a}\nPredicted Sentiment: {b}\n")
            f0.write(f"Message {i}: {a}\nTranslated: {b}\nPredicted Sentiment: {c}\nActual label: {d}\n\n")
            if c == d:
                if d == "mentor":
                    tn += 1
                else:
                    tp += 1
            else:
                if d == "mentor":
                    fp += 1
                else:
                    fn += 1
            i += 1
    return tp, fp, tn, fn, err


def temp_str1(file):
    with open(file, "r", encoding="utf-8") as f1:
        text = f1.read().replace("\n", " ")
        textToLower = text.lower()
    onestr = " "
    for s in textToLower:
        for c in s:
            if c in string.whitespace or c.isalpha():#c.isalnum()
                if c in string.whitespace and onestr[-1] == " ":
                    continue
                onestr += c
            else:
                if onestr[-1] != " ":
                    onestr += " "
    return(onestr[1:])


def mylang(text):
    lang = "ru"
    kk = "ӘәІіҢңҒғҮүҰұҚқӨөҺһ"
    en = "QqWwEeRrTtYyUuIiOoPpAaSsDdFfGgHhJjKkLlZzXxCcVvBbNnMm"
    for i in kk:
        if i in text:
            lang = "kk"
            break
    for i in en:
        if i in text:
            lang = "en"
            break
    return lang


dzamen = {
    "бұгін": "бүгін",
    "бугин": "бүгін",
    "бугін": "бүгін",
    "бүгин": "бүгін",
    "бугын": "бүгін",

    "замарозка": "заморозка",
    "замазка": "заморозка",
    "замороз": "заморозка",
    "морозка": "заморозка",
    "щамарозка": "заморозка",
    "зомарозка": "заморозка",
    "замаразка": "заморозка",
    "зоморозка": "заморозка",

    "кешбек": "кешбэк",
    "кэшбэк": "кешбэк",
    "cashback": "кешбэк",
    "кешпек": "кешбэк",
    "кэшбек": "кешбэк",
    "кэшпэк": "кешбэк",
    "кешпэк": "кешбэк",
    "кэшпек": "кешбэк",
}
#from polyglot.detect import Detector
#print(Detector("Саламатсыз ба"))
#print(chardet.detect("Саламатсыз ба".encode('cp1251'))["language"])
#print(chardet.detect("бүгінгі".encode('utf-8')))
#print(detect_langs("Саламатсыз ба. Қазыбекті бүгінгі күннен щаморощкадан шығара аласыз ба"))
'''
from guess_language import guess_language
print(guess_language("Проверкка текчта на каккие-то ашибки. Бүгің мең мүздатуды қабылдймын!"))
print(guess_language("Саламатсыз ба. Қазыбекті бүгінгі күннен щаморощкадан шығара аласыз ба"))
print(guess_language("бүгінгі"))
print(guess_language("абайлау"))
print(guess_language("сулык"))
print("--------")

import langid
print(langid.classify("Проверкка текчта на каккие-то ашибки. Бүгің мең мүздатуды қабылдймын!")[0])
print(langid.classify("Саламатсыз ба. Қазыбекті бүгінгі күннен щаморощкадан шығара аласыз ба")[0])
print(langid.classify("бүгінгі")[0])
print(langid.classify("абайлау")[0])
print(langid.classify("сулык")[0])
print("--------")

model = fasttext.load_model('lid.176.ftz')
print(model.predict("Проверкка текчта на каккие-то ашибки. Бүгің мең мүздатуды қабылдймын!", k=2)[0][1][-2:])
print(model.predict("Саламатсыз ба. Қазыбекті бүгінгі күннен щаморощкадан шығара аласыз ба", k=2)[0][1][-2:])
print(model.predict("бүгінгі", k=2)[0][1][-2:])
print(model.predict("абайлау", k=2)[0][1][-2:])
print(model.predict("сулык", k=2)[0][1][-2:])
print("--------")
'''

rukkzamena = {
    "к": "қ",
    "н": "ң",
    "г": "ғ",
    "и": "і",
    "о": "ө",
    "а": "ә"
}

zamrzam = {
    "замарозка": "заморозка",
    "замароазка": "заморозка",
    "зомарозка": "заморозка",
    "зоморозка": "заморозка",
    "замарозке": "заморозка",
    "щамарозка": "заморозка",
    "щаморозка": "заморозка",
    "зоморозке": "заморозка",
    "заморозке": "заморозка",
}





