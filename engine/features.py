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
from engine.helper import markdown_to_text
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress warnings
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_CPP_MIN_LOG_LEVEL"] = "3"

# ENHANCED: Full conversation context with metadata
conversation_context = []
conversation_metadata = {
    'topic': None,
    'last_query_time': None,
    'interaction_count': 0
}

from engine.config import LLM_KEY, ASSISTANT_NAME

try:
    connection_gemini = sqlite3.connect("adva.db", check_same_thread=False)
    cursor_gemini = connection_gemini.cursor()
except:
    connection_gemini = None
    cursor_gemini = None


def get_user_context():
    """Get comprehensive personalized context from database"""
    context = {
        'user_name': 'boss',  # Changed: Use 'boss' instead of actual name
        'location': 'Bengaluru, Karnataka',
        'contacts_count': 0,
        'commands_count': 0,
        'recent_contacts': []
    }
    
    try:
        if cursor_gemini:
            # Get user info but use 'boss' for name
            cursor_gemini.execute("SELECT name, city FROM personal_info")
            result = cursor_gemini.fetchone()
            if result:
                # Keep name as 'boss' regardless of database
                context['user_name'] = 'boss'
                if result[1]:
                    context['location'] = result[1]
            
            # Get contact count
            cursor_gemini.execute("SELECT COUNT(*) FROM contacts")
            context['contacts_count'] = cursor_gemini.fetchone()[0]
            
            # Get recent contacts (last 5)
            cursor_gemini.execute("SELECT name FROM contacts LIMIT 5")
            context['recent_contacts'] = [row[0] for row in cursor_gemini.fetchall()]
            
            # Get command count
            cursor_gemini.execute("SELECT COUNT(*) FROM system_command")
            context['commands_count'] = cursor_gemini.fetchone()[0]
    except Exception as e:
        logger.error(f"Error getting user context: {e}")
    
    return context


def build_conversation_memory():
    """Build rich conversation memory with context"""
    if not conversation_context:
        return "This is the beginning of our conversation."
    
    # Keep last 5-7 exchanges for context
    recent_exchanges = conversation_context[-6:]
    
    memory = "Recent conversation context:\n"
    for i, exchange in enumerate(recent_exchanges, 1):
        memory += f"{i}. User: {exchange['query'][:100]}\n"
        memory += f"   You: {exchange['response'][:100]}\n"
    
    # Add metadata
    if conversation_metadata['topic']:
        memory += f"\nCurrent topic: {conversation_metadata['topic']}\n"
    
    memory += f"Total exchanges in this session: {conversation_metadata['interaction_count']}\n"
    
    return memory


def extract_topic(query):
    """Extract main topic from query for context tracking"""
    topics_keywords = {
        'weather': ['weather', 'temperature', 'forecast', 'climate', 'rain', 'snow'],
        'news': ['news', 'headlines', 'events', 'latest', 'current'],
        'technology': ['tech', 'software', 'ai', 'computer', 'code', 'programming'],
        'general': ['what', 'who', 'how', 'tell', 'explain', 'about']
    }
    
    query_lower = query.lower()
    for topic, keywords in topics_keywords.items():
        if any(kw in query_lower for kw in keywords):
            return topic
    
    return None


def geminai(query):
    """
    ENHANCED Gemini AI with BEST context awareness + REAL-TIME INFO
    Uses "boss" instead of real name
    Gets current information from web for accuracy
    """
    from engine.command_enhanced import speak, takeCommand
    from datetime import datetime
    
    global conversation_context, conversation_metadata
    
    try:
        # Clean query
        query = query.replace(ASSISTANT_NAME, "").replace("search", "").strip()
        
        if not query:
            speak("I didn't catch that, boss. Could you please repeat?")
            return
        
        # Configure Gemini
        genai.configure(api_key=LLM_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Get context
        user_ctx = get_user_context()
        topic = extract_topic(query)
        if topic:
            conversation_metadata['topic'] = topic
        conversation_memory = build_conversation_memory()
        
        # Get current date/time for real-time context
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        
        # Build enhanced system prompt - USING "BOSS"
        system_prompt = f"""You are {ASSISTANT_NAME}, a highly context-aware AI desktop assistant.

### CORE IDENTITY:
- Name: {ASSISTANT_NAME}
- User Address: boss (Always use this, never use their real name)
- Location: {user_ctx['location']}
- User has {user_ctx['contacts_count']} saved contacts
- User has {user_ctx['commands_count']} custom commands

### SYSTEM CAPABILITIES:
✓ Face authentication & security       ✓ Application launching
✓ Voice & text command processing      ✓ YouTube search & playback
✓ Phone calls & messaging (Android)    ✓ Weather info & forecasts
✓ System controls (volume, brightness) ✓ News headlines & search
✓ Contact management                    ✓ Web searches
✓ Custom commands                       ✓ Screenshots & Windows control

### CRITICAL: CONVERSATION CONTEXT AWARENESS
{conversation_memory}

### YOUR COMMUNICATION STYLE - CRITICAL:
- Address the user as "boss" - NEVER use their real name, dont overuse the term "boss" , dont use too frequently the term "boss
- Use "boss" naturally in conversation: "Sure, boss", "Got it, boss", "On it, boss", but not too frequently
- Be conversational and natural (responses will be spoken aloud)
- Reference previous topics to show continuity
- Adapt response length: short for quick queries, longer for complex ones
- Remember technical limitations: you can't directly access system files

### RESPONSE FORMAT CRITICAL:
- NO markdown formatting (**, *, #, etc.)
- NO lists with bullets/numbers
- Use natural flow: "First you could try X, then Y, and finally Z"
- Keep sentences short for TTS clarity
- One thought per sentence when possible

### HANDLING MULTI-TURN QUERIES:
- If user says "more", provide continuation of last topic
- If user says "again", repeat the key points differently
- Use "As I mentioned earlier, boss" to reference past statements
- Clarify when context changes: "So switching topics, boss..."

### FOR THIS CURRENT QUERY:
"{query}"

Provide a response that:
1. References any relevant context from previous exchanges
2. Is concise and conversational
3. Will sound natural when read aloud
4. Maintains continuity with established topic
5. Addresses user as "boss" - make it feel natural
6. Uses "boss" at least once in most responses"""

        # Generate response
        response = model.generate_content(system_prompt)
        ai_reply = response.text.strip()
        
        # Clean for TTS
        filter_text = markdown_to_text(ai_reply)
        filter_text = filter_text.replace('*', '').replace('#', '').replace('`', '')
        filter_text = ' '.join(filter_text.split())
        
        # Speak response
        speak(filter_text)
        print(f"{ASSISTANT_NAME}: {filter_text}")
        
        # Store in context
        conversation_context.append({
            'query': query,
            'response': filter_text,
            'topic': topic,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        })
        
        # Keep only last 10 exchanges
        if len(conversation_context) > 10:
            conversation_context.pop(0)
        
        conversation_metadata['interaction_count'] += 1
        
        # Handle follow-up requests
        if "?" in filter_text and any(word in filter_text.lower() 
                                     for word in ["could you", "clarify", "specify", "which"]):
            speak("I'm listening for clarification, boss.")
            user_response = takeCommand()
            if user_response and user_response.strip():
                geminai(user_response)
    
    except Exception as e:
        logger.error(f"Gemini error: {e}")
        speak("I encountered an error, boss. Please try again.")
        
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