import json
import time
import openai
from datetime import date
import GPT4
import assistants
import config
from pprint import pprint

openai.api_key =
client = openai.OpenAI(
    organization=
    api_key=
)
file_id = 'file-vffMM1knuKo4irsEENB0FdnC'
#file_id = 'file-jBkm06LSoBxirRbgtTqQQiBi'#классификатор
#file_id = 'file-lUQuzgnVV9tNAQiOzgt6ux4K'#заморозка.txt
assistant0 = 'asst_UbxeQBYGe4GudfjBCRIi0wR3'#тестовый ассист для тестов классификации
#assistant0 = 'asst_DQUF1p3Uk27nXRObBtU24lHv'#ассист для классификации
#thread_id = ''#'thread_l2qe4LMCzKQoEOH1hboEGNpW'

#file0 = assistants.file_down(open(config.smart_chat + "categories.txt", "rb"))

#file_list = client.files.list()
#file_id = file_list.data[0].id
#print(file_id)

#ass_prompt_1 = "Вы умный помощник компании Qalan, следуйте инструкциям в prompt. В файле общая информация о заморозке."
ass_prompt_1 = ""

#assistant0 = assistants.ass_create(ass_prompt_1, file_id, "qalantest3")
#print(assistant0)

#msg_prompt1 = "Вы умный помощник компании Qalan, которая продает онлайн курсы по математике на казахском языке. Ваша задача общаться с клиентами и отвечать на их вопросы. Определите на каком языке задают вопрос, на русском или казахском, и отвечайте на том же языке."
msg_prompt1 = '''There is customer service query. Classify query into a primary category and a secondary category.

Primary categories: Заморозка, Other.

Заморозка secondary categories:
1) Поставить заморозку (пауза, перерыв)
2) Убрать (отменить) заморозку
3) Статус заморозки (проверить стоит ли заморозка)
4) Что такое заморозка?
5) Количество свободных (запасных) дней заморозки

Other secondary categories:
6) Other topics query

If you cannot determine the category, then it is 'Other topics query' secondary category, number 6.
Give your answer strictly in json format with the keys: primary, secondary and num. Where 'num' means the serial number of the second category.
For Example:
{
  "primary": "Заморозка",
  "secondary": "Что такое заморозка?",
  "num": 4
}'''
#, a vacation, a break or a pause
#msg_prompt2 = """There is customer service query.
#Give your answer strictly in one char:
#- Output '1' if query about a 'заморозка' or if the user says that he does not have time to solve the problems or if user will not be able to solve the problems
#- Otherwise print '2'"""
msg_prompt2 = """There is customer service query. Classify query into a category.
Categories:
1) Заморозка
2) Other
if query about a 'заморозка' or 'замарозка' or if user will not be able to solve the problems it is 'Заморозка' category, number 1
Otherwise it is 'Other' category. If you cannot determine the category, then it is 'Other' category, number 2
Give your answer strictly in json format with the keys: category, num. Where 'num' means the serial number of the second category.
"""



def msg(text0, thread_id):
    global assistant0, msg_prompt1
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role='user',
        content=text0
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant0,
        instructions=msg_prompt1#GPT4.system_prompt2#msg_prompt1
    )
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
    while run.status not in ["completed", "failed"]:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        time.sleep(1)
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    #for each in messages:
    #    pprint(each.role + ":" + each.content[0].text.value)
    ans = messages.data[0].content[0].text.value
    return ans


def check_user(text0: str, id0: str):
    #thread_id = ""
    thread_id = config.thread_by_chat(id0)
    if thread_id == "":
        thread = client.beta.threads.create()
        thread_id = thread.id
        js0 = {"chat_id": id0, "finished": 0, "action": 0, "date": "",
               "thread_id": str(thread_id), "msg": {"user": text0}}#str(date.today())
        with open("temp.json", "r", encoding="utf-8") as fr:
            temp_js = json.load(fr)
        temp_js["sessions"].append(js0)
        with open("temp.json", "w", encoding="utf-8") as fw:
            json.dump(temp_js, fw, indent=2, ensure_ascii=False)
        #print("новый json, thread_id: " + thread_id)
    else:
        print("старый json, thread_id: " + thread_id)
        config.add_msg("user", text0, id0)
    ans = msg(text0, thread_id)
    try:
        config.add_msg("bot", ans, id0)
    except:
        print("ошибка с config.add_msg в chat_id = " + id0)
    try:
        ll, rr = ans.index('{'), ans.index('}')
        ans_js = json.loads(ans[ll:rr + 1])
        action_num = int(ans_js['num'])
        print(action_num)
        config.change_temp('action', action_num, id0)
    except:
        print("не нашел json: ****************")
        if "Other" in ans:
            config.change_temp('action', 2, id0)
            print(1)
        elif "Заморозка" in ans:
            config.change_temp('action', 1, id0)
            print(2)
        else:
            print("GPT не смог классифицировать")
    return ans


def check_user0(text0: str, id0: str):
    thread_id = config.thread_by_chat(id0)
    if thread_id == "":
        thread = client.beta.threads.create()
        thread_id = thread.id
        js0 = {"chat_id": id0, "finished": 0, "action": 0,
               "date": str(date.today()), "thread_id": str(thread_id), "msg": text0}
        with open("temp.json", "r", encoding="utf-8") as fr:
            temp_js = json.load(fr)
        temp_js["sessions"].append(js0)
        with open("temp.json", "w", encoding="utf-8") as fw:
            json.dump(temp_js, fw, indent=2, ensure_ascii=False)
        #print("новый json, thread_id: " + thread_id)
    else:
        print("старый json, thread_id: " + thread_id)
    ans = msg(text0, thread_id)
    return ans


def my_test(fi, fo):
    i = 1
    f1 = open(config.smart_chat + fi, "r", encoding="utf-8")
    f2 = open(config.smart_chat + fo, "a", encoding="utf-8")
    while True:
        s = f1.readline()
        if not s:
            break
        ans = check_user0(s[:-1], str(i))
        a1, a2 = ans.find(' 1'), ans.find(' 2')
        if ans == "1":
            f2.write('1')
            config.change_temp('action', 1, str(i))
        elif ans == "2":
            f2.write('2')
            config.change_temp('action', 2, str(i))
        elif a1 > -1 and a2 == -1:
            f2.write('1')
            config.change_temp('action', 1, str(i))
        elif a1 == -1 and a2 > -1:
            f2.write('2')
            config.change_temp('action', 2, str(i))
        elif a1 == -1 and a2 == -1:
            f2.write('0')
        else:
            if ans.find('2.') != -1 or ans.find('2,') != -1:
                f2.write('2')
                config.change_temp('action', 2, str(i))
            elif ans.find('1.') != -1 or ans.find('1,') != -1:
                f2.write('1')
                config.change_temp('action', 1, str(i))
            else:
                f2.write('0')
        print(ans)
        i += 1
    f1.close()
    f2.close()


def my_test1(fi):
    i, err = 1, 0
    f1 = open(config.smart_chat + fi, "r", encoding="utf-8")
    #f2 = open(config.smart_chat + fo, "a", encoding="utf-8")
    while True:
        s = f1.readline()
        if not s:
            break
        try:
            check_user(s[:-1], str(i))
        except:
            err += 1
            print("Ошибка в " + str(i))
        i += 1
    print("Кол-во ошибок = " + str(err))
    print("Ответов с 0: " + str(config.count_in_json("action", 0, "temp.json")))
    print("Ответов с 1: " + str(config.count_in_json("action", 1, "temp.json")))
    print("Ответов с 2: " + str(config.count_in_json("action", 2, "temp.json")))
    f1.close()
    #f2.close()
    return 1


#my_test1("big_test.txt")
my_test1("заморозка/1.txt")
#print(check_user("Здравствуйте, можете поставить меня на заморозку?", "1"))
#print(check_user("Здравствуйте, можете снять заморозку?", "2"))
#print(check_user("Агай проверите у меня заморозка стоит?", "3"))
'''
print(check_user0("Здравствуйте, можете поставить меня на заморозку?", "1"))
print(check_user0("Салеметсизбе", "2"))
print(check_user0("Иә жақсы", "3"))
print(check_user0("жоқ, түсінбедім", "4"))#бұл бәрі емес
print(check_user0("ертеңнен бастап үш күнге", "5"))
print(check_user0("қаңтардың жиырма үшінен жиырма алтыншысына дейін", "6"))
print(check_user0("23.01 - 26.01", "7"))
print(check_user0("уйге келдім ағай замарозкадан алып тастай аламызба", "8"))
print(check_user0("Менде заморозка турды ма? тексеруіңізді өтінемін", "9"))
print(check_user0("Менде Қанша заморозка қалды? қанша күн", "10"))
print(check_user0("Заморозка дегеніміз не?", "11"))
print(check_user0("Кешбек керек", "12"))
'''


