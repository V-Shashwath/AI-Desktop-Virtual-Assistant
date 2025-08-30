import webbrowser
from playsound import playsound 
import eel
from engine.command import speak
from engine.config import ASSISTANT_NAME 
import os
import sqlite3
import pywhatkit as kit
from engine.helper import extract_yt_term

connection = sqlite3.connect("adva.db")
cursor = connection.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "frontend\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)
    

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":
        try:
            cursor.execute(
                'SELECT path FROM system_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

# import os
# import subprocess
# import webbrowser
# from engine.command import speak
# from engine.config import ASSISTANT_NAME

# APP_PATHS = {
#     "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
#     "notepad": "notepad",
#     "calculator": "calc",
#     "vscode": r"C:\Users\user\AppData\Local\Programs\Microsoft VS Code\Code.exe",
#     "spotify": r"C:\Users\user\AppData\Roaming\Spotify\Spotify.exe"
# }

# def openCommand(query):
#     query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip().lower()

#     if not query:
#         speak("Not sure what to open.")
#         return

#     # 🌐 Website case
#     if "." in query or any(keyword in query for keyword in ["google", "youtube", "linkedin", "canva", "instagram", "facebook"]):
#         url = query if query.startswith("http") else "https://" + query
#         speak(f"Opening {query} in browser.")
#         webbrowser.open(url)
#         return

#     # 💻 System apps
#     if query in APP_PATHS:
#         app_path = APP_PATHS[query]
#         try:
#             subprocess.Popen(app_path)
#             speak(f"Opening {query}")
#         except Exception as e:
#             speak(f"Could not open {query}")
#             print(f"[Error opening {query}]:", e)
#         return

#     # Fallback
#     try:
#         os.system("start " + query)
#         speak("Trying to open " + query)
#     except Exception as e:
#         speak("Could not open " + query)
#         print(f"[Fallback error]: {e}")


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