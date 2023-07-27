# Shakes & Fidget Bot

# DEPRECATED. Currently working on migrating the script to Selenium in order to work with the browser version on the background.

### Description:
A bot that automatically performs most of the repeatable tasks in the game.

### Locations/Tasks:
- **Tavern:** Start a random mission.
- **Arena:** Attack a random player.
- **Pets:** Attack all pets in order from "Shadow" to "Water".
- **Dungeons:** Enter "The Twister" dungeon.
- **Fortress:**
  - Academy - Collect the experience.
  - Quarry - Collect the stone.
  - Woodcutter's Hut - Collect the wood.
- **Underground:**
  - Soul Extractor - Collect the souls.
  - Gold Pit - Collect the gold.
  - Lure all 5 heroes for the day.
- **Dr. Abawuwu:**
  - Collect the daily bonus.
  - Spin the wheel.
  
### Functionality:
- Show a message with a date stamp for every action performed or every error returned.
- Always check if the activity is available to avoid spending "Mushrooms" which is the in game paid currency.
- The script is unable to run in the background as it requires the game window to be on focus.

### Prerequisites:  
- numpy
- opencv-python
- pywinauto
- pywin32


### Setup:
**Resolution:**  
Since the script is using image recognition for most of the tasks it only works correctly when the game window is
1280x720 in windowed mode. You can force the game to run with specific resolution by adding the 
following launch options in Steam:  
**-screen-width 1280 -screen-height 720**  

**Game Settings:**  
You need to have the in game timers turned on for hte script to operate correctly. You can do that in the 
"Gameplay" section in the game settings by ticking the "Always show timer" option.

### Future plans:
- [ ] Configure a GUI to choose which actions to be run.
- [ ] Implement a way to choose a specific location in the Dungeon to be entered.
- [ ] Implement image to text processing to choose a mission based on gold, exp or duration.

### Resources used:
[Learn Code By Gaming](https://www.youtube.com/channel/UCD8vb6Bi7_K_78nItq5YITA)  
