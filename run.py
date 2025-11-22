"""
Main Entry Point for AI Desktop Virtual Assistant
Dual Mode: Always-on Hotword Detection + Optional Background Mode
"""

import subprocess
import multiprocessing
import os
import sys
import logging
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def start_assistant():
    """Start the main assistant with UI"""
    print("="*60)
    print("Starting AI Desktop Virtual Assistant...")
    print("="*60)
    
    try:
        from main import start
        start()
    except KeyboardInterrupt:
        logger.info("Assistant stopped by user")
    except Exception as e:
        logger.error(f"Error starting assistant: {e}")
        input("Press Enter to exit...")


def listen_hotword():
    """
    Always-on hotword detection using speech recognition
    This works independently of the background button
    Responds without opening window when minimized
    """
    print("🎤 Hotword listener starting...")
    import speech_recognition as sr
    
    recognizer = sr.Recognizer()
    # Hotwords to detect
    hotwords = ["jarvis", "alexa", "computer", "hey computer", "hey bro"]
    
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                try:
                    # Listen for short phrases
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
                    text = recognizer.recognize_google(audio, language='en-in').lower()
                    
                    # Check if hotword detected
                    if any(hotword in text for hotword in hotwords):
                        logger.info(f"Hotword detected: {text}")
                        
                        # Process command in background WITHOUT opening window
                        try:
                            from engine.system_commands import execute_system_command
                            from engine.command_enhanced import speak, takeCommand
                            from engine.nlp import enhance_query_understanding
                            from engine.api_handler import handle_api_request
                            
                            speak("Yes, I'm listening")
                            
                            # Listen for command
                            command = takeCommand()
                            if command:
                                logger.info(f"Command received: {command}")
                                
                                # Try system command first (fast)
                                if not execute_system_command(command):
                                    # NLP processing
                                    nlp_result = enhance_query_understanding(command)
                                    intent = nlp_result['intent']
                                    entities = nlp_result['entities']
                                    
                                    # Handle based on intent
                                    if intent in ['weather', 'news', 'time_query', 'date_query', 'system_info']:
                                        response = handle_api_request(intent, entities, command)
                                        if response:
                                            speak(response)
                                    elif intent == 'greeting':
                                        speak("Hello! How can I help you?")
                                    elif intent == 'farewell':
                                        speak("Goodbye!")
                                    else:
                                        # For complex commands that need UI, inform user
                                        speak("That command requires the main window. Press Win J to open.")
                        
                        except Exception as e:
                            logger.error(f"Command processing error: {e}")
                        
                        # Wait before listening again
                        time.sleep(5)
                
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    logger.error(f"Hotword recognition error: {e}")
                    time.sleep(1)
                    
        except Exception as e:
            logger.error(f"Hotword listener error: {e}")
            time.sleep(2)


# def check_requirements():
#     """Check if all required packages are installed"""
#     required_packages = [
#         'eel', 'speech_recognition', 'pyttsx3', 'opencv-python',
#         'nltk', 'requests', 'psutil', 'pyautogui', 'google-generativeai'
#     ]
    
#     missing = []
#     for package in required_packages:
#         try:
#             __import__(package.replace('-', '_'))
#         except ImportError:
#             missing.append(package)
    
#     if missing:
#         print("\n Missing required packages:")
#         print(f"   {', '.join(missing)}")
#         print("\n Install them with:")
#         print(f"   pip install {' '.join(missing)}")
#         print()
#         return False
    
#     return True

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = {
        'eel': 'eel',
        'speech_recognition': 'speech_recognition',
        'pyttsx3': 'pyttsx3',
        'opencv-python': 'cv2',
        'nltk': 'nltk',
        'requests': 'requests',
        'psutil': 'psutil',
        'pyautogui': 'pyautogui',
        'google-generativeai': 'google.generativeai'
    }
    
    missing = []
    for pkg_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pkg_name)
    
    if missing:
        print("\n⚠️ Missing required packages:")
        print(f"   {', '.join(missing)}")
        print("\nInstall them with:")
        print(f"   pip install {' '.join(missing)}\n")
        return False
    
    return True



def initialize_nltk():
    """Initialize NLTK data"""
    try:
        from engine.nlp import initialize_nltk
        initialize_nltk()
        logger.info("NLTK initialized successfully")
    except Exception as e:
        logger.warning(f"NLTK initialization warning: {e}")


def setup_android_device():
    """Setup Android device connection (optional)"""
    try:
        if os.path.exists('device.bat'):
            logger.info("Setting up Android device connection...")
            subprocess.call(['device.bat'], timeout=30)
        else:
            logger.warning("device.bat not found. Android features may not work.")
    except Exception as e:
        logger.warning(f"Android setup warning: {e}")


if __name__ == '__main__':
    # Welcome message
    print("\n" + "="*60)
    print("🤖 AI DESKTOP VIRTUAL ASSISTANT (ADVA) v2.0")
    print("="*60)
    print("📋 Features:")
    print("   ✅ Face Authentication")
    print("   ✅ Always-on Hotword Detection (Jarvis, Alexa, Computer)")
    print("   ✅ Voice & Text Commands")
    print("   ✅ Natural Language Processing")
    print("   ✅ Optional Background Listening Mode (UI Button)")
    print("   ✅ System Controls (Volume, Brightness, etc.)")
    print("   ✅ External APIs (Weather, News, etc.)")
    print("   ✅ Phone Calls & Messages (Android)")
    print("   ✅ YouTube Integration")
    print("   ✅ Gemini AI Integration")
    print("="*60)
    print()
    
    # Check requirements
    print("🔍 Checking requirements...")
    if not check_requirements():
        sys.exit(1)
    print("✅ All requirements satisfied\n")
    
    # Initialize NLTK
    print("🧠 Initializing NLP engine...")
    initialize_nltk()
    print("✅ NLP engine ready\n")
    
    # Setup Android (optional)
    print("📱 Setting up Android device (optional)...")
    setup_android_device()
    print()
    
    # Instructions
    print("="*60)
    print("📖 HOW TO USE:")
    print("="*60)
    print("1. Face Authentication will start first")
    print("2. ALWAYS-ON HOTWORD (Works automatically):")
    print("   • Say 'Jarvis', 'Alexa', 'Computer', 'Hey Computer', 'Hey Bro'")
    print("   • Assistant activates automatically!")
    print()
    print("3. OTHER ACTIVATION METHODS:")
    print("   • Click Microphone button (one-time command)")
    print("   • Press Win+J keyboard shortcut")
    print("   • Type in text box")
    print()
    print("4. OPTIONAL BACKGROUND MODE (UI Button):")
    print("   • Click Background button for additional always-on mode")
    print("   • Say 'Hey Computer' to wake")
    print("   • Auto-sleeps after 15 seconds of inactivity")
    print("   • Say 'Stop' or 'Sleep Mode' to deactivate")
    print()
    print("💻 SYSTEM COMMANDS:")
    print("   • Volume up/down, Brightness up/down")
    print("   • Battery status, Close window, Switch tab")
    print("   • Screenshot, Lock system, and more!")
    print("="*60)
    print()
    
    # Start both processes
    try:
        p1 = multiprocessing.Process(target=start_assistant, name="MainAssistant")
        p2 = multiprocessing.Process(target=listen_hotword, name="HotwordListener", daemon=True)
        
        print("🚀 Starting main assistant...")
        p1.start()
        
        print("🎤 Starting always-on hotword listener...")
        p2.start()
        
        print("✅ All systems online!\n")
        
        # Wait for main process
        p1.join()
        
        # Cleanup
        if p2.is_alive():
            p2.terminate()
            p2.join()
        
        print("\n\n👋 Thank you for using ADVA!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Thank you for using ADVA!")
        if 'p1' in locals() and p1.is_alive():
            p1.terminate()
        if 'p2' in locals() and p2.is_alive():
            p2.terminate()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        input("\nPress Enter to exit...")