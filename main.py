from windowcapture import WindowCapture
from action import Action
import pyautogui
import time

# get window handle by title regex
wincap = WindowCapture()
action = Action()

# areas = ['abawuwu', 'arena', 'dungeons', 'guild', 'tavern', 'pets', 'underground', 'fortress']
action.arena()
action.tavern()
action.pets()
action.dungeons()
action.underground()
action.fortress()
action.abawuwu()
