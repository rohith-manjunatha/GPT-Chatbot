import speech_recognition as sr

def listen_for_audio():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Listening...")     
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
import pyttsx3
def text_to_speech(text):
	engine = pyttsx3.init()
	engine.say(text)
	engine.runAndWait()
# listen_for_audio()
text_to_speech('i will speak this text')
# print(sr.Microphone())