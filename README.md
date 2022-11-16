# Wow Fishbot by Snacks-Razorgore

## Introduction
The bot utilizes opencv template matching. This means it searches for an image in an image. Read more here: https://docs.opencv.org/4.5.2/d4/dc6/tutorial_py_template_matching.html.

It takes a screenshot of your game window and searches for the bobber (template) in it.
If it finds the bobber it takes a screenshot of that specific area and compares it to a new image every 0.5sec.
If the difference is to big (assumed fish is hooked) it passes the coordinates to pyAutoGui which moves the mouse and right clicks the bobber

Personally I leveled my druid to max fishing when classic came out and farmed fish basically every day while at work for months (eventually quit wow). Was pretty sweet not ever having to worry about buff food and made some decent gold on AH. And now after resuming Wow at the end of Shadowlands I'm farming Hirukon in Zereth Mortis.
This script only interacts with the OS and not the game itself by sending keystrokes and mouseclicks.


## Requirements
- Python installed
- Some command line knowledge to run the script (I use GitBash, but probably works as good with Windows CMD/Powershell)
- A text editor to tweak the settings. I'd recommend VSCode with Python plugin installed to get the text highlightning, but a normal notepad works as well.
- Win10 (Never tried it on anything else)
- Able to take screenshot of a region (strongly recommend Greenshot which is free and binds to your PrintScreen button)

## Installation
1. In the command line cd into location where you cloned the repo
2. (Optional) Create a python venv and activate it. It's fairly easy to do but if you only installed python for this you can skip this step. 
3. ´pip install requirements.txt´
4. cd into /fishbot


## Script settings
# Don't touch:
If you just want it to work out of the box, no need to change these. Just follow the instructions
**game_size**: Should be set to your in game resolution. In theory any should work but only tested on 1280x720.
**capture_region**: How big in % from the bottom of the game window and up should be scanned for a bobber (0.66 i.e 2/3 seem to work well).
**bobber_mask**: None or path to the template mask if you use one.
**pyautogui.PAUSE**: How long in seconds python will wait after a keystroke/mouse action.
**monitor**: NOT IMPLEMENTED. Intended for if you have more than 1 monitor. 

# Game 
**throw_key**: The key on your actionbar for casting.
**lure**: If a lure should be applied at the start and at the end of every *lure_interval*.
**lure_key**: The key on your actionbar for applying lure.
**lure_interval**: How many minutes before applying a new lure.


# Debugging
I'd recommend leaving ´log_match_val´ on. But rest can be useful for troubleshooting. ´show_match_image´ is useful to see if you get a match on something that isn't the bobber which indicates the ´match_threshold´ needs tweaking. But it's also very satisfying to leave on just to see when it detects it.
**debugging** Sets all of the below to True
**log_region_val** Print x,y,w,h of screen region which is searched for a match
**show_match_img** If a match is found show a brief image of where the match area is
**log_match_val** Print info about the match value to console (used to find the bobber in the image)
**log_bobber_loc** Print the coordinates to console after a match is found (x,y,w,h)
**log_diff_val** Print info about the diff value to console (used to tell when a fish is hooked)

# Do tweak
Change ´bobber_img´ when you swap to a new spot. ´diff_threshold´ generally needs to be set once and that's it, mine is 900 cause i use a laptop with low resolution. If you use a higher resolution you might need to increase this. ´match_threshold´ depends a bit the spot, but generally sits pretty good somewhere between 0.6-0.7
**bobber_img**: Path to the image template which will be used to look for a match. Every time you change spot, this should be updated for best results.
**match_threshold**: Is pretty good at .65 but can need a nudge up or down if you don't find the bobber. Depends on the spot
**diff_threshold**: Rarely needs changing but can be good sometimes, 900 works 9/10 times.


Instructions:
1. Set the game in windowed mode and change resolution to 1280x720 (or the value that you set in ´game_size´)
2. Move the window to the top left corner of it is in the top left corner of the display
3. In the action bars bind the cast key to 1, and lure key to 2 (or what you changed the script settings to)
4. In the game hide UI (Alt+Z usually) and zoom the camera to first person PoV. 
5. Throw a cast **manually** and take a region screenshot of **only the bobber**
6. Save it in the same folder as the script with a .png extension (E.g "terokkar.png")
7. Change the variable ´bobber_img´ to the file name (E.g "terokkar.png")
8. Start the script
9. Monitor for a bit, if it works then congratz. Sit back and relax :)
10. If it doesn't yield you any fish, check below:

Problem: It's re-casting to much
Solution: Tweak the ´match_threshold´ variable

Problem: It doesn't respond when a fish is on the hook
Solution: This can depend on 2 things. Either it think it found the bobber while it didn't, and is watching the wrong spot, or the ´diff_threshold´ is to high. To determine which, turn on ´show_match_img´ and see if it draws a rectangle around the bobber. If it does, the threshold is to high. If it draws the rectangle on the wrong spot (i.e not around the bobber), the ´match_threshold´ is too low.

## Using a mask
With a mask you don't have to take a new screenshot whenever you change to a new spot. It kind of worked but the success rate was much lower. But leaving it here in case someone wants to tinker with it. To use a mask set ´bobber_mask´ to the name of the mask file. Read more on template masks here:  https://gregorkovalcik.github.io/opencv_contrib/tutorial_template_matching.html

## Ideas I never got around to do:
* Add a keyboard listener to issue commands (pause/start, abort, apply lure off intervall)
* Train a haar cascade model of the bobber (will drastically increase bobber detection)
* Shutdown timer (HS and log out after X minutes)
* Print remaining lure timer
* Jump, dance, use a toy or go afk for a few minutes at random intervalls to not make it seem like your botting


https://user-images.githubusercontent.com/60894523/153054490-571a2733-e86d-4264-83f0-b63a2e313248.mp4

