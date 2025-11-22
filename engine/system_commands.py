"""
System Control Commands - Fixed & Enhanced
Handle system-level operations: volume, brightness, battery, etc.
"""

import os
import subprocess
import psutil
import logging
import pyautogui
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def speak(text):
    """Text to speech - wrapper"""
    try:
        from engine.command_enhanced import speak as cmd_speak
        cmd_speak(text)
    except:
        logger.error(f"Could not speak: {text}")


# ===== VOLUME CONTROL =====

def set_volume(level):
    """Set system volume (0-100)"""
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        logger.info(f"Volume set to {level}%")
        return True
    except Exception as e:
        logger.error(f"Volume control error (pycaw): {e}")
        return False


def volume_up():
    """Increase volume"""
    try:
        # Press volume up key multiple times
        for _ in range(3):
            pyautogui.press('volumeup')
            time.sleep(0.1)
        speak("Volume increased")
        logger.info("Volume increased")
        return True
    except Exception as e:
        logger.error(f"Volume up error: {e}")
        return False


def volume_down():
    """Decrease volume"""
    try:
        for _ in range(3):
            pyautogui.press('volumedown')
            time.sleep(0.1)
        speak("Volume decreased")
        logger.info("Volume decreased")
        return True
    except Exception as e:
        logger.error(f"Volume down error: {e}")
        return False


def mute_volume():
    """Mute/unmute system volume"""
    try:
        pyautogui.press('volumemute')
        speak("Volume muted")
        logger.info("Volume muted")
        return True
    except Exception as e:
        logger.error(f"Mute error: {e}")
        return False


# ===== BRIGHTNESS CONTROL =====

def increase_brightness():
    """Increase screen brightness"""
    try:
        import screen_brightness_control as sbc
        
        # Get current brightness
        try:
            current = sbc.get_brightness()[0]
        except:
            current = 50
        
        new_brightness = min(current + 15, 100)
        sbc.set_brightness(new_brightness)
        speak(f"Brightness increased to {new_brightness} percent")
        logger.info(f"Brightness increased to {new_brightness}%")
        return True
    except ImportError:
        logger.warning("screen-brightness-control not installed, trying keyboard shortcut")
        try:
            for _ in range(3):
                pyautogui.press('brightnessup')
                time.sleep(0.1)
            speak("Brightness increased")
            return True
        except Exception as e:
            logger.error(f"Brightness control error: {e}")
            return False
    except Exception as e:
        logger.error(f"Brightness error: {e}")
        # Fallback to keyboard
        try:
            for _ in range(3):
                pyautogui.press('brightnessup')
                time.sleep(0.1)
            speak("Brightness increased")
            return True
        except:
            return False


def decrease_brightness():
    """Decrease screen brightness"""
    try:
        import screen_brightness_control as sbc
        
        try:
            current = sbc.get_brightness()[0]
        except:
            current = 50
        
        new_brightness = max(current - 15, 10)
        sbc.set_brightness(new_brightness)
        speak(f"Brightness decreased to {new_brightness} percent")
        logger.info(f"Brightness decreased to {new_brightness}%")
        return True
    except ImportError:
        logger.warning("screen-brightness-control not installed, trying keyboard shortcut")
        try:
            for _ in range(3):
                pyautogui.press('brightnessdown')
                time.sleep(0.1)
            speak("Brightness decreased")
            return True
        except Exception as e:
            logger.error(f"Brightness control error: {e}")
            return False
    except Exception as e:
        logger.error(f"Brightness error: {e}")
        # Fallback to keyboard
        try:
            for _ in range(3):
                pyautogui.press('brightnessdown')
                time.sleep(0.1)
            speak("Brightness decreased")
            return True
        except:
            return False


# ===== BATTERY INFO =====

def get_battery_info():
    """Get battery information"""
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = int(battery.percent)
            plugged = "plugged in" if battery.power_plugged else "on battery power"
            
            # Only show time if on battery and time is valid
            if (battery.secsleft != psutil.POWER_TIME_UNLIMITED and 
                battery.secsleft > 0 and 
                not battery.power_plugged):
                hours = int(battery.secsleft // 3600)
                minutes = int((battery.secsleft % 3600) // 60)
                
                # Only show if reasonable (less than 100 hours)
                if hours < 100:
                    time_left = f"{hours} hours and {minutes} minutes"
                    response = f"Battery is at {percent} percent, {plugged}. Time remaining: {time_left}."
                else:
                    response = f"Battery is at {percent} percent and {plugged}."
            else:
                response = f"Battery is at {percent} percent and {plugged}."
            
            speak(response)
            logger.info(response)
            return True
        else:
            speak("No battery detected. System is running on AC power.")
            return True
    except Exception as e:
        logger.error(f"Battery info error: {e}")
        speak("Could not fetch battery information")
        return False


# ===== WINDOW CONTROL =====

def close_window():
    """Close current active window"""
    try:
        pyautogui.hotkey('alt', 'f4')
        speak("Window closed")
        logger.info("Window closed")
        time.sleep(0.5)
        return True
    except Exception as e:
        logger.error(f"Close window error: {e}")
        return False


def minimize_window():
    """Minimize current window"""
    try:
        pyautogui.hotkey('win', 'down')
        speak("Window minimized")
        logger.info("Window minimized")
        time.sleep(0.5)
        return True
    except Exception as e:
        logger.error(f"Minimize window error: {e}")
        return False


def maximize_window():
    """Maximize current window"""
    try:
        pyautogui.hotkey('win', 'up')
        speak("Window maximized")
        logger.info("Window maximized")
        time.sleep(0.5)
        return True
    except Exception as e:
        logger.error(f"Maximize window error: {e}")
        return False


def show_desktop():
    """Show desktop (minimize all windows)"""
    try:
        pyautogui.hotkey('win', 'd')
        speak("Showing desktop")
        logger.info("Desktop shown")
        return True
    except Exception as e:
        logger.error(f"Show desktop error: {e}")
        return False


# ===== TAB MANAGEMENT =====

def switch_tab():
    """Switch to next browser tab"""
    try:
        pyautogui.hotkey('ctrl', 'tab')
        speak("Switched to next tab")
        logger.info("Tab switched")
        time.sleep(0.3)
        return True
    except Exception as e:
        logger.error(f"Switch tab error: {e}")
        return False


def previous_tab():
    """Switch to previous tab"""
    try:
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        speak("Switched to previous tab")
        logger.info("Previous tab")
        time.sleep(0.3)
        return True
    except Exception as e:
        logger.error(f"Previous tab error: {e}")
        return False


def new_tab():
    """Open new browser tab"""
    try:
        pyautogui.hotkey('ctrl', 't')
        speak("New tab opened")
        logger.info("New tab opened")
        time.sleep(0.5)
        return True
    except Exception as e:
        logger.error(f"New tab error: {e}")
        return False


def close_tab():
    """Close current tab"""
    try:
        pyautogui.hotkey('ctrl', 'w')
        speak("Tab closed")
        logger.info("Tab closed")
        time.sleep(0.3)
        return True
    except Exception as e:
        logger.error(f"Close tab error: {e}")
        return False


# ===== SCREENSHOTS =====

def take_screenshot():
    """Take a screenshot"""
    try:
        import pyautogui
        from datetime import datetime
        
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/screenshot_{timestamp}.png"
        
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        speak(f"Screenshot saved")
        logger.info(f"Screenshot saved: {filename}")
        return True
    except Exception as e:
        logger.error(f"Screenshot error: {e}")
        speak("Could not take screenshot")
        return False


# ===== SYSTEM OPERATIONS =====

def lock_system():
    """Lock the computer"""
    try:
        speak("Locking the system")
        os.system("rundll32.exe user32.dll,LockWorkStation")
        logger.info("System locked")
        return True
    except Exception as e:
        logger.error(f"Lock system error: {e}")
        return False


def shutdown_system():
    """Shutdown the computer"""
    try:
        speak("Shutting down the system in 2 minutes")
        os.system("shutdown /s /t 120 /c 'Shutdown initiated by assistant'")
        logger.info("Shutdown initiated")
        return True
    except Exception as e:
        logger.error(f"Shutdown error: {e}")
        return False


def restart_system():
    """Restart the computer"""
    try:
        speak("Restarting the system in 2 minutes")
        os.system("shutdown /r /t 120 /c 'Restart initiated by assistant'")
        logger.info("Restart initiated")
        return True
    except Exception as e:
        logger.error(f"Restart error: {e}")
        return False


def cancel_shutdown():
    """Cancel scheduled shutdown/restart"""
    try:
        os.system("shutdown /a")
        speak("Shutdown cancelled")
        logger.info("Shutdown cancelled")
        return True
    except Exception as e:
        logger.error(f"Cancel shutdown error: {e}")
        return False


def open_task_manager():
    """Open Windows Task Manager"""
    try:
        subprocess.Popen("taskmgr.exe")
        speak("Opening Task Manager")
        logger.info("Task Manager opened")
        return True
    except Exception as e:
        logger.error(f"Task Manager error: {e}")
        return False


# ===== MAIN ROUTER =====

def execute_system_command(query):
    """
    Main router for system commands
    Returns True if command was handled, False otherwise
    """
    query_lower = query.lower().strip()
    
    logger.info(f"Executing system command: {query_lower}")
    
    # === VOLUME COMMANDS ===
    if any(word in query_lower for word in ['volume up', 'increase volume', 'increase the volume', 'louder', 'sound up']):
        return volume_up()
    
    elif any(word in query_lower for word in ['volume down', 'decrease volume', 'decrease the volume', 'quieter', 'lower volume', 'sound down']):
        return volume_down()
    
    elif any(word in query_lower for word in ['mute', 'silence', 'quiet']):
        return mute_volume()
    
    # === BRIGHTNESS COMMANDS ===
    elif any(word in query_lower for word in ['brightness up', 'increase brightness', 'increase the brightness', 'brighter', 'brighten']):
        return increase_brightness()
    
    elif any(word in query_lower for word in ['brightness down', 'decrease brightness', 'decrease the brightness', 'dimmer', 'dim']):
        return decrease_brightness()
    
    # === BATTERY ===
    elif any(word in query_lower for word in ['battery', 'battery level', 'battery percentage', 'battery status', 'battery info']):
        return get_battery_info()
    
    # === WINDOW MANAGEMENT ===
    elif any(word in query_lower for word in ['close window', 'close this', 'exit window']):
        return close_window()
    
    elif any(word in query_lower for word in ['minimize window', 'minimize this', 'minimize']):
        return minimize_window()
    
    elif any(word in query_lower for word in ['maximize window', 'maximize this', 'maximize']):
        return maximize_window()
    
    # === TAB MANAGEMENT ===
    elif any(word in query_lower for word in ['switch tab', 'next tab', 'change tab']):
        return switch_tab()
    
    elif any(word in query_lower for word in ['previous tab', 'last tab', 'back tab']):
        return previous_tab()
    
    elif any(word in query_lower for word in ['new tab', 'open tab']):
        return new_tab()
    
    elif any(word in query_lower for word in ['close tab', 'close this tab']):
        return close_tab()
    
    # === SCREENSHOT ===
    elif any(word in query_lower for word in ['take screenshot', 'screenshot', 'capture screen', 'screen capture']):
        return take_screenshot()
    
    # === SYSTEM OPS ===
    elif any(word in query_lower for word in ['lock system', 'lock computer', 'lock pc', 'lock screen']):
        return lock_system()
    
    elif 'shutdown' in query_lower or 'shut down' in query_lower:
        return shutdown_system()
    
    elif 'restart' in query_lower or 'reboot' in query_lower:
        return restart_system()
    
    elif any(word in query_lower for word in ['cancel shutdown', 'abort shutdown', 'stop shutdown']):
        return cancel_shutdown()
    
    elif any(word in query_lower for word in ['task manager', 'open task manager']):
        return open_task_manager()
    
    elif any(word in query_lower for word in ['show desktop', 'minimize all', 'desktop']):
        return show_desktop()
    
    # Not a system command
    return False