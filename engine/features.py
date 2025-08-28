import webbrowser
from playsound import playsound 
import eel
from engine.command import speak
from engine.config import ASSISTANT_NAME 
import os
import pywhatkit as kit
from engine.helper import extract_yt_term

@eel.expose
def playAssistantSound():
    music_dir = "frontend\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)
    

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    if query != "":
        speak("opening " + query)
        os.system('start ' + query)
    else:
        speak("not found")

def playYoutube(query):
    query = query.replace(ASSISTANT_NAME, "")
    command_type, search_term = extract_yt_term(query)

    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Could not understand what to play on YouTube")

def searchYoutube(query):
    query = query.replace(ASSISTANT_NAME, "")
    command_type, search_term = extract_yt_term(query)

    if search_term:
        speak("Searching YouTube for " + search_term)
        url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
        webbrowser.open(url)
    else:
        speak("Could not understand what to search on YouTube")