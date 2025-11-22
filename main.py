import os
import eel
import subprocess

from engine import command_enhanced
from engine.auth import recoganize
from engine.features import *
from engine.command_enhanced import *


def start():
    """Main application start function"""
    eel.init('frontend')

    playAssistantSound()

    # ==== SAFELY EXPOSE ALL EEL FUNCTIONS ====
    # This prevents "Already exposed function" error
    if hasattr(command_enhanced, "expose_eel_functions"):
        command_enhanced.expose_eel_functions()
    else:
        # fallback: expose allCommands manually
        @eel.expose
        def allCommands(message=1):
            from engine.command_enhanced import allCommands as cmd
            return cmd(message)

    # Background listener management
    @eel.expose
    def toggleBackgroundListener():
        """Toggle background listening mode"""
        try:
            from engine.background_listener import toggle_background_listener, is_listener_active
            status = toggle_background_listener()
            logger.info(f"Background listener toggled: {status}")
            return status
        except Exception as e:
            logger.error(f"Error toggling background listener: {e}")
            return False

    @eel.expose
    def init():
        """Initialize application"""
        # Setup Android device (optional)
        try:
            subprocess.call([r'device.bat'], timeout=30)
        except:
            pass
        
        eel.hideLoader()
        speak("Ready for Face Authentication")
        
        # Face authentication
        flag = recoganize.AuthenticateFace()
        
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            
            # Personalized greeting with user name from database
            from engine.utils import get_greeting
            greeting = get_greeting()
            
            # Get user name from database if exists
            try:
                cursor.execute("SELECT name FROM personal_info")
                result = cursor.fetchone()
                if result and result[0]:
                    user_name = result[0]
                    speak(f"{greeting} {user_name}! Welcome back. All systems ready.")
                else:
                    speak(f"{greeting}! Welcome back. All systems ready.")
            except:
                speak(f"{greeting}! Welcome back. All systems ready.")
            
            eel.hideStart()
            playAssistantSound()
            
            # Log session start
            from engine.logger import log_session_start
            log_session_start()
        else:
            speak("Face Authentication Failed")
            os.system("taskkill /im msedge.exe /f")
            os._exit(0)

    # Start browser
    os.system('start msedge.exe --app=http://localhost:8000/index.html')
    
    # Start Eel app
    eel.start('index.html', mode=None, host='localhost', block=True)