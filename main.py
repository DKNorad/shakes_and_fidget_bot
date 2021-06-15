from windowcapture import WindowCapture
from action import Action
import time
import tkinter as tk

wincap = WindowCapture()
action = Action()

# areas = ['abawuwu', 'arena', 'dungeons', 'guild', 'tavern', 'pets', 'underground', 'fortress']
count = 0
# while True:
#     action.tavern()
#     action.arena()
#     if count % 2 == 0:
#         action.pets()
#
#     if count % 6 == 0:
#         action.dungeons()
#         action.underground()
#         action.fortress()
#         action.abawuwu()
#     count += 1
#     print(f"{action.get_time()}: Waiting for 10 minutes.")
#     time.sleep(600)

action.underground()