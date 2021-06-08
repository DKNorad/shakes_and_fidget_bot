# Shakes & Fidget Bot

### --Description--
A bot that automaticaly performs most of the repeatable tasks in the game.

### --Locations--
- **Tavern:** Start a random mission.
- **Arena:** Attack a random player.
- **Pets:** Attack all pets in order from "Shadow" to "Water".
- **Dungeons:** Enter "The Twister" dungeon.
- **Fortress:**
  - Academy - Collect the experience.
  - Quarry - Collect the stone.
  - Woodcutter's Hut - Collect the wood.
- **Underground:**
  - Sould Extractor - Collect the souls.
  - Gold Pit - Collect the gold.
  - Lure all 5 heroes for the day.
- **Dr. Abawuwu:**
  - Collect the daily bonus.
  - Spin the wheel.
  
### --Functionality--
- Show a message with a date stamp for every action performed or every error returned.
- Always check if the activity is available to avoid spending "Mushrooms" which is the in game paid currency.

### --Setup--
Since the script is using image recognition for most of the tasks in only works correctly when the game window is 1280x720 in windowed mode. You can force the game to run with specific resolution by adding the following launch options in Steam:  
**-screen-width 1280 -screen-height 720**  
After that you can just run the script. It will automatically focus on the game. Note that the script cannot run in the background and it requires the game window ot be on top.

### --Future plans--  
- [ ] Configure a GUI to choose which actions to be run.
- [ ] Implement a way to choose a specific location in the Dungeon to be entered.
- [ ] Implement image to text processing to choose a mission based on gold, exp or duration.


### --Resources used--
[Learn Code By Gaming](https://www.youtube.com/channel/UCD8vb6Bi7_K_78nItq5YITA)  
Libraries used:
- time
- pywinauto
- datetime
- random
- cv2
- re
- numpy
- ctypes
- win32gui, win32ui, win32con, win32process
