import speech_recognition as sr
import pyttsx3
import pywhatkit

listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
# Set the voice based on the voice index; 0 for male voice and 1 for female voice
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(command)
    except Exception as e:
        print(e)
        return ""
    return command

def run_assistant():
    command = take_command()
    try:
        if 'play' in command:
            song = command.replace('play', '')
            talk('Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'search' in command:
            search_term = command.replace('search', '')
            talk('Searching for ' + search_term)
            pywhatkit.search(search_term)
        else:
            talk('Please say the command again.')
    except Exception as e:
        talk('Sorry, I am unable to perform the task.')
        print(e)

run_assistant()
