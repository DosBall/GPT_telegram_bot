import openai
from pydub import AudioSegment
import json
openai.api_key = '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'
model_id = 'whisper-1'
audio_name = "test2"
mydir = "/home/dosball/audio2text/testaudios/"
#f = open(mydir + audio_name + ".mp3", "rb")
finaltext = ""
t = 30#в секундах

def resp(i):
    global mydir, audio_name, finaltext
    ff = open(mydir + audio_name + "_" + str(i) + ".mp3", "rb")
    response = openai.Audio.transcribe(
        #api_key=API_KEY,
        model=model_id,
        file=ff,
        response_format="text",
        language="kk"
    )
    ff.close()
    #print("Отрывок от " + str(i - 1) + " до " + str(i) + " минуты: ")
    #print("Отрывок " + str(i) + " по 10 секунд: ")
    #print(response)
    finaltext += response[:-1]


def audio_cut(audio_name):
    global mydir, t
    mp3 = AudioSegment.from_mp3(mydir + audio_name + ".mp3")
    mp3 = mp3.set_channels(1)
    mp3 = mp3.set_frame_rate(16000)
    audio_len = int(len(mp3))
    if audio_len <= (t + 1) * 1000:
        mp3.export(mydir + audio_name + "_1.mp3", format="mp3")
        resp(1)
    else:
        ii = (2 * t + 1) * 1000
        atemp = mp3[:((t + 1) * 1000)]
        atemp.export(mydir + audio_name + "_1.mp3", format="mp3")
        resp(1)
        while ii < audio_len:
            atemp = mp3[(ii - ((t + 2) * 1000)):ii]
            iin = ii // (t * 1000)
            atemp.export(mydir + audio_name + "_" + str(iin) + ".mp3", format="mp3")
            resp(iin)
            ii += (t * 1000)
        atemp = mp3[(ii - ((t + 2) * 1000)):]
        iin = ii // (t * 1000)
        atemp.export(mydir + audio_name + "_" + str(iin) + ".mp3", format="mp3")
        resp(iin)

with open("/home/dosball/audio2text/etalon_words.json") as fj:
    words = ""
    js = json.load(fj)
    for ij in js["correct"]:
        words += ij
        words += ", "
    #print(words)


audio_cut(audio_name)
print(finaltext)
#resp(5)
#f.close()

#system_prompt="Listen to my audio dialogue in Kazakh and give me the text of the conversation in Kazakh, use lowercase Kazakh letters, without punctuation, please"
#system_prompt = "Ты умный помощник для редактирования казахских текстов. В тексте много ошибочных слов и опечаток, замени эти слова на подходящие по смыслу текст. Используй контекст. Используй казахский язык и не используй знаки препинания"
#system_prompt = "You are a smart assistant for editing Kazakh texts. There may be typos in the text, try to replace unclear words with Kazakh words that are suitable in meaning and sound. Use context. Give your answer in Kazakh, do not use punctuation. Here is an example of good reference words in Kazakh: ( " + words + ")."
system_prompt = "Вы умный помощник для редактирования казахских текстов. В тексте могут быть опечатки, попробуй заменить непонятные слова подходящими по смыслу и звучанию казахскими словами. Но твой обработанный текст должен быть не меньше полученного. Используйте контекст. Дайте ответ на казахском языке"

def generate_corrected_transcript(temperature, system_prompt, finaltext):

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature = temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": finaltext},
        ]
    )
    return response['choices'][0]['message']['content']

corrected_text = generate_corrected_transcript(0, system_prompt, finaltext)
#corrected_text = generate_corrected_transcript(0, system_prompt, corrected_text)

print(corrected_text)