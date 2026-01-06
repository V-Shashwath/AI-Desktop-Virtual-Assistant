# import pvporcupine
# import pyaudio
# import struct
# import time
# def hotword():
#     porcupine=None
#     paud=None
#     audio_stream=None
#     try: 
#         #pre trained keywords
#         porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
#         paud=pyaudio.PyAudio()
#         audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
#         # loop for streaming
#         while True:
#             keyword=audio_stream.read(porcupine.frame_length)
#             keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

#             # processing keyword comes from mic 
#             keyword_index=porcupine.process(keyword)

#             # checking first keyword detetcted for not
#             if keyword_index>=0:
#                 print("hotword detected")

#                 # pressing shorcut key win+j
#                 import pyautogui as autogui
#                 autogui.keyDown("win")
#                 autogui.press("j")
#                 time.sleep(2)
#                 autogui.keyUp("win")
                
#     except:
#         if porcupine is not None:
#             porcupine.delete()
#         if audio_stream is not None:
#             audio_stream.close()
#         if paud is not None:
#             paud.terminate()


# hotword()



# from engine.features import whatsApp
# whatsApp("917204845870", "Hello, this is a test message", "call", "Nelli")


# import subprocess
# subprocess.run(["adb", "shell", "input tap 980 2250"])


# from engine.system_commands import volume_up

# volume_up()



# from asyncio.log import logger
# import time
# import pyautogui

# from engine.command import speak


# def minimize_window():
#     """Minimize current window - FIXED: Now actually minimizes"""
#     try:
#         pyautogui.hotkey('win', 'down')
#         speak("Window minimized")
#         logger.info("Window minimized")
#         time.sleep(0.5)
#         return True
#     except Exception as e:
#         logger.error(f"Minimize window error: {e}")
#         return False

# minimize_window()




# from gtts import gTTS

# def speak(text):
#     """
#     Text to speech with INDIAN ENGLISH ACCENT
#     Using gTTS
#     """
#     try:
#         text = str(text).strip()
#         if not text:
#             return
    
        
#         from gtts import gTTS
#         import io
#         from pydub import AudioSegment
#         from pydub.playback import play

#         tts = gTTS(text=text, lang='en', tld='co.in', slow=False)
        
#         audio_data = io.BytesIO()
#         tts.write_to_fp(audio_data)
#         audio_data.seek(0)
        
#         audio = AudioSegment.from_mp3(audio_data)
#         play(audio)
        
        
#     except Exception as e:
#         print(f"gTTS failed: {e}, falling back to pyttsx3.")


# speak("Hello, this is a test of Indian English accent using gTTS.")
    



# # Run this to test:
# from engine.command_enhanced import speak

# # Test 1: English with Indian accent
# speak("Hello boss, how can I help you today?")
# # You should hear: Natural Indian English voice! 🇮🇳

# # Test 2: Any English text
# speak("What would you like me to do?")
# # You should hear: Indian English accent!

# # Test 3: Boss address
# speak("Got it boss, I am on it")
# # You should hear: Indian English with "boss" addressed naturally


from engine.auth.recoganize import AuthenticateFace
AuthenticateFace()