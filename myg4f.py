import g4f
g4f.debug.logging = True  # Enable debug logging
g4f.debug.check_version = False  # Disable automatic version checking
print(g4f.Provider.Bing.params)  # Print supported args for Bing

system_prompt1 = "Отвечай на русском языке"
#system_prompt1 = "Вы умный помощник компании, которая продает онлайн курсы по математике. Ваша задача общаться с клиентами и отвечать на их вопросы. О чем говориться в данном тексте? Дайте ответ на русском языке."
def main2(user_text):
    global system_prompt1
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",#model="gpt-4",
            temperature=0,
            #stream=True,
            messages=[
                {"role": "system", "content": system_prompt1},
                {"role": "user", "content": user_text},
            ]
        )
        return response
    except Exception:
        return "Exception error ;("
    except:
        return "Ошибочка ;<"

def main1(user_text):
    global system_prompt1
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt1},
                {"role": "user", "content": user_text},
            ]
        )
        #return response['choices']['0']['message']['context']
        return response
    except Exception:
        return "Exception error ;("
    except:
        return "Ошибочка ;<"

#print(main1("Привет, завтра я уезжаю с родителями в поездку в горы и не смогу закончить задания в срок. Хочу взять перерыв на два дня, поможете?"))
