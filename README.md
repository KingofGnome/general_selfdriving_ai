My attempt at upgrading sentdexes gta v self-driving ai for GTA v into a more
general purpuse project for self driving cars in games, it was
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
 * input_type is your kind of input device, options are "xinput" or "dinput", see setup section for more information.

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

First install [anaconda](https://www.continuum.io/downloads)

Now create an anaconda environment with python 3.5 with the command `conda create
--name ENVNAME python=3.5`

Now it's time to install the requirements, make sure that your env is activated for this.

Obligatory packages:

 * Tensorflow GPU 1.0rc2, to make sure that everything will work install it with
 `pip install https://storage.googleapis.com/tensorflow/windows/gpu/tensorflow_gpu-1.0.0rc2-cp35-cp35m-win_amd64.whl`
 * TFLearn. - `pip install tflearn`
 * OpenCV - `conda install opencv`
 * numpy - `conda install numpy`

Packages used for input, you only need to install the one you use:

 * pygame -  `pip install opencv`, used for xinput controller input
 * pygame_sdl2 - Currently too hard to install, used for dinput controller input (once it's on pip i can use this for dinput and xinput)


There are two methods of output, one is harder to setup and has bad support for games but
works on a default secure installation of windows 10 64bit, the other one is very easy to setup and works
much better but in some cases requires you to disable UEFI secureboot or boot into
test mode every time you want to use it because it requires the installation of an unsigned driver.

The harder method that requires no bios changes is

 * [vjoy](http://vjoystick.sourceforge.net/site/index.php/download-a-install/download)  - Used to create an emulated directinput device, make sure you open vjoy configurator after installing it and create a device
 * [pyvjoy](https://github.com/tidzo/pyvjoy)  - used to interact with vjoy from python. It's not on pip so you have to download the zip, throw it on the projects folder, find vjoyinterface.dll in your system (you need to have vjoy installed) and put it inside pyvjoys folder.
 * x360ce on the games folder - If the game you're working with only supports xinput, you need to use x360ce to convert the input

Now the easy way that might require you to make some bios changes or boot into test mode:

 * SCPVbus, this driver allows the creation of virtual xinput devices,
 to install it from [here](https://github.com/shauleiz/vXboxInterface/releases/download/v1.0.0.1/ScpVBus-x64.zip),
 open cmd with admin right, cd into the folder and run `devcon.exe install ScpVBus.inf Root\ScpVBus`.
 If it works, NICE! if it doesn't, you'll have too google how to disable secureboot or if you want to
  disable it only until you reboot again, search for how to boot into test mode.
 * [PYXInput](https://github.com/bayangan1991/PYXInput) - `pip install PYXInput`

