##Combined STT & TTS with HuggingFace DialoGPT and Flask backend server
# just connect to the ip and port and generate spoken output
import threading
import speech_recognition as sr
import requests
import pyttsx3
from termcolor import colored
import sys
import time
import wikipedia
import webbrowser



# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Flask server details of the Mac
FLASK_SERVER_URL = "http://127.0.0.1:5000/"

# Wake word and stop word
WAKE_WORD = "vision"
STOP_WORD = "over"

# Text-to-speech function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Print text with color and animation
def print_animated(text, color):
    for char in text:
        sys.stdout.write(colored(char, color))
        sys.stdout.flush()
        time.sleep(0.05)  # Adjust the speed of typing animation
    print()  # Newline after the text is printed

# Listen and recognize speech
def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio).lower()
        return text
    
    #Testing
    except sr.UnknownValueError:
        print_animated("Google Speech Recognition could not understand audio", "red")
    except sr.RequestError as e:
        print_animated(f"Could not request results from Google Speech Recognition service; {e}", "red")
    return ""

# Listen for the wake word
def listen_for_wake_word():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            speech_as_text = recognizer.recognize_google(audio).lower()
            return WAKE_WORD in speech_as_text
        #Waiting for wake word
        except sr.UnknownValueError:
            return False
        except sr.RequestError:
            return False

# Google search function
def google_search(query):
    search_url = "https://www.google.com/search?q=" + query
    webbrowser.open(search_url)
    speak("I found this on google.")

# Wikipedia search function
def wikipedia_search(query):
    results = wikipedia.summary(query, sentences=3)
    speak(f"According to Wikipedia: {results}")
    print_animated(f"According to Wikipedia: {results}", "magenta")

"""# Main function
def main():
    while True:
        if listen_for_wake_word():
            print_animated("Wake word heard, start conversation...", "cyan")
            user_input = recognize_speech_from_mic(recognizer, sr.Microphone())
            if user_input:
                if STOP_WORD in user_input:
                    print_animated("Stop word heard, ending the program...", "red")
                    break
                print_animated(f"You said: {user_input}", "green")
                if 'search for' in user_input:
                    google_search(user_input.replace('search for', '').strip())
                elif 'wikipedia' in user_input:
                    wikipedia_search(user_input.replace('wikipedia', '').strip())
                else:
                    response = requests.post(f"{FLASK_SERVER_URL}/dialogpt", json={"text": user_input})
                    if response.status_code == 200:
                        reply_text = response.json().get("response", "")
                        print_animated(f"AI replied: {reply_text}", "yellow")
                        speak(reply_text)
                    else:
                        print_animated("Failed to get response from the Mac server.", "red")
        else:
            print_animated("Listening for wake word...", "blue")"""

# Handle server dialogue in a separate thread
def handle_server_dialogue(user_input):
    response = requests.post(f"{FLASK_SERVER_URL}/dialogpt", json={"text": user_input})
    if response.status_code == 200:
        reply_text = response.json().get("response", "")
        print_animated(f"Vision replied: {reply_text}", "yellow")
        speak(reply_text)
    else:
        print_animated("Failed to get response from the server.", "red")
#Main Loop
def main():
    end_conversation = False
    while True:
        if end_conversation == True:
            break
        # Listen for the wake word
        if listen_for_wake_word():
            print_animated("Wake word heard, start conversation...", "cyan")

            # Start conversation loop
            while True:
                user_input = recognize_speech_from_mic(recognizer, sr.Microphone())
                if user_input:
                    if STOP_WORD in user_input:
                        print_animated("Stop word heard, ending the conversation...", "red")
                        speak("See you!")
                        end_conversation = True
                        break  # Exit conversation loop
                    print_animated(f"You said: {user_input}", "green")
                    
                    if "your name" in user_input:
                        speak("I am Vision!")

                    # Handling different types of user input
                    elif 'search for' in user_input:
                        google_search_thread = threading.Thread(target=google_search, args=(user_input.replace('search for', '').strip(),))
                        google_search_thread.start()
                    elif 'wikipedia' in user_input:
                        wikipedia_search_thread = threading.Thread(target=wikipedia_search, args=(user_input.replace('wikipedia', '').strip(),))
                        wikipedia_search_thread.start()
                    else:
                        print_animated("Generating response...", "white")
                        handle_server_dialogue(user_input)
                else:
                    print_animated("Listening...", "blue")

        # Listening for wake word
        else:
            print_animated("Listening for wake word...", "blue")

if __name__ == "__main__":
    main()



