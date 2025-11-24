"""
PRODUCTION-LEVEL System Control Commands
ALL SYSTEM COMMANDS WORK IN BOTH NORMAL AND BACKGROUND MODE
Fixed: close_tab closes tabs, close_window closes windows (not confused)
"""

import os
import subprocess
import psutil
import logging
import pyautogui
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Safe speak wrapper
def speak(text):
    """Text to speech - wrapper"""
    try:
        from engine.command_enhanced import speak as cmd_speak
        cmd_speak(text)
    except Exception as e:
        logger.error(f"Could not speak: {text} - Error: {e}")


# ===== VOLUME CONTROL =====

def volume_up():
    """Increase volume"""
    try:
        logger.info("Executing: Volume Up")
        for _ in range(3):
            pyautogui.press('volumeup')
            time.sleep(0.1)
        speak("Volume increased, boss")
        logger.info("Volume increased successfully")
        return True
    except Exception as e:
        logger.error(f"Volume up error: {e}")
        speak("Could not increase volume")
        return False


def volume_down():
    """Decrease volume"""
    try:
        logger.info("Executing: Volume Down")
        for _ in range(3):
            pyautogui.press('volumedown')
            time.sleep(0.1)
        speak("Volume decreased, boss")
        logger.info("Volume decreased successfully")
        return True
    except Exception as e:
        logger.error(f"Volume down error: {e}")
        speak("Could not decrease volume")
        return False


def mute_volume():
    """Mute/unmute system volume"""
    try:
        logger.info("Executing: Mute Volume")
        pyautogui.press('volumemute')
        speak("Volume muted, boss")
        logger.info("Volume muted successfully")
        return True
    except Exception as e:
        logger.error(f"Mute error: {e}")
        speak("Could not mute volume")
        return False


# ===== BRIGHTNESS CONTROL =====

def increase_brightness():
    """Increase screen brightness"""
    try:
        logger.info("Executing: Increase Brightness")
        import screen_brightness_control as sbc
        
        try:
            current = sbc.get_brightness()[0]
        except:
            current = 50
        
        new_brightness = min(current + 15, 100)
        sbc.set_brightness(new_brightness)
        speak(f"Brightness increased to {new_brightness} percent, boss")
        logger.info(f"Brightness increased to {new_brightness}%")
        return True
    except ImportError:
        logger.warning("Fallback to keyboard shortcut for brightness")
        try:
            for _ in range(3):
                pyautogui.press('brightnessup')
                time.sleep(0.1)
            speak("Brightness increased, boss")
            return True
        except Exception as e:
            logger.error(f"Brightness control error: {e}")
            speak("Could not increase brightness")
            return False
    except Exception as e:
        logger.error(f"Brightness error: {e}")
        speak("Could not increase brightness")
        return False


def decrease_brightness():
    """Decrease screen brightness"""
    try:
        logger.info("Executing: Decrease Brightness")
        import screen_brightness_control as sbc
        
        try:
            current = sbc.get_brightness()[0]
        except:
            current = 50
        
        new_brightness = max(current - 15, 10)
        sbc.set_brightness(new_brightness)
        speak(f"Brightness decreased to {new_brightness} percent, boss")
        logger.info(f"Brightness decreased to {new_brightness}%")
        return True
    except ImportError:
        logger.warning("Fallback to keyboard shortcut for brightness")
        try:
            for _ in range(3):
                pyautogui.press('brightnessdown')
                time.sleep(0.1)
            speak("Brightness decreased, boss")
            return True
        except Exception as e:
            logger.error(f"Brightness control error: {e}")
            speak("Could not decrease brightness")
            return False
    except Exception as e:
        logger.error(f"Brightness error: {e}")
        speak("Could not decrease brightness")
        return False


# ===== BATTERY INFO =====

def get_battery_info():
    """Get battery information"""
    try:
        logger.info("Executing: Get Battery Info")
        battery = psutil.sensors_battery()
        if battery:
            percent = int(battery.percent)
            plugged = "plugged in" if battery.power_plugged else "on battery power"
            
            if (battery.secsleft != psutil.POWER_TIME_UNLIMITED and 
                battery.secsleft > 0 and 
                not battery.power_plugged):
                hours = int(battery.secsleft // 3600)
                minutes = int((battery.secsleft % 3600) // 60)
                
                if hours < 100:
                    time_left = f"{hours} hours and {minutes} minutes"
                    response = f"Battery is at {percent} percent, {plugged}. Time remaining: {time_left}, boss."
                else:
                    response = f"Battery is at {percent} percent and {plugged}, boss."
            else:
                response = f"Battery is at {percent} percent and {plugged}, boss."
            
            speak(response)
            logger.info(f"Battery info: {response}")
            return True
        else:
            speak("No battery detected. System is running on AC power.")
            return True
    except Exception as e:
        logger.error(f"Battery info error: {e}")
        speak("Could not fetch battery information, boss")
        return False


# ===== WINDOW CONTROL =====

def close_window():
    """Close current active window - uses Alt+F4"""
    try:
        logger.info("Executing: Close Window (Alt+F4)")
        pyautogui.hotkey('alt', 'f4')
        speak("Window closed, boss")
        logger.info("Window closed")
        time.sleep(0.5)
        return True
    except Exception as e:
        logger.error(f"Close window error: {e}")
        speak("Could not close window, boss")
        return False


def minimize_window():
    """Minimize current window - uses Win+Down"""
    try:
        logger.info("Executing: Minimize Window (Win+Down)")
        pyautogui.hotkey('win', 'down')
        speak("Window minimized, boss")
        logger.info("Window minimized")
        time.sleep(0.5)
        return True
    except Exception as e:
        logger.error(f"Minimize window error: {e}")
        speak("Could not minimize window, boss")
        return False


def maximize_window():
    """Maximize current window - uses Win+Up"""
    try:
        logger.info("Executing: Maximize Window (Win+Up)")
        pyautogui.hotkey('win', 'up')
        speak("Window maximized, boss")
        logger.info("Window maximized")
        time.sleep(0.5)
        return True
    except Exception as e:
        logger.error(f"Maximize window error: {e}")
        speak("Could not maximize window, boss")
        return False


def show_desktop():
    """Show desktop (minimize all windows) - uses Win+D"""
    try:
        logger.info("Executing: Show Desktop (Win+D)")
        pyautogui.hotkey('win', 'd')
        speak("Showing desktop, boss")
        logger.info("Desktop shown")
        return True
    except Exception as e:
        logger.error(f"Show desktop error: {e}")
        speak("Could not show desktop, boss")
        return False


# ===== TAB MANAGEMENT - CRITICAL FIXES =====

def switch_tab():
    """Switch to next browser tab - uses Ctrl+Tab"""
    try:
        logger.info("Executing: Switch Tab (Ctrl+Tab)")
        pyautogui.hotkey('ctrl', 'tab')
        speak("Switched to next tab, boss")
        logger.info("Tab switched")
        time.sleep(0.3)
        return True
    except Exception as e:
        logger.error(f"Switch tab error: {e}")
        speak("Could not switch tab, boss")
        return False


def previous_tab():
    """Switch to previous tab - uses Ctrl+Shift+Tab"""
    try:
        logger.info("Executing: Previous Tab (Ctrl+Shift+Tab)")
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        speak("Switched to previous tab, boss")
        logger.info("Previous tab")
        time.sleep(0.3)
        return True
    except Exception as e:
        logger.error(f"Previous tab error: {e}")
        speak("Could not go to previous tab, boss")
        return False


def new_tab():
    """Open new browser tab - uses Ctrl+T"""
    try:
        logger.info("Executing: New Tab (Ctrl+T)")
        pyautogui.hotkey('ctrl', 't')
        speak("New tab opened, boss")
        logger.info("New tab opened")
        time.sleep(0.5)
        return True
    except Exception as e:
        logger.error(f"New tab error: {e}")
        speak("Could not open new tab, boss")
        return False


def close_tab():
    """Close current tab - uses Ctrl+W (CRITICAL: NOT Alt+F4)"""
    try:
        logger.info("Executing: Close Tab (Ctrl+W) - NOT WINDOW")
        time.sleep(0.1)
        # Use Ctrl+W which closes only the tab, not the window
        pyautogui.hotkey('ctrl', 'w')
        speak("Tab closed, boss")
        logger.info("Tab closed successfully")
        time.sleep(0.3)
        return True
    except Exception as e:
        logger.error(f"Close tab error: {e}")
        speak("Could not close tab, boss")
        return False


# ===== SCREENSHOTS =====

def take_screenshot():
    """Take a screenshot"""
    try:
        logger.info("Executing: Take Screenshot")
        import pyautogui
        from datetime import datetime
        
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/screenshot_{timestamp}.png"
        
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        speak("Screenshot saved, boss")
        logger.info(f"Screenshot saved: {filename}")
        return True
    except Exception as e:
        logger.error(f"Screenshot error: {e}")
        speak("Could not take screenshot, boss")
        return False


# ===== SYSTEM OPERATIONS =====

def lock_system():
    """Lock the computer"""
    try:
        logger.info("Executing: Lock System")
        speak("Locking the system, boss")
        os.system("rundll32.exe user32.dll,LockWorkStation")
        logger.info("System locked")
        return True
    except Exception as e:
        logger.error(f"Lock system error: {e}")
        speak("Could not lock system, boss")
        return False


def shutdown_system():
    """Shutdown the computer"""
    try:
        logger.info("Executing: Shutdown System")
        speak("Shutting down the system in 2 minutes, boss")
        os.system("shutdown /s /t 120 /c 'Shutdown initiated by ADVA assistant'")
        logger.info("Shutdown initiated")
        return True
    except Exception as e:
        logger.error(f"Shutdown error: {e}")
        speak("Could not shutdown, boss")
        return False


def restart_system():
    """Restart the computer"""
    try:
        logger.info("Executing: Restart System")
        speak("Restarting the system in 2 minutes, boss")
        os.system("shutdown /r /t 120 /c 'Restart initiated by ADVA assistant'")
        logger.info("Restart initiated")
        return True
    except Exception as e:
        logger.error(f"Restart error: {e}")
        speak("Could not restart, boss")
        return False


def cancel_shutdown():
    """Cancel scheduled shutdown/restart"""
    try:
        logger.info("Executing: Cancel Shutdown")
        os.system("shutdown /a")
        speak("Shutdown cancelled, boss")
        logger.info("Shutdown cancelled")
        return True
    except Exception as e:
        logger.error(f"Cancel shutdown error: {e}")
        speak("Could not cancel shutdown, boss")
        return False


def open_task_manager():
    """Open Windows Task Manager"""
    try:
        logger.info("Executing: Open Task Manager")
        subprocess.Popen("taskmgr.exe")
        speak("Opening Task Manager, boss")
        logger.info("Task Manager opened")
        return True
    except Exception as e:
        logger.error(f"Task Manager error: {e}")
        speak("Could not open task manager, boss")
        return False


# ===== MAIN ROUTER - PRODUCTION LEVEL =====

def execute_system_command(query):
    """
    PRODUCTION-LEVEL Main router for system commands
    Returns True if command was handled, False otherwise
    CRITICAL: Must work in BOTH normal and background mode
    """
    if not query:
        return False
    
    query_lower = query.lower().strip()
    logger.info(f"[SYSTEM_COMMAND] Processing: {query_lower}")
    
    # === VOLUME COMMANDS ===
    if any(word in query_lower for word in ['volume up', 'increase volume', 'louder', 'sound up', 'volume increase']):
        return volume_up()
    elif any(word in query_lower for word in ['volume down', 'decrease volume', 'quieter', 'lower volume', 'sound down']):
        return volume_down()
    elif any(word in query_lower for word in ['mute', 'silence']):
        return mute_volume()
    
    # === BRIGHTNESS COMMANDS ===
    elif any(word in query_lower for word in ['brightness up', 'increase brightness', 'brighter', 'brighten', 'bright up']):
        return increase_brightness()
    elif any(word in query_lower for word in ['brightness down', 'decrease brightness', 'dimmer', 'dim']):
        return decrease_brightness()
    
    # === BATTERY ===
    elif any(word in query_lower for word in ['battery', 'battery level', 'battery percentage', 'battery status', 'battery info']):
        return get_battery_info()
    
    # === WINDOW MANAGEMENT ===
    elif any(word in query_lower for word in ['close window', 'close this window', 'exit window']):
        return close_window()
    elif any(word in query_lower for word in ['minimize window', 'minimize this', 'minimize this window']):
        return minimize_window()
    elif any(word in query_lower for word in ['maximize window', 'maximize this', 'maximize this window']):
        return maximize_window()
    elif any(word in query_lower for word in ['show desktop', 'minimize all', 'desktop']):
        return show_desktop()
    
    # === TAB MANAGEMENT - CRITICAL: FIXED ===
    elif any(word in query_lower for word in ['switch tab', 'next tab', 'change tab']):
        return switch_tab()
    elif any(word in query_lower for word in ['previous tab', 'last tab', 'back tab']):
        return previous_tab()
    elif any(word in query_lower for word in ['new tab', 'open tab', 'open new tab']):
        return new_tab()
    elif any(word in query_lower for word in ['close tab', 'close this tab']):
        logger.info("CRITICAL: Close Tab command detected - using Ctrl+W only")
        return close_tab()
    
    # === SCREENSHOT ===
    elif any(word in query_lower for word in ['take screenshot', 'screenshot', 'capture screen', 'screen capture']):
        return take_screenshot()
    
    # === SYSTEM OPERATIONS ===
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
    
    # Not a system command
    logger.info(f"Not a system command: {query_lower}")
    return False