#import subprocess
import time
import cv2
import numpy as np
from ppadb.client import Client as AdbClient
import time
import os

IMAGE_DIR = "images"
GO_BUTTON = os.path.join(IMAGE_DIR, "go.png")
BLUE_STAR = os.path.join(IMAGE_DIR, "blueStar.png")
RED_CROSS = os.path.join(IMAGE_DIR, "redCross.png")
RED_CROSS2 = os.path.join(IMAGE_DIR, "redCross2.png")
JAIL = os.path.join(IMAGE_DIR, "jail.png")
SHUTDOWN = os.path.join(IMAGE_DIR, "shutdownMarker.png")
SHUTDOWN2 = os.path.join(IMAGE_DIR, "shutdownMarker2.png")
COLLECT = os.path.join(IMAGE_DIR, "collect.png")
HEIST = os.path.join(IMAGE_DIR, "heist.png")
GIFT = os.path.join(IMAGE_DIR, "freeGift.png")
FREE = os.path.join(IMAGE_DIR, "free.png")
CLOSE_GIFT = os.path.join(IMAGE_DIR, "closeGift.png")
GREY_CROSS = os.path.join(IMAGE_DIR, "greyCross.png")
OUT_OF_DICE = os.path.join(IMAGE_DIR, "outofdice.png")
LOGIN_GUEST = os.path.join(IMAGE_DIR, "loginAsGuest.png")
LOGIN_GUEST2 = os.path.join(IMAGE_DIR, "loginAsGuest2.png")
LOGIN_GUEST3 = os.path.join(IMAGE_DIR, "loginAsGuest3.png")
CAN_BUILD = os.path.join(IMAGE_DIR, "canBuild.png")
BUILD_ICON = os.path.join(IMAGE_DIR, "buildMoney.png")
NO_MONEY = os.path.join(IMAGE_DIR, "noMoneyBuild.png")
NEW_BOARD = os.path.join(IMAGE_DIR, "newBoardGO.png")
BUILD_TOP = os.path.join(IMAGE_DIR, "buildTop.png")
CHEST_OPEN = os.path.join(IMAGE_DIR, "chestOpen.png")
CHEST_START = os.path.join(IMAGE_DIR, "chestStart.png")
CHEST_DONE = os.path.join(IMAGE_DIR, "chestDone.png")
WHEEL_SPIN = os.path.join(IMAGE_DIR, "wheelSpin.png")
CHEST_TRIANGLE = os.path.join(IMAGE_DIR, "chestTriangle.png")
DAILY_DONE = os.path.join(IMAGE_DIR, "dailiesDone.png")
DAILY_CLEAR = os.path.join(IMAGE_DIR, "dailiesClear.png")
DAILY_BUILDING = os.path.join(IMAGE_DIR, "dailiesBuilding.png")
CLOSE_CRAP = os.path.join(IMAGE_DIR, "closeCrap.png")
DAILY_CLAIM = os.path.join(IMAGE_DIR, "dailiesClaim.png")
DAILY_MAIN = os.path.join(IMAGE_DIR, "dailiesMain.png")
SKIP = os.path.join(IMAGE_DIR, "skip.png")
STICKER_ICON = os.path.join(IMAGE_DIR, "stickerIcon.png")
STICKER_CONTINUE = os.path.join(IMAGE_DIR, "stickerContinue.png")
STICKER_CROSS = os.path.join(IMAGE_DIR, "stickerCross.png")
STICKER_EXTRA = os.path.join(IMAGE_DIR, "stickerExtra.png")
STICKER_FINAL_SEND = os.path.join(IMAGE_DIR, "stickerFinalSend.png")
STICKER_LEFT = os.path.join(IMAGE_DIR, "stickerLeft.png")
STICKER_OK = os.path.join(IMAGE_DIR, "stickerOK.png")
STICKER_PERSON = os.path.join(IMAGE_DIR, "stickerPerson.png")
STICKER_PERSON2 = os.path.join(IMAGE_DIR, "stickerPerson2.png")
STICKER_SEARCH = os.path.join(IMAGE_DIR, "stickerSearch.png")
STICKER_SEND = os.path.join(IMAGE_DIR, "stickerSend.png")
STICKER_SEND = os.path.join(IMAGE_DIR, "stickerSend.png")
CLAIM = os.path.join(IMAGE_DIR, "claim.png")
CASHGRAB = os.path.join(IMAGE_DIR, "cashgrab.png")
LETSROLL = os.path.join(IMAGE_DIR, "letsRoll.png")
ROLLOUT = os.path.join(IMAGE_DIR, "rollOut.png")
FREEROLL = os.path.join(IMAGE_DIR, "freeRoll.png")

class BluestacksManager:
    def __init__(self):
        self.client = None
        self.device = None

    def launch_bluestacks(self):
        print("Starting bluestacks....")  
        #Add Code to start bluestacks here
        #subprocess.call(["start", "Bluestacks"], shell=True)
        #time.sleep(30)

    def connect_adb(self):
        self.client = AdbClient(host="127.0.0.1", port=5037)
        if len(self.client.devices()) == 0:
            print("No devices connected")
            exit(1)
        self.device = self.client.devices()[1]  

class AdbManager:
    def __init__(self, adb_device):
        self.adb_device = adb_device

    def capture_screen(self):
        screenshot_data = self.adb_device.screencap()
        image = cv2.imdecode(np.frombuffer(screenshot_data, np.uint8), cv2.IMREAD_COLOR)
        cv2.imwrite('screen.png', image)
        return 'screen.png'

    def check_exists(self, large_image_path, template_path, threshold=0.7):
        large_image = cv2.imread(large_image_path)
        template = cv2.imread(template_path)
        result = cv2.matchTemplate(large_image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= threshold:
            return True
        return False
    
    def check_exists_multiple(self, large_image_path, template_path, top_n, min_distance=10, threshold=0.7):
        large_image = cv2.imread(large_image_path)
        template = cv2.imread(template_path)
        template_height, template_width, _ = template.shape
        result = cv2.matchTemplate(large_image, template, cv2.TM_CCOEFF_NORMED)
        sorted_results = []
        while len(sorted_results) < top_n:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Check if the similarity score is above the threshold
            if max_val < threshold:
                break
            
            # Check if the new location is sufficiently far from existing locations
            is_far_enough = True
            for _, existing_loc in sorted_results:
                distance = np.sqrt((existing_loc[0] - max_loc[0]) ** 2 + (existing_loc[1] - max_loc[1]) ** 2)
                if distance < min_distance:
                    is_far_enough = False
                    break
            
            if is_far_enough:
                sorted_results.append((max_val, max_loc))
            
            # Set the found location to a low value to find the next highest match
            result[max_loc[1], max_loc[0]] = -1

            # Break if there are no more valid matches
            if max_val < 0:
                break

        # Calculate the middle coordinates for the top N found locations
        middle_coords = []
        for score, pt in sorted_results:
            middle_x = pt[0] + template_width / 2
            middle_y = pt[1] + template_height / 2
            middle_coords.append((middle_x, middle_y))

        return middle_coords
    
    def click_image(self, large_image_path, template_path):
        large_image = cv2.imread(large_image_path)
        template = cv2.imread(template_path)
        result = cv2.matchTemplate(large_image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        template_width, template_height = template.shape[1], template.shape[0]
        x = max_loc[0] + template_width / 2
        y = max_loc[1] + template_height / 2
        command = f"input tap {x} {y}"
        self.adb_device.shell(command)

    def find_and_check_exist(self, template_path, threshold=0.80):
        large_image = cv2.imread(self.capture_screen())
        template = cv2.imread(template_path)
        result = cv2.matchTemplate(large_image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= threshold:
            template_width, template_height = template.shape[1], template.shape[0]
            middle_x = max_loc[0] + template_width / 2
            middle_y = max_loc[1] + template_height / 2
            return (middle_x, middle_y)
        return None
    
    def click_button(self, coords):
        x, y = int(coords[0]), int(coords[1])
        command = f"input tap {x} {y}"
        self.adb_device.shell(command)

    def type_text(self, text):
        text = text.replace(" ", "%s")
        command = f"input text {text}"
        self.adb_device.shell(command)

    def long_press(self, coords, duration):
        x, y = int(coords[0]), int(coords[1])
        command = f"input swipe {x} {y} {x} {y} {duration}"
        self.adb_device.shell(command)
    
    def swipe_right(self):
        command = f"input swipe 800 250 100 250"
        self.adb_device.shell(command)
    
    def swipe_for_chest(self):
        command = f"input swipe 650 400 200 1000"
        self.adb_device.shell(command)
        time.sleep(1)
        self.adb_device.shell(command)
        time.sleep(1)
        command = f"input swipe 600 1000 600 650"
        self.adb_device.shell(command)
        time.sleep(1)
        command = f"input swipe 250 750 650 750"
        self.adb_device.shell(command)
        time.sleep(1)
    
    def spam_chest(self):
        self.adb_device.shell("input tap 200 700")
        time.sleep(0.5)
        self.adb_device.shell("input tap 450 650")
        time.sleep(0.5)
        self.adb_device.shell("input tap 700 700")
        time.sleep(0.5)
        self.adb_device.shell("input tap 175 875")
        time.sleep(0.5)
        self.adb_device.shell("input tap 450 840")
        time.sleep(0.5)
        self.adb_device.shell("input tap 725 900")
        time.sleep(0.5)
        self.adb_device.shell("input tap 160 1100")
        time.sleep(0.5)
        self.adb_device.shell("input tap 450 1060")
        time.sleep(0.5)
        self.adb_device.shell("input tap 730 1100")
        time.sleep(0.5)
        

    def get_average_color(self, image_path):
        image = cv2.imread(image_path)
        avg_color_per_row = np.average(image, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        return avg_color.astype(int) 
    
    def verify_color(self, image_path, template_path, coords, tolerance=20):
            screen_image = cv2.imread(image_path)
            template_image = cv2.imread(template_path)
            
            x, y = int(coords[0]), int(coords[1])
            screen_color = screen_image[y, x]

            template_middle_x = template_image.shape[1] // 2
            template_middle_y = template_image.shape[0] // 2
            template_color = template_image[template_middle_y, template_middle_x]

            if all(abs(screen_color[i] - template_color[i]) <= tolerance for i in range(3)):
                return True
            return False

class Bot:
    def __init__(self):
        self.bluestacks_Manager = BluestacksManager()
        self.adb_Device = None
        self.adb_Manager = None
        self.running = True

    def setup(self):
        self.bluestacks_Manager.launch_bluestacks()
        self.bluestacks_Manager.connect_adb()
        self.adb_Device = self.bluestacks_Manager.device
        self.adb_Manager = AdbManager(self.adb_Device)
    
    def handle_jail(self):
        for x in range(4):
            screen = self.adb_Manager.capture_screen()
            self.adb_Manager.click_image(screen, JAIL)
            time.sleep(1)

    def handle_shutdown(self):
        count = 0
        while not self.adb_Manager.find_and_check_exist(GO_BUTTON) and count<10:
            screen = self.adb_Manager.capture_screen()
            if self.adb_Manager.check_exists(screen, SHUTDOWN):
                print("Shutting player down!")
                self.adb_Manager.click_image(screen, SHUTDOWN)
            elif self.adb_Manager.check_exists(screen, SHUTDOWN2):
                print("Shutting player down 2!")
                self.adb_Manager.click_image(screen, SHUTDOWN2)
            elif self.adb_Manager.check_exists(screen, COLLECT):
                print("Collecting Money...")
                self.adb_Manager.click_image(screen, COLLECT)
            else:
                self.close_stuff_one_loop()
            
            count = count + 1
            time.sleep(0.5)

    def handle_bankHeist(self):
        while not self.adb_Manager.find_and_check_exist(GO_BUTTON):
            screen = self.adb_Manager.capture_screen()
            if self.adb_Manager.check_exists(screen, HEIST):
                doors = self.adb_Manager.check_exists_multiple(screen, HEIST, 7)
                for coords in doors:
                    self.adb_Manager.click_button(coords)
            elif self.adb_Manager.check_exists(screen, COLLECT):
                print("Collecting Money...")
                self.adb_Manager.click_image(screen, COLLECT)
            else:
                self.close_stuff_one_loop()

            time.sleep(1)

    def check_game_open(self):
        print("Checking if game is open...")
        while not self.adb_Manager.find_and_check_exist(BLUE_STAR):
            screen = self.adb_Manager.capture_screen()
            print("Searching for blue star logo...")

            if self.adb_Manager.check_exists(screen, LOGIN_GUEST):
                print("Logging in...")
                self.adb_Manager.click_image(screen, LOGIN_GUEST)
            elif self.adb_Manager.check_exists(screen, LOGIN_GUEST2):
                print("Logging in...")
                self.adb_Manager.click_image(screen, LOGIN_GUEST2)
            elif self.adb_Manager.check_exists(screen, LOGIN_GUEST3):
                print("Logging in...")
                self.adb_Manager.click_image(screen, LOGIN_GUEST3)
            elif self.adb_Manager.check_exists(screen, COLLECT):
                print("Collecting Money...")
                self.adb_Manager.click_image(screen, COLLECT)
            elif self.adb_Manager.check_exists(screen, SKIP):
                print("Found SKIP")
                self.adb_Manager.click_image(screen, SKIP)

            time.sleep(2)
        print("Found Star: Game is open")
        return

    def close_stuff(self):
        print("Closing crap...")
        while not self.adb_Manager.find_and_check_exist(GO_BUTTON):
            screen = self.adb_Manager.capture_screen()
            if self.adb_Manager.check_exists(screen, SHUTDOWN):
                print("In Shutdown: Attacking player!")
                self.adb_Manager.click_image(screen, SHUTDOWN)
                time.sleep(0.5)
                self.handle_shutdown()
            elif self.adb_Manager.check_exists(screen, HEIST):
                print("In Bank Heist: Robbing player!")
                self.handle_bankHeist()
            elif self.adb_Manager.check_exists(screen, RED_CROSS):
                print("Found Red Cross: Clicking on Cross")
                self.adb_Manager.click_image(screen, RED_CROSS)
            elif self.adb_Manager.check_exists(screen, COLLECT):
                print("Collecting stuff...")
                self.adb_Manager.click_image(screen, COLLECT)
            elif self.adb_Manager.check_exists(screen, CLOSE_GIFT):
                print("Some screen? Closing...")
                self.adb_Manager.click_image(screen, CLOSE_GIFT)
            elif self.adb_Manager.check_exists(screen, NEW_BOARD):
                print("New Board...")
                self.adb_Manager.click_image(screen, NEW_BOARD)
            elif self.adb_Manager.check_exists(screen, GREY_CROSS):
                print("Found Grey Cross: Clicking on Cross")
                self.adb_Manager.click_image(screen, GREY_CROSS)
            elif self.adb_Manager.check_exists(screen, CLOSE_CRAP):
                print("closeing im on it sign")
                self.adb_Manager.click_image(screen, CLOSE_CRAP)
            elif self.adb_Manager.check_exists(screen, WHEEL_SPIN):
                print("Found WHEEL SPIN: SPINNING")
                self.adb_Manager.click_image(screen, WHEEL_SPIN)
            elif self.adb_Manager.check_exists(screen, SKIP):
                print("Found Skip")
                self.adb_Manager.click_image(screen, SKIP)
            elif self.adb_Manager.check_exists(screen, RED_CROSS2):
                print("Found Red Cross: Clicking on Cross")
                self.adb_Manager.click_image(screen, RED_CROSS2)
            elif self.adb_Manager.check_exists(screen, LETSROLL):
                print("Found Lets ROLL")
                self.adb_Manager.click_image(screen, LETSROLL)
            elif self.adb_Manager.check_exists(screen, ROLLOUT):
                print("Found ROLLOUT")
                self.adb_Manager.click_image(screen, ROLLOUT)

            time.sleep(3.5)
            
        time.sleep(1)

        return
    

    def close_stuff_one_loop(self):
        screen = self.adb_Manager.capture_screen()

        if self.adb_Manager.check_exists(screen, RED_CROSS):
            print("Found Red Cross: Clicking on Cross")
            self.adb_Manager.click_image(screen, RED_CROSS)
        elif self.adb_Manager.check_exists(screen, COLLECT):
            print("Collecting stuff...")
            self.adb_Manager.click_image(screen, COLLECT)
        elif self.adb_Manager.check_exists(screen, CLOSE_GIFT):
            print("Some screen? Closing...")
            self.adb_Manager.click_image(screen, CLOSE_GIFT)
        elif self.adb_Manager.check_exists(screen, NEW_BOARD):
            print("New Board...")
            self.adb_Manager.click_image(screen, NEW_BOARD)
        elif self.adb_Manager.check_exists(screen, GREY_CROSS):
            print("Found Grey Cross: Clicking on Cross")
            self.adb_Manager.click_image(screen, GREY_CROSS)
        elif self.adb_Manager.check_exists(screen, SKIP):
                print("Found WHEEL SPIN: SPINNING")
                self.adb_Manager.click_image(screen, SKIP)
        elif self.adb_Manager.check_exists(screen, LETSROLL):
                print("Found Lets ROLL")
                self.adb_Manager.click_image(screen, LETSROLL)
            

    def roll_dice(self):
        print("Rolling Dice...")
        count = 0
        gotDice = True
        while gotDice:
            screen = self.adb_Manager.capture_screen()  
            print("Finding Go Button...")
            if self.adb_Manager.check_exists(screen, GO_BUTTON):
                if count > 100:
                    break  
                count = count + 1
                print("Found Go Button: Clicking on Go")
                self.adb_Manager.click_image(screen, GO_BUTTON)
            elif self.adb_Manager.check_exists(screen, JAIL):
                print("In Jail: Clicking on Roll")
                self.handle_jail()
            elif self.adb_Manager.check_exists(screen, SHUTDOWN):
                print("In Shutdown: Attacking player!")
                self.adb_Manager.click_image(screen, SHUTDOWN)
                time.sleep(0.5)
                self.handle_shutdown()
            elif self.adb_Manager.check_exists(screen, HEIST):
                print("In Bank Heist: Robbing player!")
                self.handle_bankHeist()
            elif self.adb_Manager.check_exists(screen, CLOSE_GIFT):
                print("Some screen? Closing...")
                self.adb_Manager.click_image(screen, CLOSE_GIFT)
            elif self.adb_Manager.check_exists(screen, COLLECT):
                print("Collecting stuff...")
                self.adb_Manager.click_image(screen, COLLECT)
            elif self.adb_Manager.check_exists(screen, GREY_CROSS):
                print("Found Grey Cross: Clicking on Cross")
                self.adb_Manager.click_image(screen, GREY_CROSS)
            elif self.adb_Manager.check_exists(screen, WHEEL_SPIN):
                print("Found WHEEL SPIN: SPINNING")
                self.adb_Manager.click_image(screen, WHEEL_SPIN)
            elif self.adb_Manager.check_exists(screen, SKIP):
                print("Found SKIP")
                self.adb_Manager.click_image(screen, SKIP)
            elif self.adb_Manager.check_exists(screen, CLAIM):
                print("Found Claimm")
                self.adb_Manager.click_image(screen, CLAIM)
            elif self.adb_Manager.check_exists(screen, CASHGRAB):
                print("Found CASHGRAB")
                self.adb_Manager.click_image(screen, CASHGRAB)
            elif self.adb_Manager.check_exists(screen, FREEROLL):
                print("Found free roll")
                self.adb_Manager.click_image(screen, FREEROLL)
            else:
                if self.adb_Manager.check_exists(screen, OUT_OF_DICE):
                    print("Out of dice! Stopping...")
                    self.close_stuff()
                    gotDice = False
            time.sleep(3)

        time.sleep(2)


    def collect_free_gift(self):
        print("Collecting free Gift")
        if self.adb_Manager.find_and_check_exist(GIFT):
            screen = self.adb_Manager.capture_screen()
            self.adb_Manager.click_image(screen, GIFT)
            time.sleep(1)
            for x in range(4):
                self.adb_Manager.swipe_right()
                time.sleep(0.5)
            screen = self.adb_Manager.capture_screen()
            self.adb_Manager.click_image(screen, FREE)
            time.sleep(1)
            if self.adb_Manager.check_exists(screen, COLLECT):
                print("Collecting Money...")
                self.adb_Manager.click_image(screen, COLLECT)
            while not self.adb_Manager.find_and_check_exist(GO_BUTTON):
                screen = self.adb_Manager.capture_screen()
                self.adb_Manager.click_image(screen, CLOSE_GIFT)
                time.sleep(2)
        else:
            print("Free gift not available yet")

    def open_community_chest(self):
        print("Opening community Chest..")
        screen = self.adb_Manager.capture_screen()
        if self.adb_Manager.find_and_check_exist(GO_BUTTON):
            self.adb_Manager.swipe_for_chest()
            time.sleep(1)
            screen = self.adb_Manager.capture_screen()
            if self.adb_Manager.check_exists(screen, CHEST_OPEN):
                print("Clicking open chest")
                self.adb_Manager.click_image(screen, CHEST_OPEN)
                time.sleep(3)
                while not self.adb_Manager.check_exists(screen, CHEST_DONE):
                    screen = self.adb_Manager.capture_screen()
                    if self.adb_Manager.check_exists(screen, CHEST_TRIANGLE): # can fix this 
                        print("Spamming...")
                        self.adb_Manager.spam_chest()
                        time.sleep(3)
                    elif self.adb_Manager.check_exists(screen, CHEST_START):
                        print("Clicking start")
                        self.adb_Manager.click_image(screen, CHEST_START)
                        time.sleep(3)
                    elif self.adb_Manager.check_exists(screen, COLLECT):
                        print("Collecting...")
                        self.adb_Manager.click_image(screen, COLLECT)
                        time.sleep(1.5)
        
        print("Should be done with chest")
        time.sleep(1)
        self.close_stuff()
        return
    
    def build_buildings(self):
        noMoney = False
        while self.adb_Manager.find_and_check_exist(CAN_BUILD):
            screen = self.adb_Manager.capture_screen()
            self.adb_Manager.click_image(screen, CAN_BUILD)
            time.sleep(2)
            while True:
                screen = self.adb_Manager.capture_screen()
                if self.adb_Manager.check_exists(screen, NO_MONEY):
                    print("out of money")
                    noMoney = True
                    break
                elif self.adb_Manager.check_exists(screen, BUILD_ICON):
                    print("building building...")
                    buildings = self.adb_Manager.check_exists_multiple(screen, BUILD_ICON, 5)
                    sorted_buildings = sorted(buildings)
                    for coords in sorted_buildings:
                        self.adb_Manager.click_button(coords)
                else:
                    self.close_stuff()
                    break
                time.sleep(2)
            while not self.adb_Manager.find_and_check_exist(GO_BUTTON):
                self.close_stuff()

            if noMoney:
                break

    def do_event(self):
        pass

    def roll_dice_once(self):
        print("Rolling Dice...")
        count = 0
        gotDice = True
        while gotDice:
            screen = self.adb_Manager.capture_screen()  
            print("Finding Go Button...")
            if self.adb_Manager.check_exists(screen, GO_BUTTON):
                if count > 5:
                    break  
                count = count + 1
                print("Found Go Button: Clicking on Go")
                self.adb_Manager.click_image(screen, GO_BUTTON)
            elif self.adb_Manager.check_exists(screen, JAIL):
                print("In Jail: Clicking on Roll")
                self.handle_jail()
            elif self.adb_Manager.check_exists(screen, SHUTDOWN):
                print("In Shutdown: Attacking player!")
                self.adb_Manager.click_image(screen, SHUTDOWN)
                time.sleep(0.5)
                self.handle_shutdown()
            elif self.adb_Manager.check_exists(screen, HEIST):
                print("In Bank Heist: Robbing player!")
                self.handle_bankHeist()
            elif self.adb_Manager.check_exists(screen, CLOSE_GIFT):
                print("Some screen? Closing...")
                self.adb_Manager.click_image(screen, CLOSE_GIFT)
            elif self.adb_Manager.check_exists(screen, COLLECT):
                print("Collecting stuff...")
                self.adb_Manager.click_image(screen, COLLECT)
            elif self.adb_Manager.check_exists(screen, GREY_CROSS):
                print("Found Grey Cross: Clicking on Cross")
                self.adb_Manager.click_image(screen, GREY_CROSS)
            elif self.adb_Manager.check_exists(screen, WHEEL_SPIN):
                print("Found WHEEL SPIN: SPINNING")
                self.adb_Manager.click_image(screen, WHEEL_SPIN)
            elif self.adb_Manager.check_exists(screen, SKIP):
                print("Found SKIP")
                self.adb_Manager.click_image(screen, SKIP)
            elif self.adb_Manager.check_exists(screen, CLAIM):
                print("Found CLAIM")
                self.adb_Manager.click_image(screen, CLAIM)
            elif self.adb_Manager.check_exists(screen, CASHGRAB):
                print("Found CASHGRAB")
                self.adb_Manager.click_image(screen, CASHGRAB)
            elif self.adb_Manager.check_exists(screen, ROLLOUT):
                print("Found ROLLOUT")
                self.adb_Manager.click_image(screen, ROLLOUT)
            elif self.adb_Manager.check_exists(screen, FREEROLL):
                print("Found free roll")
                self.adb_Manager.click_image(screen, FREEROLL)
            else:
                if self.adb_Manager.check_exists(screen, OUT_OF_DICE):
                    print("Out of dice! Stopping...")
                    self.close_stuff()
                    gotDice = False
            time.sleep(3)

        time.sleep(2)
        return gotDice
    
    def do_dailies(self):
        print("trying to do dailies")
        gotDice = True
        while not self.adb_Manager.find_and_check_exist(DAILY_DONE):
            if self.adb_Manager.find_and_check_exist(DAILY_BUILDING):
                print("building buildings")
                if not self.adb_Manager.find_and_check_exist(CAN_BUILD):
                    print("no money to build yet")
                    gotDice = self.roll_dice_once()
                else:
                    self.build_buildings()
                    gotDice = self.roll_dice_once()
                    print(f"testing after building: {gotDice}")
            elif not gotDice:
                print("no more dice")
                break
            elif self.adb_Manager.find_and_check_exist(DAILY_CLEAR):
                print("done dailies")
                screen = self.adb_Manager.capture_screen()
                self.adb_Manager.click_image(screen, DAILY_CLEAR)
                time.sleep(1)
                while self.adb_Manager.find_and_check_exist(DAILY_CLAIM):
                    screen = self.adb_Manager.capture_screen()
                    print("Claiming Dailies")
                    claims = self.adb_Manager.check_exists_multiple(screen, DAILY_CLAIM, 3)
                    for coords in claims:
                        self.adb_Manager.click_button(coords)
                    self.close_stuff()
                print("FINISHED dailies")
            else:
                gotDice = self.roll_dice_once()
                print(f"testing: {gotDice}")

            time.sleep(1)

        print("no more dailies")

    def send_stickers(self):
        #23 albums click left 23 times
        albums = 23
        #170 764
        #make sure at main screen/check for go sign
        while not self.adb_Manager.find_and_check_exist(GO_BUTTON):
            self.close_stuff()
        
        screen = self.adb_Manager.capture_screen()
        if self.adb_Manager.check_exists(screen, STICKER_ICON):
            print("Opening Album")
            self.adb_Manager.click_image(screen, STICKER_ICON)
        time.sleep(2)
        self.adb_Manager.click_button([170,760])
        time.sleep(2)
        screen = self.adb_Manager.capture_screen()
        #click left arrow once 
        if self.adb_Manager.check_exists(screen, STICKER_LEFT):
            print("Clicking Left")
            self.adb_Manager.click_image(screen, STICKER_LEFT)
        time.sleep(2)
        #for number of albums 
        stickersSent = 0 
        for i in range(albums):
            screen = self.adb_Manager.capture_screen()
            extras = self.adb_Manager.check_exists_multiple(screen, STICKER_EXTRA, 5)
            print(f"Extras found: {extras}")
            #for each coordinate found
            if extras and len(extras) > 0:
                for idx, coord in enumerate(extras):
                    print(f"Found 1 Extra at coordinates {coord}")
                    #click on it
                    self.adb_Manager.click_button(coord)
                    time.sleep(2)

                    screen = self.adb_Manager.capture_screen()
                    if self.adb_Manager.check_exists(screen, STICKER_SEND):
                        print("clicking send")
                        stickersSent = stickersSent + 1
                        self.adb_Manager.click_image(screen, STICKER_SEND)
                        time.sleep(2)

                        screen = self.adb_Manager.capture_screen()
                        if self.adb_Manager.check_exists(screen, STICKER_SEARCH):
                            print("clicking search")
                            self.adb_Manager.click_image(screen, STICKER_SEARCH)
                        time.sleep(1)

                        #self.adb_Manager.type_text("yule")
                        self.adb_Manager.type_text("mktyn")
                        time.sleep(1)

                        screen = self.adb_Manager.capture_screen()
                        if self.adb_Manager.check_exists(screen, STICKER_PERSON2):
                            self.adb_Manager.click_image(screen, STICKER_PERSON2)
                        time.sleep(1)

                        screen = self.adb_Manager.capture_screen()
                        if self.adb_Manager.check_exists(screen, STICKER_PERSON2):
                            print("Selecting User")
                            self.adb_Manager.click_image(screen, STICKER_PERSON2)
                        time.sleep(1)

                        screen = self.adb_Manager.capture_screen()
                        if self.adb_Manager.check_exists(screen, STICKER_CONTINUE):
                            print("clicking continue")
                            self.adb_Manager.click_image(screen, STICKER_CONTINUE)
                        time.sleep(2)

                        screen = self.adb_Manager.capture_screen()
                        if self.adb_Manager.check_exists(screen, STICKER_FINAL_SEND):
                            print("clicking send")
                            self.adb_Manager.click_image(screen, STICKER_FINAL_SEND)
                        time.sleep(2)

                        screen = self.adb_Manager.capture_screen()
                        if self.adb_Manager.check_exists(screen, STICKER_OK):
                            print("clicking ok")
                            self.adb_Manager.click_image(screen, STICKER_OK)
                        time.sleep(2)

                        screen = self.adb_Manager.capture_screen()
                        if self.adb_Manager.check_exists(screen, STICKER_CROSS):
                            print("closing")
                            self.adb_Manager.click_image(screen, STICKER_CROSS)
                        time.sleep(2)
                    
                    else:
                        screen = self.adb_Manager.capture_screen()
                        if self.adb_Manager.check_exists(screen, STICKER_CROSS):
                            print("closing")
                            self.adb_Manager.click_image(screen, STICKER_CROSS)
                        time.sleep(2)

            else:
                print(f"no extras in {i+1}")

            time.sleep(2)
            screen = self.adb_Manager.capture_screen()

            if stickersSent > 4:
                break

            if self.adb_Manager.check_exists(screen, STICKER_LEFT):
                print("Clicking Left")
                self.adb_Manager.click_image(screen, STICKER_LEFT)
            time.sleep(2)
        
        self.close_stuff()
        print("finished sending stickers")


    def run(self):
        print("Bot started running...")
        try:
            self.check_game_open()
            time.sleep(3)
            self.close_stuff()
            self.close_stuff()
            self.do_dailies()
            self.roll_dice()
            self.build_buildings()
            self.collect_free_gift()
            self.open_community_chest()
            self.send_stickers()

        except KeyboardInterrupt:
            print("Shutdown requested...")

if __name__ == "__main__":
    bot = Bot()
    bot.setup()
    bot.run()