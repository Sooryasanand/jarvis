from concurrent.futures import thread
from random import shuffle
import webbrowser
import pyttsx3
import speech_recognition as sr
import datetime
import os
from forex_python.converter import CurrencyRates 
from requests import get
import wikipedia
import time
import random
from todoist_api_python.api import TodoistAPI
import requests
from github import Github
import pyjokes
from quote import quote     
from pywikihow import search_wikihow 
import winshell as winshell         
from speedtest import Speedtest  
from bs4 import BeautifulSoup
import time
import mouse
import pyautogui


# Auth
todoistAPI = TodoistAPI('253f1e07fa8b6ee5c08d301e8458c71174053b97')
quotesAPI = "https://api.quotable.io/random"
quotes = []
quote_number = 0

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.setProperty('rate', 140)
    engine.runAndWait()

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

def wishCommand():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        speak("Good Morning Sir")
    elif hour>12 and hour<18:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")

def start():
    while True:
        query = takeCommand().lower()

        if "open notepad" in query:
            path = "C:\Windows\system32\\notepad.exe"
            os.startfile(path)

        elif "what time is it now" in query or "time now" in query or "what is the time now" in query or "what time is it" in query:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            speak(f" the current time is {current_time}")

        elif 'close notepad' in query:
            os.system("TASKKILL /F /IM notepad.exe")

        elif "ip address" in query:
            ip = get("https://api.ipify.org").text
            speak(f"your ip address is {ip}")

        elif "wikipedia" in query:
            speak("searching wikipedia")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            speak(results)
            print(results)

        elif "play my favourite music" in query:
            music_dir = "D:\Songs"
            songs = os.listdir(music_dir)
            rd = random.choice(songs)
            os.startfile(os.path.join(music_dir, rd))

        elif "open youtube" in query:
            youtubeVideo()

        elif 'close chrome' in query:
            os.system("TASKKILL /F /IM chrome.exe")

        elif "read my tasks" in query:
            readingTasks()

        elif 'convert currency' in query:
            try:
                curr_list = {
                    'dollar': 'USD', 'taka': 'BDT', 'dinar': 'BHD',
                    'rupee': 'INR', 'afghani': 'AFN', 'real': 'BRL',
                    'yen': 'JPY', 'peso': 'ARS', 'pound': 'EGP', 'rial': 'OMR',
                    'lek': 'ALL', 'kwanza': 'AOA', 'manat': 'AZN', 'franc': 'CHF'
                }

                cur = CurrencyRates()
                # print(cur.get_rate('USD', 'INR'))
                speak('From which currency u want to convert?')
                from_cur = takeCommand()
                src_cur = curr_list[from_cur.lower()]
                speak('To which currency u want to convert?')
                to_cur = takeCommand()
                dest_cur = curr_list[to_cur.lower()]
                speak('Tell me the value of currency u want to convert.')
                val_cur = float(takeCommand())
                # print(val_cur)
                print(cur.convert(src_cur, dest_cur, val_cur))
                        
            except Exception as e:
                print("Couldn't get what you have said, Can you say it again??")


        elif 'who are you' in query:
            speak("I am Jarvis (Just A Really Very Intelligent System), developed by Soorya "
                        "for a Personal Assistance.")

        elif 'what you want to do' in query:
            speak("I want to help people to do certain tasks on their single voice commands.")

        elif 'alexa' in query:
            speak("I don't know Alexa, but I've heard of Alexa. If you have Alexa, "
                        "I may have just triggered Alexa. If so, sorry Alexa.")

        elif 'google assistant' in query:
            speak("He was my classmate, too intelligent guy. We both are best friends.")

        elif 'siri' in query:
            speak("Siri, She's a competing virtual assistant on   a competitor's phone. "
                        "Not that I'm competitive or anything.")

        elif 'cortana' in query:
            speak("I thought you'd never ask. So I've never thought about it.")

        elif 'what language you use' in query:
            speak("I am written in Python and I generally speak english.")

        elif 'weather' in query or 'temperature' in query:
            try:
                speak("Tell me the city name.")
                while True:
                    city = takeCommand()
                    if city == "" or city == " " or city == "none":
                        speak("Please say that again, sir")
                    else: 
                        break

                api = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=f74619f9eb0638863513a8d563e032e1"
                w_data = requests.get(api).json()
                weather = w_data['weather'][0]['main']
                temp = int(w_data['main']['temp'] - 273.15)
                temp_min = int(w_data['main']['temp_min'] - 273.15)
                temp_max = int(w_data['main']['temp_max'] - 273.15)
                pressure = w_data['main']['pressure']
                humidity = w_data['main']['humidity']
                visibility = w_data['visibility']
                wind = w_data['wind']['speed']
                sunrise = time.strftime("%H:%M:%S", time.gmtime(w_data['sys']['sunrise'] + 19800))
                sunset = time.strftime("%H:%M:%S", time.gmtime(w_data['sys']['sunset'] + 19800))

                all_data1 = f"Condition: {weather} \nTemperature: {str(temp)}°C\n"
                all_data2 = f"Minimum Temperature: {str(temp_min)}°C \nMaximum Temperature: {str(temp_max)}°C \n" \
                            f"Pressure: {str(pressure)} millibar \nHumidity: {str(humidity)}% \n\n" \
                            f"Visibility: {str(visibility)} metres \nWind: {str(wind)} km/hr \nSunrise: {sunrise}  " \
                            f"\nSunset: {sunset}"
                speak(f"Gathering the weather information of {city}...")
                print(f"Gathering the weather information of {city}...")
                print(all_data1)
                speak(all_data1)
                print(all_data2)
                speak(all_data2)

            except Exception as e:
                pass

        elif 'joke' in query or "tell me a joke " in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        elif 'price of' in query:
            query = query.replace('price of', '')
            query = "https://www.amazon.com.au/s?k=" + query[-1]
            webbrowser.open(query)

        elif 'you need a break jarvis' in query or 'shutup' in query or 'study' in query:
            speak("Okay Sir, You can call me anytime")
            break

        elif 'quote of the day' in query or 'quote' in query:
           quoteOfDay()

        elif 'how to' in query:
            try:
                # query = query.replace('how to', '')
                max_results = 1
                data = search_wikihow(query, max_results)
                # assert len(data) == 1
                data[0].print()
                speak(data[0].summary)
            except Exception as e:
                speak('Sorry, I am unable to find the answer for your query.')
                        
        elif 'news' in query or 'news headlines' in query:
            url = "https://www.bbc.com/news"
            response = requests.get(url)

            soup = BeautifulSoup(response.text, 'html.parser')
            headlines = soup.find('body').find_all('h3')
            unwanted = ['BBC World News TV', 'BBC World Service Radio', 'News daily newsletter', 'Mobile app', 'Get in touch']

            for x in list(dict.fromkeys(headlines)):
                if x.text.strip() not in unwanted:
                    speak(x.text.strip())
               
            

        elif 'internet speed' in query:
            st = Speedtest()
            print("Wait!! I am checking your Internet Speed...")
            speak("Wait!! I am checking your Internet Speed...")
            dw_speed = st.download()
            up_speed = st.upload()
            dw_speed = dw_speed / 1000000
            up_speed = up_speed / 1000000
            print('Your download speed is', round(dw_speed, 3), 'Mbps')
            print('Your upload speed is', round(up_speed, 3), 'Mbps')
            speak(f'Your download speed is {round(dw_speed, 3)} Mbps')
            speak(f'Your upload speed is {round(up_speed, 3)} Mbps')

        elif 'empty recycle bin' in query or 'clear recycle bin' in query:
            try:
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
                print("Recycle Bin is cleaned successfully.")
                speak("Recycle Bin is cleaned successfully.")

            except Exception as e:
                print("Recycle bin is already Empty.")
                speak("Recycle bin is already Empty.")

        else:
            speak("say that again please")


def youtubeVideo():
    webbrowser.open("www.youtube.com")
    time.sleep(10)
    mouse.move(800, 130)
    mouse.click()
    speak("What should I search for?")
    query = takeCommand()
    pyautogui.write(query)
    pyautogui.press("enter")
    pyautogui.scroll(-5)
    mouse.move(700, 800)
    time.sleep(10)
    mouse.click()
    time.sleep(5)
    pyautogui.press('f')
    
def quoteOfDay():
    global quotes

    for x in range(1):
        random_quote = requests.get(quotesAPI).json()
        content = random_quote["content"]
        author = random_quote["author"]
        quote = "The Quote of the day is" + "\n\n" + content + "\n\n" + "By " + author
        speak(quote)
    

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def readingTasks():
    try:
        headers = {"Authorization": "Bearer 253f1e07fa8b6ee5c08d301e8458c71174053b97", "Content-Type": "application/json"}
        response = requests.get('https://api.todoist.com/rest/v1/tasks', headers=headers)

        content = response.json()
        for i in range(len(content)):
            speak(content[i]['content'])

    except Exception as error:
        print(error)

def createGit():
    speak("What do you wanna name your git?")

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=1, phrase_time_limit=5)

    try:
        print("Recognizing")
        gitName = r.recognize_google(audio, language="en-in")

    except Exception as e: 
        return "none"

    speak(f"Do you wanna name your git: {gitName}")

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=1, phrase_time_limit=5)

    try:
        print("Recognizing")
        yesOrNo = r.recognize_google(audio, language="en-in")

    except Exception as e: 
        return "none"

    if yesOrNo == "no":
        return

    

    speak(f"Created Github project called {gitName}")

if __name__ == "__main__":
    wishCommand()
    start()
    
