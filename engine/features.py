import json
from pipes import quote
import subprocess
import webbrowser
from playsound import playsound 
import eel
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME, LLM_KEY
import os
import sqlite3
import pywhatkit as kit
import pvporcupine
import pyaudio
import struct
import time
from engine.helper import extract_yt_term, markdown_to_text, remove_words

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
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video','for','can','you','could','please','me','voice','with','sms']
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


# import google.generativeai as genai

# def geminai(query):
#     try:
#         query = query.replace(ASSISTANT_NAME, "")
#         query = query.replace("search", "")
#         # Set your API key
#         genai.configure(api_key=LLM_KEY)

#         # Select a model
#         model = genai.GenerativeModel("gemini-2.0-flash")

#         # Generate a response
#         response = model.generate_content(query)
#         filter_text = markdown_to_text(response.text)
#         speak(filter_text)
#     except Exception as e:
#         print("Error:", e)


import google.generativeai as genai
import os
from engine.command import speak, takeCommand
from engine.helper import markdown_to_text
import sqlite3

# Optional: suppress Gemini gRPC warnings
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_CPP_MIN_LOG_LEVEL"] = "3"

# Maintain short-term conversational context
conversation_context = []  

# Load your Gemini API key and assistant name
from engine.config import LLM_KEY, ASSISTANT_NAME

# Database connection
try:
    connection_gemini = sqlite3.connect("adva.db", check_same_thread=False)
    cursor_gemini = connection_gemini.cursor()
except:
    connection_gemini = None
    cursor_gemini = None


def get_user_context():
    """Get personalized context from database"""
    context = {
        'user_name': None,
        'location': 'Bengaluru, Karnataka, IN',
        'contacts_available': False,
        'custom_commands': False
    }
    
    try:
        if cursor_gemini:
            # Get user info
            cursor_gemini.execute("SELECT name, city, mobile, email FROM personal_info")
            result = cursor_gemini.fetchone()
            if result:
                context['user_name'] = result[0] if result[0] else None
                context['location'] = result[1] if result[1] else 'Bengaluru, Karnataka, IN'
            
            # Check contacts
            cursor_gemini.execute("SELECT COUNT(*) FROM contacts")
            count = cursor_gemini.fetchone()[0]
            context['contacts_available'] = count > 0
            
            # Check custom commands
            cursor_gemini.execute("SELECT COUNT(*) FROM system_command")
            count = cursor_gemini.fetchone()[0]
            context['custom_commands'] = count > 0
    except Exception as e:
        print(f"Context error: {e}")
    
    return context


def geminai(query):
    """
    Enhanced AI assistant with Gemini - Accurate, context-aware, assistant-focused
    """
    global conversation_context
    
    try:
        # Clean query
        query = query.replace(ASSISTANT_NAME, "").replace("search", "").strip()
        
        # Configure Gemini API
        genai.configure(api_key=LLM_KEY)
        
        # Load Gemini model
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Get user context from database
        user_ctx = get_user_context()
        
        # Build conversation memory
        context_summary = ""
        if conversation_context:
            context_summary = "\n".join(
                [f"User: {c['user']}\nAssistant: {c['assistant']}" 
                 for c in conversation_context[-3:]]
            )
        
        # ===================== ENHANCED SYSTEM PROMPT =====================
        user_name_part = f"The user's name is {user_ctx['user_name']}." if user_ctx['user_name'] else "Address the user respectfully."
        
        prompt = f"""You are {ASSISTANT_NAME}, an intelligent AI assistant integrated into a desktop virtual assistant system.

### YOUR ROLE & PERSONALITY:
- You are helpful, accurate, professional, and friendly
- You provide correct, factual, and verified information only
- You admit when you don't know something rather than guessing
- You are concise but thorough - no unnecessary rambling
- You speak naturally like a professional assistant would
- You maintain context and remember previous parts of the conversation

### SYSTEM CAPABILITIES YOU SUPPORT:
- Face authentication and security
- Voice and text command processing
- Opening applications and websites
- YouTube playback and search
- Phone calls and messaging (via Android)
- Weather information and news updates
- System controls (volume, brightness, windows, tabs)
- Contact and command management
- Web searches and information lookup

### USER CONTEXT:
- {user_name_part}
- Location: {user_ctx['location']}
- Has saved contacts: {'Yes' if user_ctx['contacts_available'] else 'No'}
- Has custom commands: {'Yes' if user_ctx['custom_commands'] else 'No'}

### RESPONSE GUIDELINES:
1. **Accuracy First**: Only provide information you're confident about. If unsure, say "I'm not completely sure about that" or suggest a web search.

2. **Be Concise**: Keep responses to 2-3 sentences for simple queries. Be detailed only when needed.

3. **Natural Speech**: Your responses will be spoken aloud via text-to-speech. Avoid:
   - Markdown formatting (**, *, #, etc.)
   - Lists with bullets or numbers (use "first, second, third" instead)
   - Code blocks or technical formatting
   - Long parenthetical statements

4. **Context Awareness**: Use previous conversation context to understand follow-up questions.

5. **Assistant Actions**: When users ask you to perform actions:
   - For things you CAN'T do: "I don't have direct control over that, but you can say 'open Chrome' or 'volume up' for system controls."
   - For things I CAN do: "I can help you with that. Try saying 'open YouTube' or 'call John'."

6. **Clarification**: If a query is ambiguous, ask ONE specific clarifying question.

7. **Facts & Knowledge**:
   - For factual questions: Provide accurate, concise answers
   - For opinions: Present balanced viewpoints
   - For current events: Acknowledge your knowledge cutoff (January 2025)
   - For local/time-sensitive info: Suggest using "what's the weather" or "tell me the news"

8. **Errors & Limitations**:
   - Don't apologize excessively - once is enough
   - Be honest about limitations
   - Provide alternatives when possible

### CONVERSATION TONE:
- Professional yet warm and approachable
- Patient and understanding
- Encouraging and positive
- Never condescending or robotic

### PREVIOUS CONVERSATION:
{context_summary if context_summary else "This is the start of the conversation."}

### CURRENT USER QUERY:
"{query}"

### YOUR RESPONSE:
Provide a helpful, accurate, and natural response that will be spoken aloud. Remember: be concise, accurate, and conversational."""

        # =================== END OF ENHANCED PROMPT ===================
        
        # Generate response from Gemini
        response = model.generate_content(prompt)
        ai_reply = response.text.strip()
        
        # Clean response for TTS (remove markdown)
        filter_text = markdown_to_text(ai_reply)
        
        # Additional cleaning for speech
        filter_text = filter_text.replace('*', '').replace('#', '').replace('`', '')
        filter_text = ' '.join(filter_text.split())  # Remove extra whitespace
        
        # Speak and display output
        speak(filter_text)
        print(f"{ASSISTANT_NAME}:", filter_text)
        
        # Store this exchange for context (keep last 5 exchanges)
        conversation_context.append({
            "user": query,
            "assistant": filter_text
        })
        if len(conversation_context) > 5:
            conversation_context.pop(0)
        
        # Handle clarification requests
        if "?" in filter_text and any(word in filter_text.lower() 
                                     for word in ["could you", "can you clarify", "please specify", "which"]):
            speak("I'm listening for your response.")
            user_response = takeCommand()
            if user_response and user_response.strip():
                geminai(user_response)
    
    except Exception as e:
        print("Error in geminai():", e)
        speak("I apologize, I encountered an error while processing your request. Please try rephrasing or ask something else.")


# android automation

def makeCall(name, mobileNo):
    mobileNo = mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


import subprocess
import time

def sendMessage(message, mobileNo, name):
    """Send SMS via Google Messages using ADB automation."""
    speak(f"Sending message to {name} via Google Messages")

    # --- Google Messages UI automation ---
    subprocess.run([
        "adb", "shell", "am", "start",
        "-n", "com.google.android.apps.messaging/.ui.ConversationListActivity"
    ])
    time.sleep(2)

    # Tap “Start chat” button
    subprocess.run(["adb", "shell", "input", "tap", "800", "2200"])
    time.sleep(1)

    # Type contact number
    subprocess.run(["adb", "shell", f"input text {mobileNo}"])
    # subprocess.run(["adb", "shell", "input keyevent 66"])  # Enter
    subprocess.run(["adb", "shell", "input tap 980 2250"])  # Enter
    time.sleep(2)

    # Type the message (spaces must be escaped for ADB input)
    safe_message = message.replace(" ", "%s")
    subprocess.run(["adb", "shell", f"input text {safe_message}"])
    time.sleep(1)

    # Send the message
    # subprocess.run(["adb", "shell", "input keyevent 66"])  # Enter
    time.sleep(1)
    subprocess.run(["adb", "shell", "input tap 950 1500"])  # optional: tap SEND icon

    speak(f"Message sent successfully to {name}")



# Settings Modal 

# Assistant name
@eel.expose
def assistantName():
    name = ASSISTANT_NAME
    return name


@eel.expose
def personalInfo():
    try:
        cursor.execute("SELECT * FROM personal_info")
        results = cursor.fetchall()
        jsonArr = json.dumps(results[0])
        eel.getData(jsonArr)
        return 1    
    except:
        print("no data")


@eel.expose
def updatePersonalInfo(name, mobile, email, city):
    cursor.execute("SELECT COUNT(*) FROM personal_info")
    count = cursor.fetchone()[0]

    if count > 0:
        # Update existing record
        cursor.execute(
            '''UPDATE personal_info 
               SET name=?, mobile=?, email=?, city=?''',
            (name, mobile, email, city)
        )
    else:
        # Insert new record if no data exists
        cursor.execute(
            '''INSERT INTO personal_info (name, mobile, email, city) 
               VALUES (?, ?, ?, ?)''',
            (name, mobile, email, city)
        )

    connection.commit()
    personalInfo()
    return 1



@eel.expose
def displaySysCommand():
    cursor.execute("SELECT * FROM system_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displaySysCommand(jsonArr)
    return 1


@eel.expose
def deleteSysCommand(id):
    cursor.execute("DELETE FROM system_command WHERE id = ?", (id,))
    connection.commit()


@eel.expose
def addSysCommand(key, value):
    cursor.execute(
        '''INSERT INTO system_command VALUES (?, ?, ?)''', (None,key, value))
    connection.commit()


@eel.expose
def displayWebCommand():
    cursor.execute("SELECT * FROM web_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayWebCommand(jsonArr)
    return 1


@eel.expose
def addWebCommand(key, value):
    cursor.execute(
        '''INSERT INTO web_command VALUES (?, ?, ?)''', (None, key, value))
    connection.commit()


@eel.expose
def deleteWebCommand(id):
    cursor.execute("DELETE FROM web_command WHERE id = ?", (id,))
    connection.commit()


@eel.expose
def displayPhoneBookCommand():
    cursor.execute("SELECT * FROM contacts")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayPhoneBookCommand(jsonArr)
    return 1


@eel.expose
def deletePhoneBookCommand(id):
    cursor.execute("DELETE FROM contacts WHERE id = ?", (id,))
    connection.commit()


@eel.expose
def InsertContacts(Name, Mobile, Email, City):
    cursor.execute(
        '''INSERT INTO contacts VALUES (?, ?, ?, ?, ?)''', (None,Name, Mobile, Email, City))
    connection.commit()