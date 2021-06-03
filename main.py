from windowcapture import WindowCapture
from action import Action
import time

# get window handle by title regex
wincap = WindowCapture(".*Shakes & Fidget.*")
action = Action()

# areas = ['abawuwu', 'arena', 'dungeons', 'guild', 'tavern', 'pets', 'underground]
action.pets()
