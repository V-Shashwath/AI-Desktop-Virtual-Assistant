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
        target_tab = 14  # Message box tab position
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

    # Launch WhatsApp once (removed duplicate launch)
    full_command = f'start "" "{whatsapp_url}"'
    subprocess.run(full_command, shell=True)
    time.sleep(4)  # Wait for WhatsApp to open

    # Try to focus WhatsApp window
    try:
        windows = gw.getWindowsWithTitle('WhatsApp')
        if windows:
            windows[0].activate()
            time.sleep(1)
    except Exception as e:
        print(f"[!] Window activation failed: {e}")

    # For messages: URL already pre-fills the message, just send it
    if flag == 'message':
        # The message is already pre-filled in the text box via URL parameter
        # Wait for WhatsApp to fully load, then just press Enter to send
        # Do NOT navigate or type anything - the message is already there!
        time.sleep(2)  # Wait for WhatsApp to fully load with pre-filled message
        pyautogui.hotkey('enter')  # Send the pre-filled message
    else:
        # For calls/video calls: navigate using keyboard
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
    """Build conversation memory - LIMITED to prevent confusion"""
    if not conversation_context:
        return "This is a new conversation."
    
    # Only keep last 2 exchanges to prevent context confusion
    recent_exchanges = conversation_context[-3:]
    
    memory = "Previous conversation (only if relevant):\n"
    for i, exchange in enumerate(recent_exchanges, 1):
        memory += f"{i}. User asked: {exchange['query'][:80]}\n"
        memory += f"   You responded: {exchange['response'][:80]}\n"
    
    memory += "\nIMPORTANT: Only reference previous context if the current query is clearly a follow-up question. If it's a new topic, answer it directly without mentioning previous topics."
    
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
        original_query = query
        query = query.replace(ASSISTANT_NAME, "").replace("search", "").strip()
        
        if not query:
            speak("I didn't catch that, boss. Could you please repeat?")
            return
        
        # Check if this is a completely new topic (different from last query)
        # Clear context if topic changed significantly
        query_lower = query.lower().strip()
        if conversation_context:
            last_query = conversation_context[-1].get('query', '').lower()
            # If new query is completely different (no common words), clear old context
            if last_query and len(query_lower.split()) > 2:
                last_words = set(last_query.split())
                current_words = set(query_lower.split())
                # If less than 30% word overlap, it's a new topic
                if len(last_words.intersection(current_words)) / max(len(last_words), len(current_words)) < 0.3:
                    # Clear old context for new topic
                    conversation_context = []
                    conversation_metadata['topic'] = None
        
        # Configure Gemini
        genai.configure(api_key=LLM_KEY)
        
        # Get context
        user_ctx = get_user_context()
        topic = extract_topic(query)
        if topic:
            conversation_metadata['topic'] = topic
        
        # Only use recent context (last 2-3 exchanges max) to prevent confusion
        conversation_memory = build_conversation_memory()
        
        # Get current date/time for real-time context
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        
        # Build system instruction
        system_instruction = f"""You are {ASSISTANT_NAME}, a highly context-aware AI desktop assistant.

### CORE IDENTITY:
- Name: {ASSISTANT_NAME}
- User Address: boss (Always use this, never use their real name)
- Location: {user_ctx['location']}
- Current Date: {current_date}
- Current Time: {current_time}

### YOUR COMMUNICATION STYLE:
- Address the user as "boss" naturally (not too frequently)
- Be conversational and natural (responses will be spoken aloud)
- Focus on the CURRENT query - only reference previous topics if explicitly asked
- Adapt response length: short for quick queries, longer for complex ones

### RESPONSE FORMAT:
- NO markdown formatting (**, *, #, etc.)
- NO lists with bullets/numbers
- Use natural flow: "First X, then Y, and finally Z"
- Keep sentences short for TTS clarity
- One thought per sentence when possible

### CRITICAL:
- Answer the CURRENT query directly and completely
- DO NOT continue or reference previous topics unless the query explicitly asks for it
- If this is a new topic, ignore previous conversation context
- Be direct and focused on answering the current question"""

        # Create model - try with system instruction first, fallback if not supported
        try:
            model = genai.GenerativeModel(
                "gemini-2.5-flash",
                system_instruction=system_instruction
            )
        except Exception as e:
            logger.warning(f"System instruction not supported, using fallback: {e}")
            model = genai.GenerativeModel("gemini-2.5-flash")
            # Include system instruction in prompt instead
            system_instruction = f"""You are {ASSISTANT_NAME}. Address user as "boss" naturally. Be conversational. NO markdown. Current date: {current_date}."""
        
        # Build the actual prompt with context
        if conversation_memory and "new conversation" not in conversation_memory.lower():
            prompt = f"""{system_instruction}

{conversation_memory}

User's question: {query}

Answer this question directly. Do not reference previous topics unless the question explicitly asks about them."""
        else:
            prompt = f"""{system_instruction}

User's question: {query}

Provide a direct, complete answer."""

        # Generate response with timeout
        logger.info(f"Calling Gemini API for query: {query[:50]}...")
        try:
            response = model.generate_content(prompt)
            ai_reply = response.text.strip()
            logger.info(f"Gemini response received: {ai_reply[:100]}...")
        except Exception as e:
            error_str = str(e)
            logger.error(f"Gemini API call failed: {e}")
            
            # Handle specific error types
            if "429" in error_str or "quota" in error_str.lower() or "exceeded" in error_str.lower():
                # Quota exceeded - free tier limit
                speak("I've reached my daily request limit, boss. The free tier allows 20 requests per day. Please try again tomorrow or upgrade your API plan.")
                print(f"{ASSISTANT_NAME}: Daily quota exceeded. Free tier limit: 20 requests/day")
            elif "403" in error_str or "forbidden" in error_str.lower():
                # API key issue
                speak("There's an issue with my API access, boss. Please check the API key configuration.")
                print(f"{ASSISTANT_NAME}: API access forbidden. Check API key.")
            elif "401" in error_str or "unauthorized" in error_str.lower():
                # Invalid API key
                speak("My API key seems invalid, boss. Please check the configuration.")
                print(f"{ASSISTANT_NAME}: Unauthorized. Invalid API key.")
            else:
                # Generic error
                speak("I'm having trouble processing that right now, boss. Please try again in a moment.")
            return
        
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
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 3 exchanges to prevent context confusion
        if len(conversation_context) > 3:
            conversation_context = conversation_context[-3:]
        
        conversation_metadata['interaction_count'] += 1
        conversation_metadata['last_query_time'] = datetime.now()
        
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
    
    # Check ADB device authorization first
    is_connected, status = check_adb_device()
    
    if not is_connected:
        if status == "unauthorized":
            error_msg = f"Your Android device is not authorized, boss. Please check your phone and accept the USB debugging authorization dialog, then try again."
            speak(error_msg)
            print(f"[ADB Error]: Device unauthorized. Please accept authorization on your phone.")
            return
        elif status == "no_device":
            error_msg = f"No Android device found, boss. Please connect your device via USB or Wi-Fi and ensure ADB is enabled."
            speak(error_msg)
            print(f"[ADB Error]: No device connected.")
            return
        else:
            error_msg = f"Could not connect to Android device, boss. Please check your connection and try again."
            speak(error_msg)
            print(f"[ADB Error]: Connection issue - {status}")
            return
    
    speak("Calling "+name)
    
    try:
        result = subprocess.run(
            ["adb", "shell", "am", "start", "-a", "android.intent.action.CALL", "-d", f"tel:{mobileNo}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0 or "unauthorized" in result.stderr.lower():
            raise Exception("ADB command failed or device unauthorized")
            
    except subprocess.TimeoutExpired:
        speak("The call operation timed out, boss. Please check your device connection.")
        print("[ADB Error]: Call command timeout")
    except Exception as e:
        error_str = str(e).lower()
        if "unauthorized" in error_str:
            speak("Your device authorization was revoked, boss. Please accept the authorization dialog on your phone and try again.")
        else:
            speak(f"Failed to make call, boss. Please check your device connection.")
        print(f"[ADB Error]: {e}")


import subprocess
import time

def check_adb_device():
    """Check if ADB device is connected and authorized."""
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout
        
        # Check for unauthorized devices
        if "unauthorized" in output.lower():
            return False, "unauthorized"
        
        # Check for connected devices (device status)
        if "device" in output and "unauthorized" not in output:
            return True, "authorized"
        
        # No devices found
        if "no devices" in output.lower() or "List of devices" in output and "device" not in output:
            return False, "no_device"
        
        return False, "unknown"
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as e:
        print(f"[ADB Check Error]: {e}")
        return False, "error"

def sendMessage(message, mobileNo, name):
    """Send SMS via Google Messages using ADB automation."""
    # Check ADB device authorization first
    is_connected, status = check_adb_device()
    
    if not is_connected:
        if status == "unauthorized":
            error_msg = f"Your Android device is not authorized, boss. Please check your phone and accept the USB debugging authorization dialog, then try again."
            speak(error_msg)
            print(f"[ADB Error]: Device unauthorized. Please accept authorization on your phone.")
            return
        elif status == "no_device":
            error_msg = f"No Android device found, boss. Please connect your device via USB or Wi-Fi and ensure ADB is enabled."
            speak(error_msg)
            print(f"[ADB Error]: No device connected.")
            return
        else:
            error_msg = f"Could not connect to Android device, boss. Please check your connection and try again."
            speak(error_msg)
            print(f"[ADB Error]: Connection issue - {status}")
            return
    
    speak(f"Sending message to {name} via Google Messages")

    try:
        # --- Google Messages UI automation ---
        result = subprocess.run(
            ["adb", "shell", "am", "start",
             "-n", "com.google.android.apps.messaging/.ui.ConversationListActivity"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0 or "unauthorized" in result.stderr.lower():
            raise Exception("ADB command failed or device unauthorized")
        
        time.sleep(2)

        # Tap "Start chat" button
        subprocess.run(["adb", "shell", "input", "tap", "800", "2200"], timeout=5)
        time.sleep(1)

        # Type contact number
        subprocess.run(["adb", "shell", f"input text {mobileNo}"], timeout=5)
        subprocess.run(["adb", "shell", "input tap 980 2250"], timeout=5)  # Enter
        time.sleep(2)

        # Type the message (spaces must be escaped for ADB input)
        safe_message = message.replace(" ", "%s")
        subprocess.run(["adb", "shell", f"input text {safe_message}"], timeout=5)
        time.sleep(1)

        # Send the message
        time.sleep(1)
        subprocess.run(["adb", "shell", "input tap 950 1500"], timeout=5)  # tap SEND icon

        speak(f"Message sent successfully to {name}")
    except subprocess.TimeoutExpired:
        speak("The operation timed out, boss. Please check your device connection.")
        print("[ADB Error]: Command timeout")
    except Exception as e:
        error_str = str(e).lower()
        if "unauthorized" in error_str:
            speak("Your device authorization was revoked, boss. Please accept the authorization dialog on your phone and try again.")
        else:
            speak(f"Failed to send message, boss. Please check your device connection. Error: {str(e)[:50]}")
        print(f"[ADB Error]: {e}")



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