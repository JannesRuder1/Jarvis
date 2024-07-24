import requests
import os 

# Define the URL for the Cohere API
url = "https://api.cohere.ai/v2/chat"

# Define the headers for the API request
headers = {
    "Authorization": "Bearer API KEY",
    "Content-Type": "application/json"
}

# Define a prompt for the public speaking coach
preamble = "Schreibe alle wichtigen informationnen aus dem folgendem text zusammen. das ziel ist alle informationen über den user in stichpunkten herauszuschreiben, und alle bisherigen gesprächsthemen in extra stichpunkten mit einem komentar, welcher weitere informatonen über das gespräch liefert, rauszuschreiben. Schreibe auch in extra stichpunkten informationen die der user jarvis explizit aufgefordert hat an sich (also Jarvis) zu ändern. Erstelle auch eine extra Stichpunkt für termine des users. Mache das in stichpunkten mit höchstens 40 Token. Überschreibe keine Informationen ergänze nur:"

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

    # Define the data for the API request
    data = {
        "preamble": preamble,
        "message": CHAT + " " + INFO,
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

    # Open the file in write mode
    with open(info_file_path, "w") as file:
        # Write the response text back to the file
        file.write(response_text)

    # Open the file in write mode and delete the contents
    with open(chat_file_path, "w") as file:
        file.write("")  # Write an empty string to delete the contents