import pyttsx3
import speech_recognition as sr
import eel
import time
import webbrowser   

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


# @eel.expose
# def allCommands():
#     query = takeCommand()
#     print(f"[User Query] {query}")

#     if query == "":
#         return
    
#     # --- Search commands ---
#     if query.startswith("search for") or query.startswith("search"):
#         search_term = query.replace("search for", "").replace("search", "").strip()
#         if search_term:
#             speak(f"Searching Google for {search_term}")
#             url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
#             webbrowser.open(url)
#         else:
#             speak("I could not understand what to search")

#     # --- Website opening ---
#     elif "open" in query:
#         site = query.replace("open", "").strip()

#         # Common website keywords (you can expand this list)
#         common_sites = {
#             "google": "https://www.google.com",
#             "youtube": "https://www.youtube.com",
#             "canva": "https://www.canva.com",
#             "spotify": "https://www.spotify.com",
#             "linkedin": "https://www.linkedin.com",
#             "facebook": "https://www.facebook.com",
#             "instagram": "https://www.instagram.com"
#         }

#         if site in common_sites:
#             speak(f"Opening {site}")
#             webbrowser.open(common_sites[site])
#         elif "." in site:   # if user says "open github.com"
#             speak(f"Opening {site}")
#             if not site.startswith("http"):
#                 site = "https://" + site
#             webbrowser.open(site)
#         else:
#             # Try as system app
#             from engine.features import openCommand
#             openCommand(query)

#     # --- YouTube play/search ---
#     elif 'on youtube' in query:
#         from engine.features import playYoutube, searchYoutube
#         command_type, _ = extract_yt_term(query)

#         if command_type == 'search':
#             searchYoutube(query)
#         else:
#             playYoutube(query)

#     else:
#         speak("Sorry, I didn't understand that.")

#     eel.ShowHood()

