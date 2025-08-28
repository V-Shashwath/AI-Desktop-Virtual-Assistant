import os
import eel

from engine.features import *
from engine.command import *

eel.init('frontend')

os.system('start msedge.exe --app=http://localhost:8000/index.html')

playAssistantSound()

eel.start('index.html', mode=None, host='localhost', block=True)


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
