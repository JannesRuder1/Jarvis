import requests
import pyttsx3
import speech_recognition as sr
import sys
import datetime
import time
import os

r = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        print("Standby mode...")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            if text.lower() == "jarvis":
                print("Jarvis mode activated!")
                # Add the path to the Python file you want to execute
                os.system("python C:\Users\jannes\Desktop\jarvis\jarvis.py")
            else:
                print("Standby mode...")
        except:
            print("Standby mode...")