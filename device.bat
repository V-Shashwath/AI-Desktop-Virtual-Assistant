
@REM @echo off
@REM echo ===================================================
@REM echo Setting up Android device for wireless ADB...
@REM echo ===================================================
@REM echo Disconnecting old connections...
@REM adb disconnect
@REM echo Setting up connected device
@REM adb tcpip 5555
@REM echo Waiting for device to initialize
@REM timeout 3
@REM FOR /F "tokens=2" %%G IN ('adb shell ip addr show wlan0 ^|find "inet "') DO set ipfull=%%G
@REM FOR /F "tokens=1 delims=/" %%G in ("%ipfull%") DO set ip=%%G
@REM echo Connecting to device with IP %ip%...
@REM adb connect %ip%

@REM @echo off

@REM rem Set the IP address of your Android device
@REM set DEVICE_IP=192.0.0.4

@REM rem Set the port number for ADB
@REM set ADB_PORT=5555

@REM rem Set the path to the ADB executable
@REM set ADB_PATH="adb"

@REM rem Restart the ADB server
@REM %ADB_PATH% kill-server
@REM %ADB_PATH% start-server

@REM rem Connect to the Android device over Wi-Fi
@REM %ADB_PATH% connect %DEVICE_IP%:%ADB_PORT%



@REM --------------------------------------------




@REM @echo off
@REM echo ===================================================
@REM echo Setting up Android device for wireless ADB...
@REM echo ===================================================

@REM :: Disconnect any previous connections
@REM echo Disconnecting old connections...
@REM adb disconnect

@REM :: List USB devices
@REM echo Checking for connected USB devices...
@REM adb devices

@REM :: Start TCP mode on port 5555
@REM echo Restarting device in TCP mode on port 5555...
@REM adb tcpip 5555

@REM :: Wait for device to initialize
@REM timeout /t 3

@REM :: Get device IP from wlan0
@REM FOR /F "tokens=2" %%G IN ('adb shell ip addr show wlan0 ^| find "inet "') DO set ipfull=%%G
@REM FOR /F "tokens=1 delims=/" %%G IN ("%ipfull%") DO set DEVICE_IP=%%G

@REM echo Auto-detected device IP: %DEVICE_IP%

@REM :: Disconnect USB (optional)
@REM echo Disconnecting USB device...
@REM adb disconnect

@REM :: Connect to device via Wi-Fi
@REM echo Connecting to device via Wi-Fi...
@REM adb connect %DEVICE_IP%:5555

@REM :: Restart ADB server to ensure clean state
@REM echo Restarting ADB server...
@REM adb kill-server
@REM adb start-server

@REM :: List all connected devices
@REM echo ===================================================
@REM echo Current connected devices (USB + Wi-Fi):
@REM adb devices
@REM echo ===================================================






@REM @echo off
@REM echo ===================================================
@REM echo Setting up Android device for wireless ADB...
@REM echo ===================================================

@REM REM 1. Disconnect any existing ADB Wi-Fi connections
@REM adb disconnect
@REM echo Disconnected old connections.

@REM REM 2. Check for USB devices
@REM for /f "skip=1 tokens=1" %%D in ('adb devices') do (
@REM     if not "%%D"=="" set USB_DEVICE=%%D
@REM )

@REM if "%USB_DEVICE%"=="" (
@REM     echo No USB device detected. Please connect your device via USB.
@REM     pause
@REM     exit /b
@REM )

@REM echo USB device detected: %USB_DEVICE%

@REM REM 3. Restart device in TCP mode
@REM adb -s %USB_DEVICE% tcpip 5555
@REM echo Device restarted in TCP/IP mode on port 5555
@REM timeout /t 3 /nobreak >nul

@REM REM 4. Get device IPv4 address
@REM for /f "tokens=2" %%A in ('adb -s %USB_DEVICE% shell ip addr show wlan0 ^| find "inet " ^| findstr /v ":"') do set ipfull=%%A
@REM for /f "tokens=1 delims=/" %%B in ("%ipfull%") do set DEVICE_IP=%%B

@REM if "%DEVICE_IP%"=="" (
@REM     echo Failed to detect device IP. Make sure Wi-Fi is enabled on your device.
@REM     pause
@REM     exit /b
@REM )

@REM echo Auto-detected device IP: %DEVICE_IP%

@REM REM 5. Disconnect USB (optional)
@REM adb -s %USB_DEVICE% disconnect
@REM echo USB disconnected.

@REM REM 6. Connect over Wi-Fi
@REM adb connect %DEVICE_IP%:5555

@REM REM 7. Restart ADB server to refresh devices
@REM adb kill-server
@REM adb start-server

@REM echo ===================================================
@REM echo Current connected devices (USB + Wi-Fi):
@REM adb devices
@REM echo ===================================================




@echo off
echo ===================================================
echo Setting up Android device for dual ADB (USB + Wi-Fi)...
echo ===================================================

REM Check if USB device is connected
FOR /F "tokens=1" %%G IN ('adb devices ^| findstr /R "^[0-9a-f]*	device$"') DO set USB_DEVICE=%%G

IF "%USB_DEVICE%"=="" (
    echo No USB device detected. Attempting Wi-Fi connection...
) ELSE (
    echo USB device detected: %USB_DEVICE%
    echo Restarting device in TCP mode on port 5555...
    adb tcpip 5555
    timeout 3
)

REM Get IPv4 device IP (filter out IPv6)
FOR /F "tokens=2" %%G IN ('adb shell ip addr show wlan0 ^| findstr "inet " ^| findstr /V ":"') DO set IP_FULL=%%G
FOR /F "tokens=1 delims=/" %%G IN ("%IP_FULL%") DO set IP=%%G

IF "%IP%"=="" (
    echo Could not detect IPv4 address. Ensure Wi-Fi is connected on the phone.
    goto end
)

echo Attempting Wi-Fi connection to %IP%:5555...
adb connect %IP%:5555

REM Show current connected devices
echo ===================================================
echo Current connected devices (USB + Wi-Fi):
adb devices
echo ===================================================
