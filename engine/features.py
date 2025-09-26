from pipes import quote
import subprocess
import webbrowser
from playsound import playsound 
import eel
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME 
import os
import sqlite3
import pywhatkit as kit
import pvporcupine
import pyaudio
import struct
import time
from engine.helper import extract_yt_term, remove_words

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


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try: 
        #pre trained keywords
        porcupine=pvporcupine.create(keywords=["jarvis","alexa","computer"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()




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


# Find contact in database and return number
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video','for','can','you','could','please','me','voice','with']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    

# def whatsApp(mobile_no, message, flag, name):

#     if flag == 'message':
#         target_tab = 12
#         assistant_message = "message send successfully to "+name

#     elif flag == 'call':
#         target_tab = 7
#         message = ''
#         assistant_message = "calling to "+name

#     else:
#         target_tab = 6
#         message = ''
#         assistant_message = "staring video call with "+name

#     # Encode the message for URL
#     encoded_message = quote(message)
#     # Construct the URL
#     whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
#     # Construct the full command
#     full_command = f'start "" "{whatsapp_url}"'
#     # Open WhatsApp with the constructed URL using cmd.exe
#     subprocess.run(full_command, shell=True)
#     time.sleep(5)
#     subprocess.run(full_command, shell=True)
    
#     pyautogui.hotkey('ctrl', 'f')

#     for i in range(1, target_tab):
#         pyautogui.hotkey('tab')

#     pyautogui.hotkey('enter')
#     speak(assistant_message)



import pygetwindow as gw

def whatsApp(mobile_no, message, flag, name):
    # Set target_tab and assistant_message based on the flag
    if flag == 'message':
        target_tab = 12  # You said 12 is the message box
        assistant_message = f"Message sent successfully to {name}"

        encoded_message = quote(message)
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    elif flag == 'call':
        target_tab = 7
        assistant_message = f"Calling {name}"
        whatsapp_url = f"whatsapp://send?phone={mobile_no}"  # No &text=
    else:  # video call
        target_tab = 6
        assistant_message = f"Starting video call with {name}"
        whatsapp_url = f"whatsapp://send?phone={mobile_no}"  # No &text=

    # Optional debug print
    print("[DEBUG] WhatsApp URL:", whatsapp_url)

    # Launch WhatsApp twice for reliability
    full_command = f'start "" "{whatsapp_url}"'
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    time.sleep(3)

    # Try to focus WhatsApp window
    try:
        windows = gw.getWindowsWithTitle('WhatsApp')
        if windows:
            windows[0].activate()
            time.sleep(1)
    except Exception as e:
        print(f"[!] Window activation failed: {e}")

    # Keyboard navigation
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)

    for _ in range(1, target_tab):
        pyautogui.hotkey('tab')
        time.sleep(0.3)

    time.sleep(0.5)
    pyautogui.hotkey('enter')

    # Confirmation
    speak(assistant_message)
