import sys
from openai import OpenAI
from apikey import api_data
import os
import speech_recognition as sr
import pyttsx3
import webbrowser
import time

# OpenAI setup
Model = "gpt-4o"
client = OpenAI(api_key=api_data)

def Reply(question):
    try:
        completion = client.chat.completions.create(
            model=Model,
            messages=[
                {'role': "system", "content": "You are a helpful assistant."},
                {'role': 'user', 'content': question}
            ],
            max_tokens=200
        )
        answer = completion.choices[0].message.content
        return answer
    except Exception as e:
        return f"Sorry, I could not get a response: {str(e)}"

# Text-to-speech setup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening .......')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print('Recognizing ....')
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}\n")
    except Exception:
        print("Say that again .....")
        return "None"
    return query.lower()

# Open websites dynamically
def open_website(query):
    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "linkedin": "https://www.linkedin.com",
        "github": "https://www.github.com"
    }
    for key, url in sites.items():
        if f"open {key}" in query:
            webbrowser.open(url)
            speak(f"Opening {key}")
            return True
    return False

# Main loop
if __name__ == '__main__':
    speak("Hello! How can I assist you today?")
    while True:
        query = takeCommand()
        if query == "none":
            continue
        if "bye" in query or "exit" in query:
            speak("Goodbye! Have a nice day.")
            break
        elif open_website(query):
            continue
        else:
            ans = Reply(query)
            print(ans)
            speak(ans)
