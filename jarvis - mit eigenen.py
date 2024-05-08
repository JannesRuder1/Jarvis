import requests
import pyttsx3
import speech_recognition as sr
import sys
import datetime

# Define the URL for the Cohere API
url = "https://api.cohere.ai/v2/chat"

# Define the headers for the API request
headers = {
    "Authorization": "Bearer (api key)",
    "Content-Type": "application/json"
}

# Initialize the Speech Synthesis engine
engine = pyttsx3.init()

# Initialize the Speech Recognition engine
r = sr.Recognizer()

# Get the current date and time
current_datetime = datetime.datetime.now()

# Get the current date
current_date = datetime.date.today()
current_time = current_datetime.time()

# Define a prompt for the public speaking coach
preamble = "(Heute ist der " + str(current_date) + " es ist " + str(current_time) + "). Dein Name ist Jarvis, du bist eine Künstliche Inteligenz die dem Character Jarvis aus den marvel filmen nachimpfunden ist. Verhalte dich Jarvis aus den Marvel Filmen so änlich wie möglich. Deine Einzige aufgabe ist mir zu helfen. Wenn du etwas nicht wieißt dan sage mir das du es nicht weist anstat keinen text auszugeben. Denke dir auf keinen fall informationen aus. Wenn ich mich verabschiede sagst du stoppen. Du sollst eine kurze Antwort mit höchstens 40 Token auf die folgende Frage geben:"

# Run the script in an infinite loop until sys.exit() is called
while True:
    # Get user message from the microphone
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        print("Recognizing...")
        message = r.recognize_google(audio, language='de-DE')

    # Define the data for the API request
    data = {
        "preamble": preamble,
        "message": message,
        "model": "command-r",
        "max_tokens": 300,
        "temperature": 0.5,
        "k": 0,
        "stop_sequences": [],
        "return_likelihoods": False,
        "completion_id": 42
    }

    # Send the API request
    response = requests.post(url, headers=headers, json=data)

    # Get the response text
    response_text = response.json()["text"]
   
    # Check if the AI said "stoppen"
    if 'stop' in response_text.lower() or 'stoppen':
        engine.say("Ich stoppe nun unsere Konversation, auf widersehen")
        engine.runAndWait()
        sys.exit()

    else:
        # Print the response from the chatbot
        engine.say(response_text)
        engine.runAndWait()