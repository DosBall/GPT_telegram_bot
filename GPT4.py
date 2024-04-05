from datetime import date
import openai
import time
import json
import config
openai.api_key = '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'

zamorozka = ["заморозка", "зоморозка", "замарозка", "муздану", "мұздану", "муздату", "мұздату", "мұздау", "муздау"]

system_prompt1 = '''There is customer service query. Classify query into a primary category and a secondary category.

Primary categories: Заморозка, Cashback, Technical Support, Other.

Заморозка secondary categories:
1) Поставить заморозку (пауза, перерыв)
2) Убрать (отменить) заморозку
3) Статус заморозки (проверить стоит ли заморозка)
4) Что такое заморозка?
5) Количество свободных (запасных) дней заморозки

Cashback secondary categories:
6) Cashback did not arrive or did not arrive completely
7) Information about cashback, question related to cashback

Technical Support secondary categories:
8) problems with solving tasks (math problems)
9) problems with the site
10) problems with problem conditions
11) ask for help with math problems

Other secondary categories:
12) Greetings
13) Agreement (Иә, жақсы, да, хорошо и т.д.)
14) Disagreement (не согласен)
15) Date (day, сегодня, дата и т.д.)
16) Other topics query

If you cannot determine the category, then it is 'Other topics query' secondary category, number 16.
Give your answer strictly in json format with the keys: primary, secondary and num. Where 'num' means the serial number of the second category.
For Example:
{
  "primary": "Заморозка",
  "secondary": "Что такое заморозка?",
  "num": 4
}'''
system_prompt2 = """There is customer service query about "заморозка" in Kazakh or Russian.
Determine what the query says, select the desired item:
1) Просят поставить заморозку
2) Просят убрать (отменить) заморозку
3) Просят проверить стоит ли заморозка
4) Говорят что сами поставили или убрали заморозку
5) Говорят что планируют поставить или убрать заморозку
6) Просят рассказать что такое заморозка
7) Хотят узнать сколько свободных (запасных) дней заморозки осталось

Give your answer strictly in one number - the number of the required item"""
system_prompt3 = "Тебе дано русское или казахское слово возможно написанное с опечатками, исправь его если нужно и выведи обратно только это слово и больше ничего"


def gpt_msg(user_text):
    global system_prompt1
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",#"gpt-4"
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt3},
                {"role": "user", "content": user_text},
            ]
        )
    except:
        return "Вышло время выполнения msg"
    #return response['choices'][0]['message']['context']
    return response['choices'][0]['message']['content']


def msg(text):
    for s in zamorozka:
        if s in text:
            return gpt_msg(text)
    return "ментор"


def js_create(text0, id0: str):
    js0 = {"chat_id": id0, "finished": 0, "action": 0, "date": str(date.today()),
           "thread_id": id0, "msg": text0, "ans": ""}
    with open("temp.json", "r", encoding="utf-8") as fr:
        temp_js = json.load(fr)
    temp_js["sessions"].append(js0)
    with open("temp.json", "w", encoding="utf-8") as fw:
        json.dump(temp_js, fw, indent=2, ensure_ascii=False)
    try:
        ans = gpt_msg(text0)
    except:
        print("Ошибка при работе msg в " + str(id0))
        return 0
    try:
        config.change_temp("ans", ans, id0)
    except:
        print("ошибка с config.change_temp в chat_id = " + id0)
    try:
        ll, rr = ans.index('{'), ans.index('}')
        ans_js = json.loads(ans[ll:rr + 1])
        action_num = int(ans_js['num'])
        print(str(action_num) + " id: " + str(id0))
        config.change_temp('action', action_num, id0)
    except:
        print("не нашел json: ****************")
        for jj in range(16, 0, -1):
            if str(jj) in ans:
                config.change_temp('action', jj, id0)
                print(str(jj) + " ans: " + ans)
                return ans
        print("GPT не смог классифицировать")
    return ans


def my_test1(fi):
    i, err = 1, 0
    start = time.time()
    f1 = open(config.smart_chat + fi, "r", encoding="utf-8")
    #f2 = open(config.smart_chat + fo, "a", encoding="utf-8")
    while True:
        s = f1.readline()
        if not s:
            break
        try:
            js_create(s[:-1], str(i))
        except:
            err += 1
            print("Ошибка в тесте номер " + str(i))
        i += 1
        time.sleep(0.1)
    print("Временя на исполнение кода: " + str(time.time() - start))
    print("Кол-во ошибок = " + str(err))
    for jj in range(17):
        print("Ответов с "+str(jj)+":\t" + str(config.count_in_json("action", jj, "temp.json")))
    f1.close()
    #f2.close()
    return 1

#my_test1("big_test.txt")

#print(msg("Выбери лишнее: стол, стул, кефир, шкаф"))
#print(msg("Почему ты стедал такой выбор?"))
#print(msg("Какое сообщение я тебе отправил в начале нашего диалога?"))
def gptmsgtest(file):
    i, err = 1, 0
    ans = [0, 0, 0, 0, 0, 0, 0, 0]
    start = time.time()
    f = open(file, "r", encoding="utf")
    while True:
        s = f.readline()
        if not s:
            break
        try:
            m = gpt_msg(s[:-1])
            print(str(i) + ": " + m)
            stop = 0
            for ii in range(8):
                if m[0] == str(ii):
                    ans[ii] += 1
                    stop = 1
                    break
            if stop == 0:
                for ii in range(8):
                    if str(ii) in m:
                        ans[ii] += 1
                        stop = 1
                        break
            if stop == 0:
                ans[0] += 1
        except:
            err += 1
            print("Ошибка в тесте номер " + str(i))
        i += 1
        time.sleep(0.1)
    print("Временя на исполнение кода: " + str(time.time() - start))
    print("Кол-во ошибок = " + str(err))
    print(ans)
    f.close()
    return 0

#gptmsgtest("C:/Users/ITQALAN12/Documents/smart_chat/заморозка/1.txt")

#print(gpt_msg("Здравствуйте, можете поставить мне замрозку на завтра?"))
#print(gpt_msg("Здравствуйте, можете убрать мне заморозку с сегодняшнего дня?"))
#print(gpt_msg("агай, менде заморозка турды ма?"))
#print(gpt_msg("апай, мен замарозканы ертеңге қойдым"))#print(gpt_msg("апай, мен замарозканы койдым на завтра"))
#print(gpt_msg("апай, я завтра заморозку поставлю"))#print(gpt_msg("апай, мен ертен заморозканы коямын, занят буду"))
#print(gpt_msg("зымырозка бул не?"))
#print(gpt_msg("агай, калайсыз? менде замарозканы канша кун калды?"))
"""Временя на исполнение кода: 4499.751828672587
Кол-во ошибок = 0
Ответов с 0:	5
Ответов с 1:	208
Ответов с 2:	31
Ответов с 3:	18
Ответов с 4:	9
Ответов с 5:	26
Ответов с 6:	95
Ответов с 7:	73
Ответов с 8:	722
Ответов с 9:	97
Ответов с 10:	19
Ответов с 11:	18
Ответов с 12:	255
Ответов с 13:	7
Ответов с 14:	25
Ответов с 15:	54
Ответов с 16:	925"""
i1 = 1
with open(config.smart_chat + "slova0.txt", "r", encoding="utf-8") as f1:
    while i1 <= 1781:
        s = f1.readline()
        i1 += 1
    while i1 <= 1881:
        s = f1.readline()
        if not s:
            break
        stop = s.find(":")
        s = s[:stop]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # "gpt-4"
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt3},
                {"role": "user", "content": s},
            ]
        )
        ans = response['choices'][0]['message']['content']
        with open(config.smart_chat + "gpt_исправления.txt", "a", encoding="utf-8") as f2:
            f2.write(s + " = " + ans + "\n")
        print(s + " = " + ans)
        i1 += 1


