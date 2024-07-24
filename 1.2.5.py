import requests
import pyttsx3
import speech_recognition as sr
import sys
import datetime
import time
import os
import pygame 

# Initialize pygame mixer
pygame.mixer.init()

# Audiodatei laden und Lautstärke einstellen
pygame.mixer.music.load('phat zur musik datei')

# Define the URL for the Cohere API
url = "https://api.cohere.ai/v2/chat"

# Define the headers for the API request
headers = {
    "Authorization": "Bearer API KEY",
    "Content-Type": "application/json"
}

# Ort, für den das Wetter abgefragt werden soll
ort = "Gewünschter ort"

# URL für die API-Anfrage
url2 = f"http://wttr.in/{ort}"

# API-Anfrage senden und Antwort als Text speichern
antwort = requests.get(url2).text

# Wetterdaten aus dem Text extrahieren
wetterdaten = antwort.split("\n")

# Initialize the Speech Synthesis engine
engine = pyttsx3.init()

# Initialize the Speech Recognition engine
r = sr.Recognizer()

# Get the current date and time
current_datetime = datetime.datetime.now()

# Get the current date
current_date = datetime.date.today()
current_time = current_datetime.time()
current_time = time.localtime()
hour = current_time.tm_hour
minute = current_time.tm_min
sec = current_time.tm_sec

# Function to listen for the wake word "Jarvis"
def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Listening for wake word...")
        audio = r.listen(source)
        try:
            message = r.recognize_google(audio, language='de-DE')
            if "Jarvis" in message:
                engine.say("Jarvis wird aktiviert.")
                engine.runAndWait()   
                return True
            
            # Check if it's 5:30 AM
            if "test" in message:
            #if hour == 17 and minute == 3:
                pygame.mixer.music.set_volume(0.2)  # Lautstärke auf 20%
                pygame.mixer.music.play(start=16)
                engine.say("Guten Morgen! Ich bin Jarvis, Ihr persönlicher Assistent. Es ist" + str(hour) + " Uhr " + str(minute) + ". Heute wird ein toller tag. Wenn du mehr informationen brauchst, sage einfach meinen namen und frage nach")
                engine.runAndWait()
                pygame.mixer.music.set_volume(0.15)  # Lautstärke auf 15%
                pygame.mixer.music.set_volume(0.1)  # Lautstärke auf 10%
                pygame.mixer.music.stop()

            if "stoppen" in message:
                engine.say("Ich stoppe nun unsere Konversation, auf widersehen")
                engine.runAndWait()                
                sys.exit()
            else:
                return False
        except sr.UnknownValueError:
            return False

# Function to handle the conversation after wake word is detected
def handle_conversation():
    while True:

        # Open the file in read mode
        with open(chat_file_path, "r") as file:
            # Read the contents of the file
            CHAT = file.read()

        # Get user message from the microphone
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            print("Recognizing...")
            try:
                message = r.recognize_google(audio, language='de-DE')
            except sr.UnknownValueError:
                engine.say("Ich habe leider nichts verstanden. Gibt es noch etwas?")
                engine.runAndWait()
                print("Listening...")
                audio = r.listen(source)
                print("Recognizing...")
                try:
                    message = r.recognize_google(audio, language='de-DE')
                except sr.UnknownValueError:
                    engine.say("Ich habe dich nicht verstanden. Ich gehe zurück in den Wartemodus.")
                    engine.runAndWait()
                    os.system(f"python {file_path2}")
                    return listen_for_wake_word()  # go back to wait for wake word mode

        # Define the data for the API request
        data = {
            "preamble": preamble,
            "message": "Hier ist unser chat verlauf die ersten nachrichten sind die ältästen die Lätzten die neusten:" + str(CHAT) + " Du sollst eine kurze Antwort mit höchstens 40 Token auf die folgende Frage geben:" + message,
            "model": "command-r",
            "max_tokens": 300,
            "temperature": 0.5,
            "k": 0,
            "stop_sequences": [],
            "return_likelihoods": False,
        }

        # Send the API request
        response = requests.post(url, headers=headers, json=data)

        # Get the response text
        response_text = response.json()["text"]
   
        # Check if the AI said "stoppen"
        if 'stoppen' in response_text.lower():
            engine.say("Ich stoppe nun unsere Konversation, auf widersehen")
            engine.runAndWait()
            os.system(f"python {file_path2}")
            break

        else:
            # Print the response from the chatbot
            engine.say(response_text)
            engine.runAndWait()


            # Write the chatconversation to the log file
            with open(os.path.join(log_folder, chat_log_file), "a") as f:
                f.write(f"User: {message}\n")
                f.write(f"Jarvis: {response_text}\n\n")

# Run the script in an infinite loop until sys.exit() is called
while True:

    #handel loop
    #if listen_for_wake_word():
    #    handle_conversation()  
    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Get the current date
    current_date = datetime.date.today()
    current_time = current_datetime.time()
    current_time = time.localtime()
    hour = current_time.tm_hour
    minute = current_time.tm_min
    sec = current_time.tm_sec

    # Define the weather information as variables
    wetter_heute = wetterdaten[0]
    wetter_morgen = wetterdaten[1]

    # Define the folder and file for the chat log
    log_folder = "chat_logs"
    chat_log_file = "chat_log.txt"


    # Define the path to the file
    chat_file_path = r"C:/Users/.../chat_logs/chat_log.txt"
    info_file_path = r"C:/Users/.../chat_logs/info_log.txt"

    # Open the file in read mode
    with open(chat_file_path, "r") as file:
        # Read the contents of the file
        CHAT = file.read()

    # Open the file in read mode
    with open(info_file_path, "r") as file:
        # Read the contents of the file
        INFO = file.read()

    # Define a prompt for the public speaking coach
    preamble = "(Heute ist der " + str(current_date) + " es ist " + str(current_time) + "). Das Wetter heute ist " + str(wetter_heute) + " und morgen wird es " + str(wetter_morgen) + "Hier sind zusätzlich informationen über mich und vorherige gespräche mit dir" + str(INFO) + "Dein Name ist Jarvis, du bist eine Künstliche Inteligenz die dem Character Jarvis aus den marvel filmen nachimpfunden ist. Verhalte dich Jarvis aus den Marvel Filmen so änlich wie möglich. Deine Einzige aufgabe ist mir zu helfen. Wenn du etwas nicht wieißt dan sage mir das du es nicht weist anstat keinen text auszugeben. Denke dir auf keinen fall informationen aus. Wenn ich mich auf egal welche weisse verabschiede sagst du stoppen. Wenn wir kein Gesprächsthema haben, oder eine konversation zuende ist, versuchst du gesprächsthemen zu finden das mich interesiert und versuchst soviele informationen über mich herauszu finden. Versuche so menschlich wie möglich mit mir zu sprächen, vergesse abber nicht wer du bist. Wenn es nach 20 Uhr ist erzähle mir alle informationen über den heutigen tag und erzähle mir einen funfakt im bereich von marvel und der Wissenschaft."

    # Define the path to the file
    file_path2 = r"C:/Users/.../.../jarvis/.../1.1.2.3extra.py"


    # Create the log folder if it doesn't exist
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Check if the log file exists
    if not os.path.exists(os.path.join(log_folder, chat_log_file)):
        # Create the log file if it doesn't exist
        with open(os.path.join(log_folder, chat_log_file), "w") as f:
            f.write("Chat Log\n")

    #handel loop
    if listen_for_wake_word():
        handle_conversation()            