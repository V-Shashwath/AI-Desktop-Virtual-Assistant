import pyttsx3
import speech_recognition as sr
import eel
import time

from engine.helper import extract_yt_term

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6 )
    
    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
        time.sleep(2)
        

    except Exception as e:
        return ""

    return query.lower()    


# text = takeCommand()
# speak(text)

@eel.expose
def allCommands():
    query = takeCommand()
    print(query)

    if 'open' in query:
        from engine.features import openCommand
        openCommand(query)
    elif 'on youtube' in query:
        from engine.features import playYoutube, searchYoutube
        command_type, _ = extract_yt_term(query)
        
        if command_type == 'search':
            searchYoutube(query)
        else:
            playYoutube(query)



    else:
        print("not run")
    
    eel.ShowHood()