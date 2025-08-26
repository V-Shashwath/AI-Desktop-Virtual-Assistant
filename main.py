import os
import eel

from engine.features import *

eel.init('frontend')

os.system('start msedge.exe --app=http://localhost:8000/index.html')

playAssistantSound()

eel.start('index.html', mode=None, host='localhost', block=True)