from windowcapture import WindowCapture
from action import Action
from time import time

# get window handle by title regex
wincap = WindowCapture(".*Shakes & Fidget.*")
action = Action()

# areas = ['abawuwu', 'arena', 'dungeons', 'guild', 'tavern', 'pets']


action.arena()
# while True:
#     action.pets()
#     action.arena()
#     action.abawuwu()
#
#     time.sleep(600)

# press 'q' with t

# he output window focused to exit.
# waits 1 ms every loop to process key presses
# if cv.waitKey(1) == ord('q'):
#     cv.destroyAllWindows()
#     break
