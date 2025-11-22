"""
Enhanced Command Processing Module - FIXED
Integrates NLP and API handlers with existing command system
All commands accessible in both normal and background mode
"""

import pyttsx3
import speech_recognition as sr
import eel
import time
from engine.helper import extract_yt_term
from engine.nlp import enhance_query_understanding, improve_query_with_context, is_follow_up_query
from engine.api_handler import handle_api_request
from engine.system_commands import execute_system_command
import logging
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
try:
    connection = sqlite3.connect("adva.db", check_same_thread=False)
    cursor = connection.cursor()
except:
    connection = None
    cursor = None

# Global context for multi-step commands
command_context = {}


def speak(text):
    """Text to speech with error handling"""
    try:
        text = str(text)
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 174)
        eel.DisplayMessage(text)
        engine.say(text)
        eel.receiverText(text)
        engine.runAndWait()
    except Exception as e:
        logger.error(f"Speech error: {e}")


def takeCommand():
    """
    Listen to microphone and convert to text
    Returns query string or empty string on error
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            logger.warning("Listening timeout")
            return ""
    
    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
        time.sleep(1.5)
        return query.lower()
        
    except sr.UnknownValueError:
        logger.warning("Could not understand audio")
        return ""
    except sr.RequestError as e:
        logger.error(f"Recognition service error: {e}")
        return ""
    except Exception as e:
        logger.error(f"Recognition error: {e}")
        return ""


def get_gemini_context():
    """Get personalized context for Gemini from database"""
    context = {
        'user_name': 'User',
        'location': 'Bengaluru, Karnataka, IN',
        'has_contacts': False,
        'has_commands': False
    }
    
    try:
        if cursor:
            # Get user info
            cursor.execute("SELECT name, city FROM personal_info")
            result = cursor.fetchone()
            if result:
                if result[0]:
                    context['user_name'] = result[0]
                if result[1]:
                    context['location'] = result[1]
            
            # Check if user has contacts
            cursor.execute("SELECT COUNT(*) FROM contacts")
            contact_count = cursor.fetchone()[0]
            context['has_contacts'] = contact_count > 0
            
            # Check if user has custom commands
            cursor.execute("SELECT COUNT(*) FROM system_command")
            cmd_count = cursor.fetchone()[0]
            context['has_commands'] = cmd_count > 0
    except Exception as e:
        logger.error(f"Error getting context: {e}")
    
    return context


def expose_eel_functions():
    """
    Safely expose all Eel functions.
    Ensures functions are only exposed once to prevent AssertionError.
    """
    if "allCommands" not in eel._exposed_functions:

        @eel.expose
        def allCommands(message=1):
            """
            Enhanced command handler with NLP integration.
            Handles voice (message=1) or text (message=str) input.
            ALL COMMANDS ACCESSIBLE - No restrictions!
            """
            global command_context

            try:
                # Determine input mode
                input_mode = "voice" if message == 1 else "text"
                
                if input_mode == "voice":
                    query = takeCommand()
                else:
                    query = str(message).strip().lower()
                
                if not query:
                    eel.ShowHood()
                    return
                
                print(f"[Query] {query}")
                # DISPLAY USER QUERY IN CHAT - FIXED!
                eel.senderText(query)
                
                # Multi-step command context handling
                if command_context:
                    handle_context_command(query, input_mode)
                    return
                
                # NLP processing
                enhanced_query = improve_query_with_context(query)
                nlp_result = enhance_query_understanding(enhanced_query)
                intent = nlp_result.get('intent')
                entities = nlp_result.get('entities', {})
                confidence = nlp_result.get('confidence', 0.0)
                sub_type = nlp_result.get('sub_type')
                
                logger.info(f"Intent: {intent}, Confidence: {confidence:.2f}, Entities: {entities}")
                
                # ===== COMMAND ROUTING - ALL ACCESSIBLE =====
                
                # === GREETINGS ===
                if intent == 'greeting':
                    speak("Hello Boss! How can I help you?")
                    eel.ShowHood()
                    return
                
                if intent == 'farewell':
                    speak("Goodbye! Have a great day!")
                    eel.ShowHood()
                    return
                
                # === SYSTEM COMMANDS - ALL ACCESSIBLE ===
                if intent in ['volume_control', 'volume_down', 'mute', 'brightness_up', 
                             'brightness_down', 'battery_status', 'screenshot', 'window_close',
                             'window_minimize', 'window_maximize', 'lock_system', 'shutdown', 'restart']:
                    handled = execute_system_command(query)
                    if handled:
                        eel.ShowHood()
                        return
                
                # === APPLICATIONS ===
                if intent == 'open_app':
                    from engine.features import openCommand
                    openCommand(query)
                    eel.ShowHood()
                    return
                
                # === YOUTUBE ===
                if intent in ['youtube_play', 'youtube_search']:
                    from engine.features import playYoutube, searchYoutube
                    if intent == 'youtube_search':
                        searchYoutube(query)
                    else:
                        playYoutube(query)
                    eel.ShowHood()
                    return
                
                # === COMMUNICATION ===
                if intent in ['send_message', 'make_call', 'video_call']:
                    handle_communication_command(query, intent, entities, input_mode)
                    return
                
                # === EXTERNAL APIs ===
                if intent in ['weather', 'news', 'time_query', 'date_query', 'system_info']:
                    api_response = handle_api_request(intent, entities, query)
                    if api_response:
                        speak(api_response)
                    eel.ShowHood()
                    return
                
                # === WEB SEARCH ===
                if intent == 'web_search':
                    search_query = entities.get('search_query', query)
                    api_response = handle_api_request(intent, entities, query)
                    if api_response and "Let me search" not in api_response:
                        speak(api_response)
                    else:
                        import webbrowser
                        search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                        speak(f"Searching Google for {search_query}")
                        webbrowser.open(search_url)
                    eel.ShowHood()
                    return
                
                # === GENERAL QUERIES ===
                if intent == 'general_query':
                    api_response = handle_api_request(intent, entities, query)
                    if api_response:
                        speak(api_response)
                    else:
                        from engine.features import geminai
                        geminai(query)
                    eel.ShowHood()
                    return
                
                # === FALLBACK: Try system command ===
                if execute_system_command(query):
                    eel.ShowHood()
                    return
                
                # === FINAL FALLBACK: Gemini AI ===
                from engine.features import geminai
                geminai(query)
                
                eel.ShowHood()

            except Exception as e:
                logger.error(f"Command execution error: {e}")
                speak("I encountered an error processing your request.")
                eel.ShowHood()


def handle_communication_command(query, intent, entities, input_mode):
    """Handle calls and messages with multi-step flow"""
    global command_context
    
    from engine.features import findContact, whatsApp, makeCall, sendMessage
    
    # Get contact
    contact_no, name = findContact(query)
    if contact_no == 0:
        speak("I couldn't find that contact in your phone book.")
        eel.ShowHood()
        return
    
    # Video call - direct to WhatsApp
    if intent == 'video_call' or 'video' in query:
        speak(f"Starting WhatsApp video call with {name}")
        whatsApp(contact_no, "", "video call", name)
        eel.ShowHood()
        return
    
    # Ask for mode
    speak("Which mode do you want to use - WhatsApp or Mobile?")
    eel.DisplayMessage("Waiting for your response...")
    
    # Store context
    command_context = {
        "step": "mode",
        "contact": (contact_no, name),
        "original_query": query,
        "intent": intent,
        "input_mode": input_mode
    }
    
    # If voice mode, get response immediately
    if input_mode == "voice":
        time.sleep(1)
        mode = takeCommand()
        if mode:
            handle_mode_selection(mode)
    # For text mode, wait for next input
    eel.ShowHood()


def handle_mode_selection(mode):
    """Handle mode selection (Mobile/WhatsApp)"""
    global command_context
    
    mode = mode.lower().strip()
    
    if mode not in ["mobile", "whatsapp"]:
        speak("Please say Mobile or WhatsApp.")
        return
    
    contact_no, name = command_context["contact"]
    intent = command_context["intent"]
    command_context["preference"] = mode
    
    # If message
    if "message" in intent:
        speak("What message should I send?")
        eel.DisplayMessage("Listening for your message...")
        
        if command_context["input_mode"] == "voice":
            time.sleep(1)
            message_text = takeCommand()
            if message_text:
                send_final_message(message_text)
        else:
            command_context["step"] = "message"
            eel.ShowHood()
    # If call
    else:
        from engine.features import whatsApp, makeCall
        if "mobile" in mode:
            makeCall(name, contact_no)
        else:
            whatsApp(contact_no, "", "call", name)
        command_context = {}
        eel.ShowHood()


def send_final_message(message_text):
    """Send final message"""
    global command_context
    
    from engine.features import sendMessage, whatsApp
    
    contact_no, name = command_context["contact"]
    preference = command_context.get("preference", "mobile")
    
    if "mobile" in preference:
        sendMessage(message_text, contact_no, name)
    else:
        whatsApp(contact_no, message_text, "message", name)
    
    command_context = {}
    eel.ShowHood()


def handle_context_command(query, input_mode):
    """Handle commands within context (multi-step)"""
    global command_context
    
    step = command_context.get("step")
    
    # Mode selection
    if step == "mode":
        handle_mode_selection(query)
        return
    
    # Message text
    if step == "message":
        send_final_message(query)
        return