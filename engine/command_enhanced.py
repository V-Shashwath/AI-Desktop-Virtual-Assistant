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
        
        # Display recognized query in chat history immediately
        safe_eel_call('senderText', query)
        safe_eel_call('DisplayMessage', query)
        time.sleep(0.5)
        
        # Return original query (not lowercase) so it can be displayed properly
        return query.strip()
        
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
                # Query already displayed in takeCommand(), no need to display again
            else:
                query = str(message).strip()
                # Display text input in chat history
                safe_eel_call('senderText', query)
            
            if not query:
                safe_eel_call('ShowHood')
                return
            
            # Convert to lowercase for processing but keep original for display
            query_lower = query.lower().strip()
            
            logger.info(f"[{input_mode.upper()}] Query: {query}")
            
            # Convert to lowercase for processing
            query_lower = query.lower().strip()
            
            # ========== HANDLE MULTI-STEP CONTEXT ==========
            if command_context:
                handle_context_command(query_lower, input_mode)
                return
            
            # ========== HANDLE SINGLE-WORD COMMANDS ==========
            # Single words that might be incomplete system commands
            single_word_commands = {
                'up': 'volume up',
                'down': 'volume down',
                'volume': None,  # Ask for clarification
                'brightness': None,  # Ask for clarification
                'bright': 'brightness up',
                'dim': 'brightness down'
            }
            
            if len(query_lower.split()) == 1 and query_lower in single_word_commands:
                mapped_command = single_word_commands[query_lower]
                if mapped_command:
                    # Map to full command
                    if execute_system_command(mapped_command):
                        logger.info(f"Single word command '{query_lower}' mapped to '{mapped_command}'")
                        safe_eel_call('ShowHood')
                        return
                else:
                    # Ask for clarification
                    if query_lower == 'volume':
                        speak("Do you want to increase or decrease the volume, boss?")
                    elif query_lower == 'brightness':
                        speak("Do you want to increase or decrease the brightness, boss?")
                    safe_eel_call('ShowHood')
                    return
            
            # ========== CHECK WEATHER/NEWS FIRST (BEFORE SYSTEM COMMANDS) ==========
            # Weather and News should use APIs, not Gemini - check immediately
            weather_keywords = ['weather', 'temperature', 'forecast', 'climate', 'rain', 'snow', 'humid', 'wind', 'weather in', 'weather at', 'weather for']
            news_keywords = ['news', 'headlines', 'latest news', 'current events', 'breaking news', 'today\'s news', 'sports headlines', 'tech news', 'business news']
            
            # Check for weather queries FIRST (before system commands or NLP)
            if any(keyword in query_lower for keyword in weather_keywords):
                logger.info(f"[PRIORITY] Detected weather query: {query}")
                try:
                    from engine.api_handler import handle_api_request
                    # Extract location from query if present
                    entities = {}
                    import re
                    location_match = re.search(r'(?:weather|temperature|forecast)\s+(?:in|at|for)\s+(\w+)', query_lower)
                    if location_match:
                        entities['location'] = location_match.group(1).title()
                    api_response = handle_api_request('weather', entities, query)
                    if api_response and api_response.strip():
                        error_indicators = ["error", "couldn't", "not configured", "not found", "taking too long"]
                        if not any(indicator in api_response.lower() for indicator in error_indicators):
                            speak(api_response)
                        else:
                            speak(api_response)
                    else:
                        speak("I couldn't fetch weather information, boss. Please check your internet connection and try again.")
                except Exception as e:
                    logger.error(f"Weather request error: {e}", exc_info=True)
                    speak("I encountered an error while getting weather information, boss. Please try again.")
                safe_eel_call('ShowHood')
                return
            
            # Check for news queries FIRST (before system commands or NLP)
            if any(keyword in query_lower for keyword in news_keywords):
                logger.info(f"[PRIORITY] Detected news query: {query}")
                try:
                    from engine.api_handler import handle_api_request
                    # Extract category from query if present
                    entities = {}
                    categories = ['sports', 'technology', 'business', 'entertainment', 'health', 'science']
                    for cat in categories:
                        if cat in query_lower:
                            entities['category'] = cat
                            break
                    api_response = handle_api_request('news', entities, query)
                    if api_response and api_response.strip():
                        error_indicators = ["error", "couldn't", "not configured", "not found", "timed out"]
                        if not any(indicator in api_response.lower() for indicator in error_indicators):
                            speak(api_response)
                        else:
                            speak(api_response)
                    else:
                        speak("I couldn't fetch news information, boss. Please check your internet connection and try again.")
                except Exception as e:
                    logger.error(f"News request error: {e}", exc_info=True)
                    speak("I encountered an error while getting news information, boss. Please try again.")
                safe_eel_call('ShowHood')
                return
            
            # ========== TRY SYSTEM COMMANDS (HIGHEST PRIORITY) ==========
            # System commands should work immediately without NLP
            # Use query_lower for system command matching
            if execute_system_command(query_lower):
                logger.info("System command executed")
                safe_eel_call('ShowHood')
                return
            
            # ========== NLP PROCESSING FOR OTHER COMMANDS ==========
            enhanced_query = improve_query_with_context(query_lower)
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
            # Check both intent and explicit keywords for weather/news (secondary check after NLP)
            weather_keywords_secondary = ['weather', 'temperature', 'forecast', 'climate', 'rain', 'snow', 'humid', 'wind']
            news_keywords_secondary = ['news', 'headlines', 'latest news', 'current events', 'breaking news', 'today\'s news']
            
            # Explicit weather check
            if intent == 'weather' or any(keyword in query_lower for keyword in weather_keywords):
                logger.info(f"Processing weather request: {query}, Intent: {intent}, Entities: {entities}")
                try:
                    api_response = handle_api_request('weather', entities, query)
                    if api_response and api_response.strip():
                        # Check if response indicates an error
                        error_indicators = ["error", "couldn't", "not configured", "not found", "taking too long"]
                        if not any(indicator in api_response.lower() for indicator in error_indicators):
                            speak(api_response)
                        else:
                            logger.warning(f"Weather API returned error: {api_response}")
                            speak(api_response)  # Speak the error message so user knows what went wrong
                    else:
                        logger.warning(f"Weather API returned None or empty response")
                        speak("I couldn't fetch weather information, boss. Please check your internet connection and try again.")
                except Exception as e:
                    logger.error(f"Weather request error: {e}", exc_info=True)
                    speak("I encountered an error while getting weather information, boss. Please try again.")
                safe_eel_call('ShowHood')
                return
            
            # Explicit news check
            if intent == 'news' or any(keyword in query_lower for keyword in news_keywords):
                logger.info(f"Processing news request: {query}, Intent: {intent}, Entities: {entities}")
                try:
                    api_response = handle_api_request('news', entities, query)
                    if api_response and api_response.strip():
                        # Check if response indicates an error
                        error_indicators = ["error", "couldn't", "not configured", "not found", "timed out"]
                        if not any(indicator in api_response.lower() for indicator in error_indicators):
                            speak(api_response)
                        else:
                            logger.warning(f"News API returned error: {api_response}")
                            speak(api_response)  # Speak the error message so user knows what went wrong
                    else:
                        logger.warning(f"News API returned None or empty response")
                        speak("I couldn't fetch news information, boss. Please check your internet connection and try again.")
                except Exception as e:
                    logger.error(f"News request error: {e}", exc_info=True)
                    speak("I encountered an error while getting news information, boss. Please try again.")
                safe_eel_call('ShowHood')
                return
            
            # Other API intents (time, date, system_info)
            if intent in ['time_query', 'date_query', 'system_info']:
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
            # BUT FIRST: Check if it's actually a weather/news query that was misclassified
            weather_keywords_fallback = ['weather', 'temperature', 'forecast', 'climate', 'rain', 'snow', 'humid', 'wind', 'weather in', 'weather at']
            news_keywords_fallback = ['news', 'headlines', 'latest news', 'current events', 'breaking news', 'today\'s news', 'tell me news', 'what\'s the news']
            
            # Double-check for weather/news even if intent is general_query
            if intent == 'general_query':
                # Check if it's actually a weather query
                if any(keyword in query_lower for keyword in weather_keywords_fallback):
                    logger.info(f"Detected weather query in general_query: {query}")
                    try:
                        api_response = handle_api_request('weather', entities, query)
                        if api_response and api_response.strip():
                            error_indicators = ["error", "couldn't", "not configured", "not found", "taking too long"]
                            if not any(indicator in api_response.lower() for indicator in error_indicators):
                                speak(api_response)
                            else:
                                speak(api_response)
                        else:
                            speak("I couldn't fetch weather information, boss. Please check your internet connection and try again.")
                    except Exception as e:
                        logger.error(f"Weather request error: {e}", exc_info=True)
                        speak("I encountered an error while getting weather information, boss. Please try again.")
                    safe_eel_call('ShowHood')
                    return
                
                # Check if it's actually a news query
                if any(keyword in query_lower for keyword in news_keywords_fallback):
                    logger.info(f"Detected news query in general_query: {query}")
                    try:
                        api_response = handle_api_request('news', entities, query)
                        if api_response and api_response.strip():
                            error_indicators = ["error", "couldn't", "not configured", "not found", "timed out"]
                            if not any(indicator in api_response.lower() for indicator in error_indicators):
                                speak(api_response)
                            else:
                                speak(api_response)
                        else:
                            speak("I couldn't fetch news information, boss. Please check your internet connection and try again.")
                    except Exception as e:
                        logger.error(f"News request error: {e}", exc_info=True)
                        speak("I encountered an error while getting news information, boss. Please try again.")
                    safe_eel_call('ShowHood')
                    return
                
                # If it's truly a general query (not weather/news), try API first, then Gemini
                api_response = handle_api_request(intent, entities, query)
                if api_response:
                    speak(api_response)
                else:
                    from engine.features import geminai
                    geminai(query)
                safe_eel_call('ShowHood')
                return
            
            # === FALLBACK: Gemini AI ===
            # Final check: Even in fallback, check for weather/news keywords
            weather_keywords_final = ['weather', 'temperature', 'forecast', 'climate']
            news_keywords_final = ['news', 'headlines', 'latest news']
            
            if any(keyword in query_lower for keyword in weather_keywords_final):
                logger.info(f"Fallback: Detected weather query: {query}")
                try:
                    api_response = handle_api_request('weather', entities, query)
                    if api_response and api_response.strip():
                        speak(api_response)
                    else:
                        speak("I couldn't fetch weather information, boss. Please try again.")
                except Exception as e:
                    logger.error(f"Weather fallback error: {e}")
                    speak("I encountered an error while getting weather information, boss.")
                safe_eel_call('ShowHood')
                return
            
            if any(keyword in query_lower for keyword in news_keywords_final):
                logger.info(f"Fallback: Detected news query: {query}")
                try:
                    api_response = handle_api_request('news', entities, query)
                    if api_response and api_response.strip():
                        speak(api_response)
                    else:
                        speak("I couldn't fetch news information, boss. Please try again.")
                except Exception as e:
                    logger.error(f"News fallback error: {e}")
                    speak("I encountered an error while getting news information, boss.")
                safe_eel_call('ShowHood')
                return
            
            # Only use Gemini if it's truly not a weather/news query
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