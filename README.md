My attempt at upgrading sentdexes gta v self-driving ai for GTA v, it was
originally going to be a fork but i decided that starting from scratch
would be better, some of the code is from his project (gave up on trying to do a
ctypes-only screenshot after a lot of fighting with windows).


# Usage
To get it working yourself, first edit config.json for your game,
current example in for GTA V, here's what all the options do:

 * window_name is the name of games window, you can check that in the task manager
 * model_name is used for the tensorflow log, can be anything just make sure it's unique
 * model_save_name is the name used for saving the model, can be anything too as long as it ends with .tflearn
 * save_dir is the name of the folder that will be created inside the data folder for everything related to this project (Training data and the model)
 * max_samples_per_file is the number of samples to store in memory before writing it to a file, more is better but uses more RAM
 * FPS is how many samples will be recorded every second, NVIDIA recommends 10

After that just run your game and make sure you have a controller plugged in,
if you have more then one controller it's fine it will ask you which one you want
to record data from. First script to run is data_gathering.py, only argument is
the number of seconds it will record for, so "python data_gathering.py 60" will
record for a minute (about 600 samples at 10fps).

Now that we have our precious data we need to train a model, that's done by running
train_model.py, the number of EPOCHS it will run for is inside the file so you have
to edit it (todo: make it an argument).

Last step is running test_model.py, it will load the trained model and
start predicting stuff from your active game window and sending the results to it,
currently you need to have vjoy installed and x360ce on the games folder.

# Setting up stuff

Currently the project has a bunch of requirements, i recommend creating an anaconda env for the project.

Requires packages are:

 * Tensorflow GPU 1.0 (versions above 1.0 don't seem to work with tflearn)
 * TFLearn
 * OpenCV
 * pygame (used for data gathering)
 * numpy
 * pyvjoy (not on pip, clone from github and put vjoyinterface.dll inside its folder)
 * x360ce on the games folder, used to convert directinput to xinput
 * vjoy

Yep, quite the list, pygame, pyvjoy, x360ce and vjoy can all be removed if i get
https://github.com/bayangan1991/PYXInput/ to work.

