from windowcapture import WindowCapture
from detection import Detection
import pywinauto
from pywinauto.keyboard import send_keys
from datetime import datetime
import time


class Action:

    def __init__(self):
        self.app = pywinauto.application.Application(backend="uia").connect(title_re='.*Shakes & Fidget.*')
        self.wincap = WindowCapture(".*Shakes & Fidget.*")

    @staticmethod
    def get_time():
        # return current date and time
        return datetime.now().strftime("%y-%m-%d %H:%M:%S")

    @staticmethod
    def enter(n):
        # press ENTER key N number of times
        for i in range(n):
            send_keys("{ENTER}")
            time.sleep(0.7)

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
        # check if arena is available
        det = self.screenshot_and_match(r'arena\arena', 0.92)
        # get main center coordinates
        main_x, main_y = det.get_item_center()

        # check if available
        if not det.check_if_available():
            self.click(main_x, main_y)
        else:
            return print(f'{self.get_time()}: Arena is currently on cooldown.')

        # create a new screenshot to see if we opened the correct tab
        det = self.screenshot_and_match(r'arena\arena_boxes')
        while not det.check_if_available():
            self.click(main_x, main_y)
            det = self.screenshot_and_match(r'arena\arena_boxes')

        # attack middle player
        x, y = det.get_item_center()
        self.click(x, y + 100)
        self.enter(3)
        print(f'{self.get_time()}: A player has been attacked in the Arena.')

    def pets(self):
        # TODO fix pets being attacked while on a cooldown
        # check if pets are available
        det = self.screenshot_and_match(r'pets\pets_cooldown', 0.89)
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
                    print(f'{self.get_time()}: All pets have been attacked.')
                continue
            x, y = det.get_item_center()
            self.click(x, y)
            self.enter(3)
            print(f'{self.get_time()}: A pet has been attacked.')
            break

    def tavern(self):
        # TODO implement image to text processing to choose quest based on gold, exp or duration
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
        # open the fortress tab
        det = self.screenshot_and_match(r'underground\fortress')
        main_x, main_y = det.get_item_center()
        self.click(main_x, main_y)

        # create a new screenshot to see if we opened the correct tab
        det = self.screenshot_and_match(r'underground\soul_harvest')
        while not det.check_if_available():
            self.click(main_x, main_y)
            det = self.screenshot_and_match(r'underground\soul_harvest')

        # collect souls
        x, y = det.get_item_center()
        self.click(x, y)
        print(f'{self.get_time()}: Underground souls collected.')

        # lure heroes underground
        det = self.screenshot_and_match(r'underground\lure_hero', 0.9)
        if not det.check_if_available():
            return print(f'{self.get_time()}'
                         f': Maximum heroes lured for the day.')
        x, y = det.get_item_center()
        self.click(x, y)
        self.enter(4)
