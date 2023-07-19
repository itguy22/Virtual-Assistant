import speech_recognition as sr
import pyttsx3
import pywhatkit
import sqlite3

conn = sqlite3.connect('reminders.db')

conn.execute('''CREATE TABLE IF NOT EXISTS reminders
                (reminder TEXT, remind_time TEXT);''')


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
        elif 'remind me to' in command:
            reminder = command.replace('remind me to', '')
            talk('When should I remind you?')
            remind_time = take_command()  # Use voice commands for input
            talk('I will remind you to' + reminder + ' at ' + remind_time)
            conn.execute("INSERT INTO reminders (reminder, remind_time) VALUES (?, ?)",
                         (reminder, remind_time))
            conn.commit()
        else:
            talk('Please say the command again.')
    except Exception as e:
        talk('Sorry, I am unable to perform the task.')
        print(e)

try:
    while True:
        run_assistant()
except KeyboardInterrupt:
    print("Stopping the assistant...")
finally:
    # Always ensure the connection to the database is closed
    conn.close()
