# import pyttsx3
# import speech_recognition as sr
# import eel
# import time
# import webbrowser   

# from engine.helper import extract_yt_term

# def speak(text):
#     text = str(text)
#     engine = pyttsx3.init('sapi5')
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[1].id)
#     engine.setProperty('rate', 150)
#     eel.DisplayMessage(text)
#     engine.say(text)
#     eel.receiverText(text)
#     engine.runAndWait()


# def takeCommand():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         eel.DisplayMessage("Listening...")
#         r.pause_threshold = 1
#         r.adjust_for_ambient_noise(source)

#         audio = r.listen(source, 12, 8 )
    
#     try:
#         print("Recognizing...")
#         eel.DisplayMessage("Recognizing...")
#         query = r.recognize_google(audio, language='en-in')
#         print(f"User said: {query}\n")
#         eel.DisplayMessage(query)
#         time.sleep(2)
        

#     except Exception as e:
#         return ""

#     return query.lower()    


# # text = takeCommand()
# # speak(text)

# import pyttsx3
# import speech_recognition as sr
# import eel
# import time
# import webbrowser
# from engine.helper import extract_yt_term

# # Keep a global context to handle multi-step commands
# command_context = {}

# @eel.expose
# def allCommands(message=1):
#     """
#     Handles all commands from user, either via voice (message=1) or text (message=str)
#     Supports multi-step flows for messaging and calling.
#     """
#     global command_context
#     try:
#         # -------- GET QUERY -------- #
#         if message == 1:
#             query = takeCommand()
#         else:
#             query = str(message).strip().lower()
        
#         print("Query:", query)
#         eel.senderText(query)

#         # -------- CHECK CONTEXT FOR MULTI-STEP -------- #
#         if command_context:
#             step = command_context.get("step")
            
#             # Step 1: mode selected
#             if step == "mode":
#                 command_context["preference"] = query
#                 if "send message" in command_context["original_query"] or "send sms" in command_context["original_query"] or "send a message" in command_context["original_query"]:
#                     speak("What message should I send?")
#                     command_context["step"] = "message"
#                     eel.ShowHood()
#                     return
#                 else:
#                     # It's a call, execute immediately
#                     contact_no, name = command_context["contact"]
#                     pref = command_context["preference"]
#                     if "mobile" in pref:
#                         from engine.features import makeCall
#                         makeCall(name, contact_no)
#                     elif "whatsapp" in pref:
#                         from engine.features import whatsApp
#                         whatsApp(contact_no, "", "call", name)
#                     command_context = {}
#                     eel.ShowHood()
#                     return
            
#             # Step 2: message typed
#             elif step == "message":
#                 contact_no, name = command_context["contact"]
#                 preference = command_context.get("preference", "mobile")
#                 message_text = query
#                 from engine.features import sendMessage, whatsApp
#                 if "mobile" in preference:
#                     sendMessage(message_text, contact_no, name)
#                 elif "whatsapp" in preference:
#                     whatsApp(contact_no, message_text, "message", name)
#                 command_context = {}
#                 eel.ShowHood()
#                 return

#         # -------- OPEN COMMANDS -------- #
#         if 'open' in query:
#             from engine.features import openCommand
#             openCommand(query)
#             eel.ShowHood()
#             return

#         # -------- YOUTUBE COMMANDS -------- #
#         elif 'youtube' in query:
#             from engine.features import playYoutube, searchYoutube
#             command_type, _ = extract_yt_term(query)
#             if command_type == 'search':
#                 searchYoutube(query)
#             else:
#                 playYoutube(query)
#             eel.ShowHood()
#             return

#         # -------- CALL & MESSAGE HANDLING -------- #
#         elif any(kw in query for kw in ["send a message", "send message", "send sms",
#                                         "phone call", "voice call", "video call", "call"]):
#             from engine.features import findContact, whatsApp, makeCall, sendMessage

#             contact_no, name = findContact(query)
#             if contact_no == 0:
#                 speak("I couldn't find the contact.")
#                 eel.ShowHood()
#                 return

#             # Auto WhatsApp video call
#             if "video call" in query:
#                 speak(f"Starting WhatsApp video call with {name}")
#                 whatsApp(contact_no, query, "video call", name)
#                 eel.ShowHood()
#                 return

#             # Ask for mode first
#             speak("Which mode do you want to use — WhatsApp or Mobile?")
#             # Save context to wait for next input
#             command_context = {
#                 "step": "mode",
#                 "contact": (contact_no, name),
#                 "original_query": query
#             }
#             eel.ShowHood()
#             return

#         # -------- GEMINI AI FALLBACK -------- #
#         else:
#             from engine.features import geminai
#             geminai(query)
#             eel.ShowHood()
#             return

#     except Exception as e:
#         print("Error in command execution:", e)
#         eel.ShowHood()



import pyttsx3
import speech_recognition as sr
import eel
import time
import webbrowser
from engine.helper import extract_yt_term

# Keep a global context to handle multi-step commands
command_context = {}

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)
    
    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
        time.sleep(2)
    except Exception as e:
        return ""

    return query.lower()


@eel.expose
def allCommands(message=1):
    """
    Handles all commands from user, either via voice (message=1) or text (message=str).
    Supports multi-step flows for messaging and calling with both voice and text modes.
    """
    global command_context
    try:
        # -------- DETERMINE INPUT MODE -------- #
        input_mode = "voice" if message == 1 else "text"

        # -------- GET QUERY -------- #
        if input_mode == "voice":
            query = takeCommand()
        else:
            query = str(message).strip().lower()
        
        print("Query:", query)
        eel.senderText(query)

        # -------- CHECK CONTEXT FOR MULTI-STEP -------- #
        if command_context:
            step = command_context.get("step")

            # STEP 1: Mode selection (Mobile / WhatsApp)
            if step == "mode":
                if query == "" or query not in ["mobile", "whatsapp"]:
                    speak("Please say or type Mobile or WhatsApp.")
                    eel.DisplayMessage("Listening or waiting for your input...")
                    if input_mode == "voice":
                        query = takeCommand().lower().strip()
                    else:
                        return  # wait for user text input again

                command_context["preference"] = query
                contact_no, name = command_context["contact"]

                # If it was a message
                if any(kw in command_context["original_query"] for kw in ["send message", "send sms", "send a message"]):
                    speak("What message should I send?")
                    eel.DisplayMessage("Listening or waiting for your message...")

                    if input_mode == "voice":
                        message_text = takeCommand().lower().strip()
                    else:
                        command_context["step"] = "message"
                        return  # wait for text input again

                    if message_text:
                        from engine.features import sendMessage, whatsApp
                        pref = command_context.get("preference", "mobile")
                        if "mobile" in pref:
                            sendMessage(message_text, contact_no, name)
                        elif "whatsapp" in pref:
                            whatsApp(contact_no, message_text, "message", name)
                        
                    else:
                        speak("I didn't catch that message. Please try again.")

                    command_context = {}
                    eel.ShowHood()
                    return

                # If it was a call
                else:
                    pref = command_context["preference"]
                    if "mobile" in pref:
                        from engine.features import makeCall
                        makeCall(name, contact_no)
                    elif "whatsapp" in pref:
                        from engine.features import whatsApp
                        whatsApp(contact_no, "", "call", name)

                    command_context = {}
                    eel.ShowHood()
                    return

            # STEP 2: Text message (for text mode)
            elif step == "message":
                contact_no, name = command_context["contact"]
                pref = command_context.get("preference", "mobile")
                message_text = query

                from engine.features import sendMessage, whatsApp
                if "mobile" in pref:
                    sendMessage(message_text, contact_no, name)
                elif "whatsapp" in pref:
                    whatsApp(contact_no, message_text, "message", name)

                command_context = {}
                eel.ShowHood()
                return

        # -------- OPEN COMMANDS -------- #
        if 'open' in query:
            from engine.features import openCommand
            openCommand(query)
            eel.ShowHood()
            return

        # -------- YOUTUBE COMMANDS -------- #
        elif 'youtube' in query:
            from engine.features import playYoutube, searchYoutube
            command_type, _ = extract_yt_term(query)
            if command_type == 'search':
                searchYoutube(query)
            else:
                playYoutube(query)
            eel.ShowHood()
            return

        # -------- CALL & MESSAGE HANDLING -------- #
        elif any(kw in query for kw in ["send a message", "send message", "send sms",
                                        "phone call", "voice call", "video call", "call"]):
            from engine.features import findContact, whatsApp, makeCall, sendMessage

            contact_no, name = findContact(query)
            if contact_no == 0:
                speak("I couldn't find the contact.")
                eel.ShowHood()
                return

            # Auto WhatsApp video call
            if "video call" in query:
                speak(f"Starting WhatsApp video call with {name}")
                whatsApp(contact_no, query, "video call", name)
                eel.ShowHood()
                return

            # Ask for mode first
            speak("Which mode do you want to use — WhatsApp or Mobile?")
            eel.DisplayMessage("Listening or waiting for your response...")

            if input_mode == "voice":
                mode = takeCommand().lower().strip()
            else:
                command_context = {
                    "step": "mode",
                    "contact": (contact_no, name),
                    "original_query": query
                }
                return  # wait for text input again

            if mode not in ["mobile", "whatsapp"]:
                speak("Please say Mobile or WhatsApp.")
                eel.DisplayMessage("Listening again...")
                if input_mode == "voice":
                    mode = takeCommand().lower().strip()
                else:
                    command_context = {
                        "step": "mode",
                        "contact": (contact_no, name),
                        "original_query": query
                    }
                    return

            # Proceed immediately for voice
            if any(kw in query for kw in ["send message", "send sms", "send a message"]):
                speak("What message should I send?")
                eel.DisplayMessage("Listening or waiting for your message...")

                if input_mode == "voice":
                    message_text = takeCommand().lower().strip()
                else:
                    command_context = {
                        "step": "message",
                        "contact": (contact_no, name),
                        "preference": mode
                    }
                    return

                if message_text:
                    if "mobile" in mode:
                        sendMessage(message_text, contact_no, name)
                    else:
                        whatsApp(contact_no, message_text, "message", name)
                    
                else:
                    speak("I didn't catch that message. Please try again.")

            else:
                if "mobile" in mode:
                    makeCall(name, contact_no)
                else:
                    whatsApp(contact_no, "", "call", name)

            command_context = {}
            eel.ShowHood()
            return

        # -------- GEMINI AI FALLBACK -------- #
        else:
            from engine.features import geminai
            geminai(query)
            eel.ShowHood()
            return

    except Exception as e:
        print("Error in command execution:", e)
        eel.ShowHood()
