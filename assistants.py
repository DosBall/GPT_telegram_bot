# -*- coding: utf-8 -*-
from pprint import pprint
import json
import time
import openai
openai.api_key = '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'
client = openai.OpenAI(
    organization='org-RDWc8Ix4q80mbFDQ5lp2OWb2',
    api_key='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'
)

system_prompt0 = "Вы умный помощник компании Qalan, которая продает онлайн курсы по математике на казахском языке. Ваша задача общаться с клиентами и отвечать на их вопросы. "
system_prompt1 = "in this knowledge base there is a json of jsons, this is instructions on how to answer the user’s question. you need to find the desired topic in json keys and the standard answer, which is written in value"
system_prompt2 = "in this knowledge base there is a jsons ,these are template examples of dialogue between clients (user) and you (assistant), rely on these examples when responding to a client, use the context of the correspondence."
#первый вариант, заморозка:
file_id = 'file-6duoYWSy0XzAxP53dY1W7qAI'#'file-lUQuzgnVV9tNAQiOzgt6ux4K'
assistant0 = 'asst_oHdRfVCVpFVyYEdkcEdoZ7Bj'
thread_id = 'thread_l2qe4LMCzKQoEOH1hboEGNpW'
#инструкции json
#file_id='file-XYQ6yaGVDIQNHRNppsdUluJw'
#assistant0='asst_DgFwgPVCu2Cb0xjdWmVPJVoi'
#thread_id='thread_nYw0bK9Pyrevb0BhHeaU3RCJ'
#p1 = "1) Если тебе говорят что хотят взять перерыв, отпуск, выходной или заморозку, спроси о продолжительности текущего периода обучения и на какой срок им нужна заморозка. "
p1 = "1) If they tell you they want to take a break, vacation, day off or freeze, ask about the length of the current training period and how long they need the freeze for. Answer in Russian"
p2 = "2) Если клиент говорит что сам поставит заморозку или что он уже брал заморозку или что он не хочет ее брать, тогда ответьте одним сообщением 'ok'. "
p3 = "3) Используй контекст предыдущих сообщений. Если тема диалога связана с заморозкой ответь на вопрос "
p4 = "4) If the information was not retrieved from the knowledge base answer in one word 'mentor'"
p0 = "Вы умный помощник компании Qalan, которая продает онлайн курсы по математике на казахском языке. Ваша задача общаться с клиентами и отвечать на их вопросы. Определите на каком языке задают вопрос, на русском или казахском, и отвечайте на том же языке."

def file_down(file1):
    file = client.files.create(
        file=file1,
        purpose='assistants'
    )
    return file
#file0 = file_down(open(config.smart_chat + "finetune.json", "rb"))

file_list = client.files.list()
file_id = file_list.data[0].id
#print(file_id)

def ass_create(prompt, file_id0, name):
    assistant = client.beta.assistants.create(
        name=name,
        instructions=prompt,
        #model = "gpt-4-1106-preview",
        model="gpt-3.5-turbo-1106",
        tools=[{'type': 'retrieval'}],
        file_ids=[file_id0]
    )
    return assistant.id

#assistant0 = ass_create(system_prompt0 + system_prompt1, file_id)

def ass_update(prompt):
    global system_prompt0, file_id, assistant0
    assistant = client.beta.assistants.update(
        assistant_id=assistant0,
        name="qalantest0",
        instructions=prompt,
        model = "gpt-3.5-turbo-1106",
        #model="gpt-4-1106-preview",
        tools=[{'type': 'retrieval'}],
        file_ids=[file_id]
    )
    #assistant0 = assistant.id
    return assistant.id


#assistant0 = ass_update(system_prompt0 + system_prompt2)

#my_assistants = client.beta.assistants.list(order="desc", limit="20")
#pprint(my_assistants.data)

#thread = client.beta.threads.create()
#print(thread)
#thread_id = thread.id
#print(thread_id)

def check_user(text0, id0, a):
    global thread_id
    if a == 0:
        thread = client.beta.threads.create()
        thread_id = thread.id
    else:
        thread_id = id0
    ans = msg(text0)
    return ans, str(thread_id)

def msg(text0):
    global thread_id, assistant0
    global p1, p2, p3, p4, p0
    #client.beta.threads.messages.list(thread_id=thread_id).data.clear()

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role='user',
        content=text0
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant0,
        #instructions="Please address the user as Qalanbot. If the information was not retrieved from the knowledge base answer in one word 'mentor'" а если нет то ответь одним словом 'ментор'
        instructions=(p0)
        #instructions="найти в knowledge base подходящий под вопрос ключ и выведи его значение и 'путь' до этого значения"
        #instructions="в knowledge base прописаны интсрукции по строчкам, в начале строки пишется номер пункта или подпункта в виде '1)' или например '1.2.1)'. Найди нужную тему (конечный подпункт) в knowledge base, выведи 'путь' до нужного подпунтка и ответ, который записан после символа '=' в конечном подпункте"
    )
    time.sleep(2)
    run = client.beta.threads.runs.retrieve(thread_id = thread_id, run_id = run.id)

    while run.status not in ["completed", "failed"]:
        run = client.beta.threads.runs.retrieve(thread_id = thread_id, run_id = run.id)
        time.sleep(3)

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    #for each in messages:
    #    pprint(each.role + ":" + each.content[0].text.value)

    ans = messages.data[0].content[0].text.value
    return ans

#print(msg("Здравствуйте, можете поставить меня на заморозку?"))
#print(msg("Сәлеметсіз бе, мені заморозка кою болады ма?"))
#print(msg("Здравствуйте, на сколько дней я могу взять заморозку, в зависимости от срока обучения?"))
#print(msg("какое ответ соответсвует слову кровать"))
#print(msg("выдай все value из knowledge base в разделе животные"))
#print(msg("относится ли жаба к животным? и выведи соотвествующее слово из knowledge base"))

#response = client.beta.assistants.delete('asst_INOiofcY3i5YcT2pKKMtRq0a')
#print(response)
#response = client.files.delete('file-2rLMpyckEdx7NZOP5qXMkLEF')
#print(response)
