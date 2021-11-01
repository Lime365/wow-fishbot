import cv2
import numpy as np
import mss
import mss.tools
import time
import pyautogui
import time

'''
Wow Fishbot by Snacks-Razorgore

The bot uses opencv template matching. This means it searches for an image in an image. Read more here: https://docs.opencv.org/4.5.2/d4/dc6/tutorial_py_template_matching.html
It takes a screenshot of your game window and searches for the bobber (template) in it.
If it finds the bobber it takes a screenshot of that specific area and compares it to a new image every 0.5sec.
If the difference is to big (assumed fish is hooked) it passes the coordinates to pyAutoGui which moves the mouse and right clicks the bobber

NOTE:
1. RESOLUTION: In theory any should work if you adjust the config but only tested on 1280x720. 
2. POSITION: It is assumed that the game is in the top left corner
3. THRESHOLD: If the bot doesn't find the bobber, or is pressing right click too soon/not at all. Play around with the match_threshold and diff_threshold with debugging on.
It is more likely that you will have to adjust the value for the match_threshold than the diff_threshold
4. MASK: Since different zones have different colors to be able to fish at any location you can use a mask.
The mask overlays the template so it only looks for the "shape". This is useful so you can fish no matter the color of the zone, but might give less matches/no matches at all.
To use a mask, set bobber_img = "bobber_template.png" and bobber_mask = 'bobber_mask.png'  (or create your own template/mask)
To not use a mask, take a small screenshot of the bobber at the location you will be fishing and set it equal to bobber_img and bobber_mask = None
Not using a mask and taking a screenshot of the bobber in the setting you will fish will most of the time yield better result (but is a bit more work for every new area)
5. COUNTS: The fish/lure count might not be 100% accurate. 
If the bot got a false positive on the match AND diff it will count as a bobber clicked.
Also if you already have a lure applied when the bot tries to apply the lure it will count as a lure used
6. DEBUGGING: Set different debugging values to True/False depending on how much information you want to see which is useful for finetuning the bot.
Especially when arriving at a new zone there can be a need to adjust the match threshold.

How to:
1. Set game in top left window with desired resolution (1280x720 recommended)
2. Set your throw key/lure key in the config
3.  a) Without mask: Throw bobber and take a screenshot of it where it lands. Place the image in the same directory as the script and set bobber_img=[img name] 
       in the config (see examples uploaded in repo). Make sure bobber_mask = None
    b) With mask: You can make your own mask or use one of the 3 provided in the repo. Set bobber_mask='bobber_mask.png' and bobber_img='bobber_template.png'
       to use the one provided. Read more on template masks here: https://gregorkovalcik.github.io/opencv_contrib/tutorial_template_matching.html
4. Hide UI (not a must but reduces false positives)
5. Start script
6. Adjust thresholds in config if needed

Ideas:
* Add a keyboard listener to issue commands (pause/start, abort, apply lure off intervall)
* Train a haar cascade model of the bobber (will drastically increase bobber detection)
* Shutdown timer (HS and log out after X minutes)
* Print remaining lure timer
'''
#------ CONFIG --------#
game_size = {"width":1280, "height": 720} # Game screen size
capture_region = 0.66 # From bottom up. 0.5 captures half bottom
throw_key = '1' # Fish keybind
lure = True # Enable auto application of lure (press lure_key every lure_interval)
lure_key = '2' # Macro keybind for applying lure.
lure_interval = 11 # How often (in min) to apply lure
monitor = 1 # Monitor to capture (NOT IMPLEMENTED)
bobber_img = "bobber_terokkar2.png" # Path to template of bobber
bobber_mask = None #'bobber_ma12sk.png' # Path to template mask (must have same dimensions and nr of channels as template). Set = None to not use a mask
pyautogui.PAUSE = 1 # How long in seconds python will wait after a keystroke/mouse action
match_threshold = .65 # Bobber template match threshold. Adjust this if the bot has troubles finding the bobber. Higher = Better match
diff_threshold = 900 # Bobber img comparison threshhold. Adjust this if the bot clicks the bobber too soon or not at all. Higher = Bigger diff
# Debugging options. Use these to
debugging = False # See what the bot is thinking of (Overrides all of the below to True)
log_region_val = False # Print x,y,w,h of screen region which is searched for a match
show_match_img = True # If a match is found show a brief image of where the match area is
log_match_val = True # Print info about the match value to console (used to find the bobber in the image)
log_bobber_loc = False # Print the coordinates to console after a match is found (x,y,w,h)
log_diff_val = False # Print info about the diff value to console (used to tell when a fish is hooked)
#------------------------#


bobbers_clicked = 0
lures_used = 0
timeouts = 0
window={"top": int(game_size["height"] * abs(capture_region-1)), "left": 0, "width": 1280, "height": int(game_size["height"] * capture_region)} # Adjust region to config game_size & captuire region

#----- DEFINE FUNCTIONS ------#

# Input position of wow screen and click once to make it the active window
def start_click(x, y):
    print('Starting fishing session')
    x, y = x + 100, y + 100 #top left corner + some pixels
    pyautogui.click(x,y)

def throw(key):
    print('Throwing...')
    pyautogui.press(key)
    #Let bobble settle in water
    time.sleep(1)

def apply_lure(key, lure_count, sleep=5):
    print('Applying lure...')
    pyautogui.press(key)
    lure_count += 1
    time.sleep(sleep)
    return lure_count


#Grab a picture of the game screen
def screen_region(region, mon_nr = 1):
    if debugging or log_region_val:
        print(f'Grabbing region: {region}')
    with mss.mss() as sct:
        #mon = sct.monitors[mon_nr]
        output = f'fishtemp_{region["width"]}x{region["height"]}.png'
        sct_img = sct.grab(region)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        return output

def click_bobber(loc):
    # Click middle of bobber box
    x,y = loc[0]+loc[2]//2, loc[1]+loc[3]//2
    pyautogui.rightClick(x,y)

    print(f'Got em!')

    pyautogui.moveTo(100,100)



def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    # return the MSE, the lower the error, the more "similar"
    return err


#Find the bobber in a image
def find_bobber(source, bobber, mask=None):

    source = cv2.imread(source, cv2.IMREAD_UNCHANGED)
    bobber = cv2.imread(bobber, cv2.IMREAD_UNCHANGED)
    h = bobber.shape[0]
    w = bobber.shape[1]
    # template match
    if mask:
        mask = cv2.imread(mask, cv2.COLOR_BGR2GRAY)
        match = cv2.matchTemplate(source, bobber, cv2.TM_CCORR_NORMED, mask=mask)
    else:
        match = cv2.matchTemplate(source, bobber, cv2.TM_CCOEFF_NORMED)
    #Get coordinates and value of best/worst match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
    #If isn't good enough
    if max_val < match_threshold:
        if debugging or log_match_val:
            print(f'Match not good enough: {round(max_val,2)} / {match_threshold}')
        else:
            print("I can't see the bobber, trying again...")
        return False
    #Rectangle coordinates
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    #Middle coordinates
    #middle = ( int((bottom_right[0]-top_left[0])/2+top_left[0]), int((bottom_right[1]-top_left[1])/2+top_left[1])   )
    #print(middle)
    if debugging or log_match_val: #Show picture of region with rectangle around the match
        print(f'Match found: {round(max_val, 2)} / {match_threshold}')
    else:
        print('I think I see the bobber!')
        # Draw a rectangle around bobber
    if debugging or show_match_img:
        cv2.rectangle(source, top_left, bottom_right, 255, 2)
        #cv2.imshow('match', match)
        cv2.imshow('Fish', source)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()

    #Adjust coordinates to take into account entire screen (not just the region of screen capture)
    x = top_left[0]+window["left"]
    y = top_left[1]+window["top"]

    return (x,y,w,h)

# Grab first image of bobber then keep comparing it to a new one. If difference is above threshold break out (and right click)
def watch_bobber(rect):
    dict_rect = {"top": rect[1], "left": rect[0], "width": rect[2], "height": rect[3]}
    if debugging or log_bobber_loc:
        print(f'Bobber coordinates: {rect}')
    with mss.mss() as sct:
        sct_img = sct.grab(dict_rect)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output='nothooked.png')
    nothooked = cv2.imread('nothooked.png', cv2.IMREAD_GRAYSCALE)
    #cv2.imshow('BOBBERTROUBLE', nothooked)
    #cv2.moveWindow('BOBBERTROUBLE', 50, 780)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # Grab a new image every 0.5s and compare it to original

    print('Waiting for fish...')
    diff_list = []
    for i in range(40):
         sct_img = sct.grab(dict_rect)
         mss.tools.to_png(sct_img.rgb, sct_img.size, output='hooked.png')
         hooked = cv2.imread('hooked.png', cv2.IMREAD_GRAYSCALE)
         diff = mse(nothooked, hooked)
         diff_list.append(diff)
         #if debugging:
             #print(diff)
         #Probably hooked
         #print(diff_list)
         if diff > diff_threshold:
             if debugging or log_diff_val:
                 print(f'''\nWent above at: {max(diff_list)}\nThreshold: {diff_threshold}\nAvg diff: {sum(diff_list[1:-1])/(len(diff_list)-2)}\nMax diff: {max(diff_list[:-1])}\nMin diff: {min(diff_list[1:])}\n-------''')
             return True
         else:
            time.sleep(0.5)
    if debugging or log_diff_val:
        print('Timed out. Match was false or threshold to high')
        print( f'''Threshold: {diff_threshold}\nAvg diff: {sum(diff_list[1:]) / (len(diff_list) - 1)}\nMax diff: {max(diff_list)}\nMin diff: {min(diff_list[1:])}''')
    return False


if __name__ == '__main__':
    start_click(window["top"], window["left"])
    start = time.time()
    if lure:
        lures_used = apply_lure(lure_key, lures_used)
    while True:
        try:
            timer = time.time() - start
            hours = int(timer//3600)
            minutes = int(timer//60 - hours*60)
            seconds = int(timer - hours*3600 - minutes*60)
            print('\nSession:')
            if timer > 3600:
                print(f'Fished for {hours}h {minutes}m {seconds}s')
            elif timer > 60:
                print(f'Fished for {minutes}m {seconds}s')
            else:
                print(f'Fished for {seconds}s')
            print(f'Bobbers clicked: {bobbers_clicked}')
            print(f'Lures used: {lures_used}')
            print(f'Timeouts: {timeouts}')
            if lure:
                if timer+6 > lures_used * lure_interval*60:
                    lures_used = apply_lure(lure_key, lures_used)
            throw(throw_key)
            bobber_info = find_bobber(screen_region(window, monitor), bobber_img, bobber_mask)
            if not bobber_info: # Match below threshold
                continue
            if watch_bobber(bobber_info):
                click_bobber(bobber_info)
                bobbers_clicked += 1

            else:
                print('Exiting loop...\n')
                timeouts += 1
                continue
        except OSError as err:
            print(f'OSError: {err}')
        except pyautogui.FailSafeException as err:
            print(f'Mouse moved outside monitor: {err}')





