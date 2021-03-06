# Wow Fishbot by Snacks-Razorgore

The bot utilizes opencv template matching. This means it searches for an image in an image. Read more here: https://docs.opencv.org/4.5.2/d4/dc6/tutorial_py_template_matching.html.

It takes a screenshot of your game window and searches for the bobber (template) in it.
If it finds the bobber it takes a screenshot of that specific area and compares it to a new image every 0.5sec.
If the difference is to big (assumed fish is hooked) it passes the coordinates to pyAutoGui which moves the mouse and right clicks the bobber

Personally i leveled my druid to max fishing (shadowlands) and farmed fish basically every day while at work for months (eventually quit wow). Was pretty sweet not ever having to worry about buff food and made some sweet gold on AH.
This script only interacts with the OS and not the game itself, besides pressing keystrokes and mouseclicks.

Notes regarding script settings:
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


https://user-images.githubusercontent.com/60894523/153054490-571a2733-e86d-4264-83f0-b63a2e313248.mp4

