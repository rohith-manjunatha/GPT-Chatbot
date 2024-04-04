import openai
import speech_recognition as sr
from dotenv import dotenv_values
import pyttsx3

config = dotenv_values('.env')

def listen_for_audio():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Listening...",flush=True)     
            recognizer.adjust_for_ambient_noise(source,duration=0.2)
            audio = recognizer.listen(source) 
        try:
                text = recognizer.recognize_google(audio)
                print("You: " + text)
                return text
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            continue
        except sr.RequestError as e:
            print("Error recognizing the audio; {0}".format(e))
            return ""

def text_to_speach(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 125)

def ask_gpt(prompt,conversation):
    gpt_output = ''
    conversation.append({'role':'user','content': prompt})
    response = openai.ChatCompletion.create(
        model = 'gpt-4',
        messages=conversation,
        temperature = 0.7,
        stream = True,
    )
    print('GPT: ',end='')
    for chunk in response:
        if not chunk.choices[0].finish_reason:
            print(chunk.choices[0].delta.content, end="",flush=True)
            gpt_output+=chunk.choices[0].delta.content
    print()
    conversation.append({"role": "assistant", 'content': gpt_output})
    text_to_speach(gpt_output)
    
if __name__ == '__main__':
    openai.api_key = config["API_KEY"]
    openai.api_base = config["API_BASE"]
    conversation = []

    while True:
        prompt = listen_for_audio() # input('You: ') 
        if prompt.lower() == 'stop':
            break
        ask_gpt(prompt,conversation)