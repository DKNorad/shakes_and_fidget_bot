import random

from windowcapture import WindowCapture
from detection import Detection
import pywinauto
from pywinauto.keyboard import send_keys
from datetime import datetime
from random import choice
import time


class Action:

    # properties
    main_x = 0
    main_y = 0
    x = 0
    y = 0

    def __init__(self):
        self.wincap = WindowCapture()
        self.app = pywinauto.application.Application(backend="uia").connect(process=self.wincap.get_pid())

    @staticmethod
    def get_time():
        # return current date and time
        return datetime.now().strftime("%y-%m-%d %H:%M:%S")

    @staticmethod
    def enter(n):
        # press ENTER key N number of times
        for i in range(n):
            send_keys("{ENTER}")
            time.sleep(0.8)

    def click(self, x, y):
        # left mouse click with 4ms sleep timer
        self.app.MainDialog.click_input(coords=(x, y))
        time.sleep(0.4)

    def screenshot_and_match(self, image, threshold=0.85):
        # create screenshot and match(detect) image in entire window
        self.wincap.get_screenshot()
        return Detection(r'images\main_screen.jpg', fr'images\{image}.jpg', threshold)

    def abawuwu(self):
        # check for match
        det = self.screenshot_and_match(r'abawuwu\abawuwu')
        # get center coordinates
        main_x, main_y = det.get_item_center()
        self.click(main_x, main_y)

        # grab the daily bonus
        det = self.screenshot_and_match(r'abawuwu\daily_login')
        while not det.check_if_available():
            self.click(main_x, main_y)
            det = self.screenshot_and_match(r'abawuwu\daily_login')
        if det.check_if_available():
            x, y = det.get_item_center()
            self.click(x, y)

        # spin the wheel
        det = self.screenshot_and_match(r'abawuwu\abawuwu_check')
        while not det.check_if_available():
            self.click(main_x, main_y)
            det = self.screenshot_and_match(r'abawuwu\abawuwu_check')

        det = self.screenshot_and_match(r'abawuwu\dr_spin')
        if det.check_if_available():
            x, y = det.get_item_center()
            self.click(x, y)
            print(f'{self.get_time()}: Dr. Abawuwu wheel has been spun')
        else:
            return print(f'{self.get_time()}: The wheel has already been spun today.')

    def arena(self):
        opponents = [(575, 300), (790, 300), (1000, 300)]
        # check if arena is available
        det = self.screenshot_and_match(r'arena\arena', 0.93)
        # get main center coordinates
        main_x, main_y = det.get_item_center()

        # check if available
        if det.check_if_available():
            self.click(main_x, main_y)
        else:
            return print(f'{self.get_time()}: Arena is currently on cooldown.')

        # create a new screenshot to see if we opened the correct tab
        det = self.screenshot_and_match(r'arena\arena_boxes')
        while not det.check_if_available():
            self.click(main_x, main_y)
            det = self.screenshot_and_match(r'arena\arena_boxes')

        # attack a random player
        x, y = random.choice(opponents)
        self.click(x, y)
        self.enter(3)
        print(f'{self.get_time()}: A player has been attacked in the Arena.')

    # TODO fix pets being attacked while on a cooldown
    def pets(self):
        # check if pets are available
        det = self.screenshot_and_match(r'pets\pets_cooldown', 0.92)
        if det.check_if_available():
            return print(f'{self.get_time()}: Pets are under cooldown at the moment.')

        # get center coordinates and click
        main_x, main_y = det.get_item_center()
        self.click(main_x, main_y)

        # create a new screenshot to see if we opened the correct tab
        det = self.screenshot_and_match(r'pets\check_if_pet_screen')
        while not det.check_if_available():
            self.click(main_x, main_y)
            det = self.screenshot_and_match(r'pets\check_if_pet_screen')

        # iterate over all 5 pets
        pets = ['pet_shadow', 'pet_light', 'pet_earth', 'pet_fire', 'pet_water']
        count = 0
        for pet in pets:
            det = self.screenshot_and_match(r'pets\pets_cooldown', 0.89)
            if det.check_if_available():
                return print(f'{self.get_time()}: Pets are under cooldown at the moment.')

            det = Detection('images/main_screen.jpg', f'images/pets/{pet}.jpg')
            if not det.check_if_available():
                count += 1
                if count == 5:
                    return print(f'{self.get_time()}: All pets have been attacked.')
                continue
            x, y = det.get_item_center()
            self.click(x, y)
            self.enter(3)
            print(f'{self.get_time()}: A pet has been attacked.')
            break

    # TODO implement image to text processing to choose quest based on gold, exp or duration
    def tavern(self):
        # check if tavern is free
        det = self.screenshot_and_match(r'tavern\tavern', 0.92)
        if not det.check_if_available():
            return print(f'{self.get_time()}: You are currently on a mission.')

        # get center coordinates and click
        main_x, main_y = det.get_item_center()
        self.click(main_x, main_y)

        # create a new screenshot to see if we opened the correct tab
        det = self.screenshot_and_match(r'tavern\tavern_guard')
        while not det.check_if_available():
            self.click(main_x, main_y)
            det = self.screenshot_and_match(r'tavern\tavern_guard')

        # start the first quest
        self.enter(2)
        print(f'{self.get_time()}: Mission started.')

    def dungeons(self):
        dungeons = {'The Twister': (370, 180), 'Hemorridor': (600, 200), 'Mount Olympus': (815, 115),
                    'Nordic Gods': (1100, 105), 'Continues Loop of Idols': (715, 280), 'The Tower': (370, 180),
                    'Time-honored School of Magic': (920, 200), 'Easteros': (1225, 180),
                    'Black Skull Fortress': (515, 360), 'Circus of Terror': (850, 345), 'Hell': (1000, 365),
                    'The 13th Floor': (1120, 270), 'The Pyramids of Madness': (345, 430),
                    'The Emerald Scale Altar': (1140, 425), 'Desecrated Catacombs': (410, 680),
                    'The Frost Blood Temple': (550, 540), 'The Mines of Gloria': (620, 630),
                    'The Magma Stream': (780, 515), 'The Ruins of Gnark': (910, 670), 'The Toxic Tree': (1030, 520),
                    'The Cutthroat Grotto': (1125, 620), 'Demon\'s Portal': (715, 280)}
        # check if dungeons are available
        det = self.screenshot_and_match(r'dungeons\dungeons', 0.92)
        if not det.check_if_available():
            return print(f'{self.get_time()}: The dungeons are currently on a cooldown.')

        # get center coordinates and click
        main_x, main_y = det.get_item_center()
        self.click(main_x, main_y)

        # create a new screenshot to see if we opened the correct tab
        det = self.screenshot_and_match(r'dungeons\dungeons_twister')
        while not det.check_if_available():
            self.click(main_x, main_y)
            det = self.screenshot_and_match(r'dungeons\dungeons_twister')

        # enter "The Twister"
        x, y = det.get_item_center()
        self.click(x, y)
        self.enter(3)

    def underground(self):
        # create a new screenshot to see if we opened the correct tab
        det = self.screenshot_and_match(r'underground\lure_hero', 0.9)
        det2 = self.screenshot_and_match(r'underground\lure_hero_done', 0.9)
        while not (det2.check_if_available() or det.check_if_available()):
            self.click(140, 450)
            det = self.screenshot_and_match(r'underground\lure_hero', 0.83)
            det2 = self.screenshot_and_match(r'underground\lure_hero_done', 0.83)

        # collect souls
        det = self.screenshot_and_match(r'underground\soul_harvest')
        x, y = det.get_item_center()
        self.click(x, y)
        det = self.screenshot_and_match(r'underground\close')
        if det.check_if_available():
            x, y = det.get_item_center()
            self.click(x, y)
            print(f'{self.get_time()}: Underground souls collected.')
        else:
            print(f'{self.get_time()}: Soul Extractor already collected or storage is full.')

        # collect gold # TODO grab a relevant screenshot to match the gold mine
        # det = self.screenshot_and_match(r'underground\soul_harvest')
        # x, y = det.get_item_center()
        # self.click(x, y)
        # det = self.screenshot_and_match(r'underground\close')
        # if det.check_if_available():
        #     x, y = det.get_item_center()
        #     self.click(x, y)
        #     print(f'{self.get_time()}: Gold Pit is under construction or the gold has already been collected.')
        # else:
        #     print(f'{self.get_time()}: Underground gold collected.')

        # lure heroes underground
        det = self.screenshot_and_match(r'underground\lure_hero', 0.95)
        while True:
            if not det.check_if_available():
                print(f'{self.get_time()}: Maximum heroes lured for the day.')
                break
            x, y = det.get_item_center()
            self.click(x, y)
            self.enter(4)
            print(f'{self.get_time()}: A hero has been lured in the underground.')

        # Use adventure points in the Adventuromatic
        det = self.screenshot_and_match(r'underground\adventurematic', 0.98)
        while True:
            if not det.check_if_available():
                x, y = det.get_item_center()
                self.click(x, y)
                self.enter(3)
                print(f'{self.get_time()}: Underground adventure points used.')
            else:
                print(f'{self.get_time()}: All Adventuromatic points have been used.')
                break

    def fortress(self):
        pass
