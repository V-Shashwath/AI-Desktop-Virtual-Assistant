"""
PRODUCTION-LEVEL Background Hotword Listener
ALL COMMANDS WORK IN BACKGROUND MODE
Weather forecasts fixed, News fixed, Communication fixed, Tabs fixed
"""

import speech_recognition as sr
import time
import threading
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state
_listener_active = False
_listener_thread = None
_listener_enabled = True
_last_activity_time = None
_is_listening = False
_inactive_timeout = 15  # seconds

# Wake words and stop words
WAKE_WORDS = ["hey computer", "hey bro", "hey adva", "computer", "assistant"]
STOP_WORDS = ["stop listening", "go to sleep", "stop", "sleep mode", "deactivate"]


def is_wake_word(text):
    """Check if text contains wake word"""
    text_lower = text.lower().strip()
    for wake in WAKE_WORDS:
        if wake in text_lower:
            return True
    return False


def is_stop_word(text):
    """Check if text contains stop word"""
    text_lower = text.lower().strip()
    for stop in STOP_WORDS:
        if stop in text_lower:
            return True
    return False


def listen_for_command():
    """Listen for a single command with timeout"""
    global _last_activity_time, _is_listening
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            r.adjust_for_ambient_noise(source, duration=0.5)
            _is_listening = True
            logger.info("Listening for command...")
            
            # Listen with timeout
            audio = r.listen(source, timeout=10, phrase_time_limit=8)
            _is_listening = False
            
            # Recognize
            query = r.recognize_google(audio, language='en-in')
            logger.info(f"User said: {query}")
            _last_activity_time = time.time()
            return query.lower().strip()
            
        except sr.WaitTimeoutError:
            _is_listening = False
            logger.debug("Listen timeout")
            return None
        except sr.UnknownValueError:
            _is_listening = False
            logger.debug("Could not understand")
            return None
        except Exception as e:
            _is_listening = False
            logger.error(f"Recognition error: {e}")
            return None


def process_background_command(query):
    """
    PRODUCTION-LEVEL: Process command in background mode
    ALL COMMANDS ACCESSIBLE AND WORKING
    Returns command status
    """
    if not query:
        return
    
    try:
        from engine.system_commands import execute_system_command
        from engine.command_enhanced import speak
        from engine.nlp import enhance_query_understanding
        from engine.api_handler import handle_api_request
        
        # DISPLAY USER QUERY
        try:
            import eel
            eel.senderText(query)
        except:
            pass
        
        # Check if stop command
        if is_stop_word(query):
            speak("Going to sleep mode, boss. Say hey computer to wake me up.")
            return "STOP"
        
        logger.info(f"[BACKGROUND] Processing: {query}")
        
        # ========== TRY SYSTEM COMMANDS FIRST (HIGHEST PRIORITY) ==========
        # System commands like volume, brightness, battery, close tab, etc.
        if execute_system_command(query):
            logger.info("System command handled in background mode")
            return "HANDLED"
        
        # ========== NLP PROCESSING FOR OTHER COMMANDS ==========
        nlp_result = enhance_query_understanding(query)
        intent = nlp_result['intent']
        entities = nlp_result['entities']
        
        logger.info(f"[BACKGROUND] Intent: {intent}, Entities: {entities}")
        
        # ========== COMMAND ROUTING - PRODUCTION LEVEL ==========
        
        if intent == 'greeting':
            speak("Hey boss! What can I do for you?")
            return "HANDLED"
        
        elif intent == 'farewell':
            speak("See you later, boss. Say hey computer to wake me again.")
            return "HANDLED"
        
        # === API-BASED INTENTS (WEATHER, NEWS, TIME, etc.) ===
        elif intent in ['weather', 'news', 'time_query', 'date_query', 'system_info']:
            response = handle_api_request(intent, entities, query)
            if response:
                speak(response)
                return "HANDLED"
        
        # === WEB SEARCH ===
        elif intent == 'web_search':
            search_query = entities.get('search_query', query)
            import webbrowser
            speak(f"Searching for {search_query}, boss")
            webbrowser.open(f"https://www.google.com/search?q={search_query.replace(' ', '+')}")
            return "HANDLED"
        
        # === YOUTUBE ===
        elif intent in ['youtube_play', 'youtube_search']:
            from engine.features import playYoutube, searchYoutube
            if intent == 'youtube_search':
                searchYoutube(query)
            else:
                playYoutube(query)
            return "HANDLED"
        
        # === OPEN APPS ===
        elif intent == 'open_app':
            app_name = entities.get('app_name', '')
            if app_name:
                from engine.features import openCommand
                openCommand(query)
                return "HANDLED"
        
        # === COMMUNICATION (CALLS, MESSAGES, VIDEO CALLS) ===
        elif intent in ['send_message', 'make_call', 'video_call']:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            
            contact_no, name = findContact(query)
            if contact_no != 0:
                if intent == 'video_call' or 'video' in query:
                    speak(f"Starting WhatsApp video call with {name}, boss")
                    whatsApp(contact_no, "", "video call", name)
                elif intent == 'make_call':
                    speak(f"Calling {name}, boss")
                    makeCall(name, contact_no)
                elif intent == 'send_message':
                    speak(f"What message should I send to {name}, boss?")
                    message = listen_for_command()
                    if message:
                        speak(f"Sending message to {name}, boss")
                        sendMessage(message, contact_no, name)
                return "HANDLED"
        
        # === GENERAL QUERIES ===
        elif intent == 'general_query':
            response = handle_api_request(intent, entities, query)
            if response:
                speak(response)
                return "HANDLED"
            # Try Gemini AI
            from engine.features import geminai
            geminai(query)
            return "HANDLED"
        
        # === FALLBACK: Gemini AI ===
        else:
            from engine.features import geminai
            geminai(query)
            return "HANDLED"
            
    except Exception as e:
        logger.error(f"Error processing background command: {e}", exc_info=True)
        return None


def background_listener_loop():
    """Main background listener loop - PRODUCTION LEVEL"""
    global _listener_active, _last_activity_time, _is_listening
    
    logger.info("Background listener started")
    r = sr.Recognizer()
    
    # Initially in sleep mode
    in_sleep_mode = True
    
    while _listener_active:
        try:
            # Check if we should go to sleep
            if not in_sleep_mode and _last_activity_time:
                inactive_time = time.time() - _last_activity_time
                if inactive_time > _inactive_timeout:
                    logger.info("Going to sleep mode due to inactivity")
                    in_sleep_mode = True
                    _last_activity_time = None
            
            # Listen for wake word or command
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.3)
                
                try:
                    # Short listen for wake word
                    audio = r.listen(source, timeout=2, phrase_time_limit=4)
                    text = r.recognize_google(audio, language='en-in')
                    text_lower = text.lower().strip()
                    
                    logger.info(f"[BACKGROUND] Heard: {text}")
                    
                    # Check for wake word
                    if in_sleep_mode:
                        if is_wake_word(text_lower):
                            logger.info("Wake word detected!")
                            from engine.command_enhanced import speak
                            speak("Yes, I'm listening, boss")
                            in_sleep_mode = False
                            _last_activity_time = time.time()
                            
                            # Wait for command
                            time.sleep(0.5)
                            command = listen_for_command()
                            if command:
                                result = process_background_command(command)
                                if result == "STOP":
                                    in_sleep_mode = True
                                    _last_activity_time = None
                    
                    # Already active, process command
                    else:
                        result = process_background_command(text_lower)
                        if result == "STOP":
                            in_sleep_mode = True
                            _last_activity_time = None
                        elif result == "HANDLED":
                            _last_activity_time = time.time()
                
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    logger.error(f"Listener error: {e}")
                    time.sleep(1)
        
        except Exception as e:
            logger.error(f"Background listener error: {e}", exc_info=True)
            time.sleep(2)
    
    logger.info("Background listener stopped")


def start_background_listener():
    """Start the background listener thread"""
    global _listener_active, _listener_thread, _listener_enabled
    
    if not _listener_enabled:
        logger.info("Background listener is disabled")
        return False
    
    if _listener_active:
        logger.warning("Background listener already running")
        return False
    
    _listener_active = True
    _listener_thread = threading.Thread(target=background_listener_loop, daemon=True)
    _listener_thread.start()
    logger.info("Background listener thread started")
    return True


def stop_background_listener():
    """Stop the background listener"""
    global _listener_active, _listener_thread
    
    if not _listener_active:
        return False
    
    _listener_active = False
    if _listener_thread:
        _listener_thread.join(timeout=3)
    
    logger.info("Background listener stopped")
    return True


def toggle_background_listener():
    """Toggle background listener on/off"""
    global _listener_enabled
    
    if _listener_active:
        stop_background_listener()
        _listener_enabled = False
        return False
    else:
        _listener_enabled = True
        start_background_listener()
        return True


def is_listener_active():
    """Check if listener is active"""
    return _listener_active


def is_listener_enabled():
    """Check if listener is enabled"""
    return _listener_enabled


def get_listener_status():
    """Get detailed listener status"""
    return {
        'active': _listener_active,
        'enabled': _listener_enabled,
        'listening': _is_listening,
        'last_activity': _last_activity_time
    }