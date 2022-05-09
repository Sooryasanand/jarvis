import speech_recognition as sr
import os

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=1, phrase_time_limit=5)

    try:
        print("Recognizing")
        query = r.recognize_google(audio, language="en-in")
        print(f"user said: {query}")

    except Exception as e: 
        return "none"
    return query

while True:

    wake_up = takeCommand().lower()

    if "wake up" in wake_up or "hey jarvis" in wake_up:
        os.startfile('D:\Projects\Jarvis\Jarvis.py')

    else:
        print("no command")