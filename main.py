import os
import eel

from engine.features import *
from engine.command import *

eel.init('frontend')

os.system('start msedge.exe --app=http://localhost:8000/index.html')

playAssistantSound()

eel.start('index.html', mode=None, host='localhost', block=True)

#1
# import os
# import eel
# import threading
# import speech_recognition as sr

# from engine.features import *
# from engine.command import *
# from engine.helper import extract_yt_term  # If needed

# eel.init('frontend')

# # Launch the UI
# os.system('start msedge.exe --app=http://localhost:8000/index.html')

# # Play the startup sound
# playAssistantSound()


# # 🔊 Wake Word Listener Thread
# def listen_for_wake_word(wake_word="hey bro"):
#     recognizer = sr.Recognizer()

#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source)
#         eel.DisplayMessage("Listening for wake word...")

#         while True:
#             try:
#                 audio = recognizer.listen(source, phrase_time_limit=4)
#                 query = recognizer.recognize_google(audio).lower()
#                 print(f"[Wake Word Listener] Heard: {query}")

#                 if wake_word in query:
#                     speak("Yes, I am listening.")
#                     allCommands()

#             except sr.UnknownValueError:
#                 pass  # Ignore unrecognized input
#             except Exception as e:
#                 print(f"[Wake Word Error]: {e}")


# # 🔁 Start Wake Word Listener in Background
# listener_thread = threading.Thread(target=listen_for_wake_word, daemon=True)
# listener_thread.start()

# # 🧠 Start Eel App
# eel.start('index.html', mode=None, host='localhost', block=True)


#2
# import os
# import eel
# import threading
# import speech_recognition as sr
# import webbrowser

# from engine.features import *
# from engine.command import *
# from engine.helper import extract_yt_term  # If needed

# eel.init('frontend')

# # Launch the UI
# os.system('start msedge.exe --app=http://localhost:8000/index.html')

# # Play the startup sound
# playAssistantSound()


# # 🔊 Wake Word Listener Thread
# def listen_for_wake_word(wake_word="hey bro"):
#     recognizer = sr.Recognizer()

#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source)
#         eel.DisplayMessage("Listening for wake word...")

#         while True:
#             try:
#                 audio = recognizer.listen(source, phrase_time_limit=5)
#                 query = recognizer.recognize_google(audio).lower()
#                 print(f"[Wake Word Listener] Heard: {query}")

#                 if wake_word in query:
#                     speak("Yes, I am listening.")
                    
#                     # 🔁 Enter follow-up command loop
#                     while True:
#                         follow_up = takeCommand()
#                         if not follow_up:
#                             continue

#                         if follow_up in ["stop", "cancel", "exit", "thank you"]:
#                             speak("Okay, going back to sleep.")
#                             break

#                         handleCommand(follow_up)

#             except sr.UnknownValueError:
#                 pass
#             except Exception as e:
#                 print(f"[Wake Word Error]: {e}")

#     recognizer = sr.Recognizer()

#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source)
#         eel.DisplayMessage("Listening for wake word...")

#         while True:
#             try:
#                 audio = recognizer.listen(source, phrase_time_limit=6)
#                 query = recognizer.recognize_google(audio).lower()
#                 print(f"[Wake Word Listener] Heard: {query}")

#                 if wake_word in query:
#                     # Remove wake word from the query
#                     clean_query = query.replace(wake_word, "").strip()

#                     speak("Yes, I am listening.")
#                     handleCommand(clean_query)   # <-- pass query directly

#             except sr.UnknownValueError:
#                 pass
#             except Exception as e:
#                 print(f"[Wake Word Error]: {e}")


# def handleCommand(query):
#     if not query:
#         return

#     print(f"[User Command] {query}")

#     # --- Search ---
#     if query.startswith("search for") or query.startswith("search"):
#         search_term = query.replace("search for", "").replace("search", "").strip()
#         if search_term:
#             speak(f"Searching Google for {search_term}")
#             url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
#             webbrowser.open(url)
#         else:
#             speak("I could not understand what to search")

#     # --- Open website or system app ---
#     elif query.startswith("open"):
#         from engine.features import openCommand
#         openCommand(query)


#     # --- YouTube ---
#     elif "on youtube" in query:
#         command_type, _ = extract_yt_term(query)
#         if command_type == 'search':
#             searchYoutube(query)
#         else:
#             playYoutube(query)

#     else:
#         speak("Sorry, I didn't understand that.")


# # 🔁 Start Wake Word Listener in Background
# listener_thread = threading.Thread(target=listen_for_wake_word, daemon=True)
# listener_thread.start()

# # 🧠 Start Eel App
# eel.start('index.html', mode=None, host='localhost', block=True)
