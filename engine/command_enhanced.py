"""
PRODUCTION-LEVEL Enhanced Command Processing
ALL COMMANDS WORK IN BOTH NORMAL AND BACKGROUND MODE
Comprehensive error handling and routing
"""

import pyttsx3
import speech_recognition as sr
import eel
import time
from engine.helper import extract_yt_term
from engine.nlp import enhance_query_understanding, improve_query_with_context
from engine.api_handler import handle_api_request
from engine.system_commands import execute_system_command
import logging
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    connection = sqlite3.connect("adva.db", check_same_thread=False)
    cursor = connection.cursor()
except:
    connection = None
    cursor = None

command_context = {}

# Safe eel calls wrapper
def safe_eel_call(func_name, *args):
    """Safely call eel functions with error handling"""
    try:
        func = getattr(eel, func_name, None)
        if func:
            func(*args)
    except Exception as e:
        logger.warning(f"Eel call {func_name} failed: {e}")


def speak(text):
    """Text to speech with comprehensive error handling"""
    try:
        text = str(text).strip()
        if not text:
            return
        
        # Try to display message
        safe_eel_call('DisplayMessage', text)
        
        # Initialize TTS engine
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        
        # Set voice (use female voice if available)
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
        
        engine.setProperty('rate', 174)
        engine.say(text)
        
        # Send to receiver
        safe_eel_call('receiverText', text)
        
        engine.runAndWait()
        engine.stop()
        
    except Exception as e:
        logger.error(f"Speech error: {e}")


def takeCommand():
    """Listen to microphone and convert to text - PRODUCTION LEVEL"""
    r = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logger.info("Starting voice input")
            safe_eel_call('DisplayMessage', "Listening...")
            
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=0.5)
            
            # Listen with timeout
            audio = r.listen(source, timeout=10, phrase_time_limit=8)
    
    except sr.WaitTimeoutError:
        logger.warning("Listening timeout - no audio detected")
        return ""
    except Exception as e:
        logger.error(f"Microphone error: {e}")
        return ""
    
    try:
        logger.info("Recognizing speech")
        safe_eel_call('DisplayMessage', "Recognizing...")
        
        query = r.recognize_google(audio, language='en-in')
        logger.info(f"User said: {query}")
        
        safe_eel_call('DisplayMessage', query)
        time.sleep(1.5)
        
        return query.lower().strip()
        
    except sr.UnknownValueError:
        logger.warning("Could not understand audio")
        return ""
    except sr.RequestError as e:
        logger.error(f"Recognition service error: {e}")
        return ""
    except Exception as e:
        logger.error(f"Recognition error: {e}")
        return ""


def expose_eel_functions():
    """Safely expose all Eel functions - PRODUCTION LEVEL"""
    
    # Check if already exposed
    if hasattr(eel, '_exposed_functions') and "allCommands" in eel._exposed_functions:
        return

    @eel.expose
    def allCommands(message=1):
        """
        PRODUCTION-LEVEL Enhanced command handler
        Works in both voice and text modes
        ALL COMMANDS WORK IN BOTH MODES
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
                safe_eel_call('ShowHood')
                return
            
            logger.info(f"[{input_mode.upper()}] Query: {query}")
            safe_eel_call('senderText', query)
            
            # ========== HANDLE MULTI-STEP CONTEXT ==========
            if command_context:
                handle_context_command(query, input_mode)
                return
            
            # ========== TRY SYSTEM COMMANDS FIRST (HIGHEST PRIORITY) ==========
            # System commands should work immediately without NLP
            if execute_system_command(query):
                logger.info("System command executed")
                safe_eel_call('ShowHood')
                return
            
            # ========== NLP PROCESSING FOR OTHER COMMANDS ==========
            enhanced_query = improve_query_with_context(query)
            nlp_result = enhance_query_understanding(enhanced_query)
            intent = nlp_result.get('intent')
            entities = nlp_result.get('entities', {})
            confidence = nlp_result.get('confidence', 0.0)
            
            logger.info(f"Intent: {intent}, Confidence: {confidence:.2f}, Entities: {entities}")
            
            # ========== COMMAND ROUTING - PRODUCTION LEVEL ==========
            
            # === GREETINGS ===
            if intent == 'greeting':
                speak("Hey boss! What can I do for you?")
                safe_eel_call('ShowHood')
                return
            
            if intent == 'farewell':
                speak("See you later, boss!")
                safe_eel_call('ShowHood')
                return
            
            # === APPLICATIONS ===
            if intent == 'open_app':
                from engine.features import openCommand
                openCommand(query)
                safe_eel_call('ShowHood')
                return
            
            # === YOUTUBE ===
            if intent in ['youtube_play', 'youtube_search']:
                from engine.features import playYoutube, searchYoutube
                if intent == 'youtube_search':
                    searchYoutube(query)
                else:
                    playYoutube(query)
                safe_eel_call('ShowHood')
                return
            
            # === COMMUNICATION (WORKS IN BOTH MODES) ===
            if intent in ['send_message', 'make_call', 'video_call']:
                handle_communication_command(query, intent, entities, input_mode)
                return
            
            # === EXTERNAL APIs (WEATHER, NEWS, TIME, DATE, etc.) ===
            if intent in ['weather', 'news', 'time_query', 'date_query', 'system_info']:
                api_response = handle_api_request(intent, entities, query)
                if api_response:
                    speak(api_response)
                else:
                    speak(f"I couldn't fetch {intent} information, boss. Please try again.")
                safe_eel_call('ShowHood')
                return
            
            # === WEB SEARCH ===
            if intent == 'web_search':
                search_query = entities.get('search_query', query)
                api_response = handle_api_request(intent, entities, query)
                
                if api_response and "search" not in api_response.lower():
                    speak(api_response)
                else:
                    import webbrowser
                    speak(f"Searching Google for {search_query}, boss")
                    webbrowser.open(f"https://www.google.com/search?q={search_query.replace(' ', '+')}")
                
                safe_eel_call('ShowHood')
                return
            
            # === GENERAL QUERIES ===
            if intent == 'general_query':
                api_response = handle_api_request(intent, entities, query)
                if api_response:
                    speak(api_response)
                else:
                    from engine.features import geminai
                    geminai(query)
                safe_eel_call('ShowHood')
                return
            
            # === FALLBACK: Gemini AI ===
            from engine.features import geminai
            geminai(query)
            safe_eel_call('ShowHood')

        except Exception as e:
            logger.error(f"Command execution error: {e}", exc_info=True)
            speak("I encountered an error, boss. Please try again.")
            safe_eel_call('ShowHood')


def handle_communication_command(query, intent, entities, input_mode):
    """Handle calls and messages - WORKS IN BOTH MODES - PRODUCTION LEVEL"""
    global command_context
    
    try:
        from engine.features import findContact, whatsApp, makeCall, sendMessage
        
        # Get contact
        contact_no, name = findContact(query)
        if contact_no == 0:
            speak("I couldn't find that contact, boss. Please try again.")
            safe_eel_call('ShowHood')
            return
        
        # Video call - direct to WhatsApp
        if intent == 'video_call' or 'video' in query:
            speak(f"Starting WhatsApp video call with {name}, boss")
            whatsApp(contact_no, "", "video call", name)
            safe_eel_call('ShowHood')
            return
        
        # Ask for mode (Mobile/WhatsApp)
        speak(f"Which mode, boss - WhatsApp or Mobile?")
        
        command_context = {
            "step": "mode",
            "contact": (contact_no, name),
            "original_query": query,
            "intent": intent,
            "input_mode": input_mode
        }
        
        # Voice mode: get response immediately
        if input_mode == "voice":
            time.sleep(0.5)
            mode = takeCommand()
            if mode:
                handle_mode_selection(mode)
                return
        
        safe_eel_call('ShowHood')
        
    except Exception as e:
        logger.error(f"Communication command error: {e}", exc_info=True)
        speak("I couldn't process your request, boss.")
        safe_eel_call('ShowHood')


def handle_mode_selection(mode):
    """Handle mode selection (Mobile/WhatsApp) - PRODUCTION LEVEL"""
    global command_context
    
    try:
        mode = mode.lower().strip()
        
        if mode not in ["mobile", "whatsapp"]:
            speak("Please say Mobile or WhatsApp, boss.")
            return
        
        contact_no, name = command_context["contact"]
        intent = command_context["intent"]
        command_context["preference"] = mode
        
        # If message
        if "message" in intent:
            speak(f"What message should I send to {name}, boss?")
            
            if command_context["input_mode"] == "voice":
                time.sleep(0.5)
                message_text = takeCommand()
                if message_text:
                    send_final_message(message_text)
            else:
                command_context["step"] = "message"
                safe_eel_call('ShowHood')
        
        # If call
        else:
            from engine.features import whatsApp, makeCall
            if "mobile" in mode:
                makeCall(name, contact_no)
            else:
                whatsApp(contact_no, "", "call", name)
            
            command_context = {}
            safe_eel_call('ShowHood')
    
    except Exception as e:
        logger.error(f"Mode selection error: {e}", exc_info=True)


def send_final_message(message_text):
    """Send message - PRODUCTION LEVEL"""
    global command_context
    
    try:
        from engine.features import sendMessage, whatsApp
        
        contact_no, name = command_context["contact"]
        preference = command_context.get("preference", "mobile")
        
        if "mobile" in preference:
            sendMessage(message_text, contact_no, name)
        else:
            whatsApp(contact_no, message_text, "message", name)
        
        command_context = {}
        safe_eel_call('ShowHood')
    
    except Exception as e:
        logger.error(f"Send message error: {e}", exc_info=True)


def handle_context_command(query, input_mode):
    """Handle multi-step commands - PRODUCTION LEVEL"""
    global command_context
    
    try:
        step = command_context.get("step")
        
        if step == "mode":
            handle_mode_selection(query)
            return
        
        if step == "message":
            send_final_message(query)
            return
    
    except Exception as e:
        logger.error(f"Context command error: {e}", exc_info=True)