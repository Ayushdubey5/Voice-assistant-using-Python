import speech_recognition as sr
import webbrowser
import music_library
import requests
from openai import OpenAI
import time
import pygame
from gtts import gTTS
import os

# Initialize recognizer
Recognizer = sr.Recognizer()

# Initialize pygame mixer
pygame.mixer.init()

newsapi = "e0e3e18e6c434bbb90de6927c2njnae541d"  # Your NewsAPI key (unchanged)

# Function to make the program speak
def speak(text):
    print(f"Assistant: {text}")
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    # Wait till playback finishes
    while pygame.mixer.music.get_busy():
        time.sleep(0.5)
    
    # Stop mixer explicitly
    pygame.mixer.music.stop()

    # Windows sometimes locks the file for a while, so wait longer
    time.sleep(1.5)  # Increased wait
    
    # Try deleting with extra retry loop
    for _ in range(5):
        try:
            os.remove('temp.mp3')
            break
        except PermissionError:
            print("File still locked, retrying...")
            time.sleep(0.5)

def aiprocess(command):
    client = OpenAI(
        api_key="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",
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant, help as much as possible and short if possible."},
            {"role": "user", "content": command}
        ]
    )
    return response.choices[0].message.content

def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        link = music_library.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in the library.")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # Limit to 5 articles
                speak(article['title'])
        else:
            speak("Sorry, unable to fetch news now.")
    else:
        output = aiprocess(c)
        speak(output)

if __name__ == "__main__":
    speak("Hello, how may I help you")

    while True:
        try:
            with sr.Microphone() as source:
                print("LISTENING...")
                audio = Recognizer.listen(source, timeout=10, phrase_time_limit=5)
                print("RECOGNIZING...")
                command = Recognizer.recognize_google(audio)

            if command.lower() in ["hello", "hi", "hii"]:
                speak("Hi, if you have any problem, let me know")
            else:
                processcommand(command)

        except sr.RequestError as e:
            print(f"Recognition error: {e}")
        except sr.UnknownValueError:
            print("Could not understand audio")
