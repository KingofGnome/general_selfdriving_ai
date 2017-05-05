My attempt at upgrading sentdexes gta v self-driving ai for GTA v, it was
originally going to be a fork but i decided that starting from scratch
would be better, some of the code is from his project (gave up on trying to do a
ctypes-only screenshot after a lot of fighting with windows).

What works:

 * Saving screenshots and controller data
 * Taining a model with that data
 * Predicting values from screenshots in real time


Current problems:

 * Code organization is bad
 * Bunch of hardcoded stuff
 * Actually sending the input to the game is not working,
 only method i found was using vjoy and most games don't support it properly,
 gta V seems to support it but when i try to configure it the joystick doesn't work :(