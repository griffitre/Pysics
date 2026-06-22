# Pysics
A very small and lightweight physics simulator that was originally made for a grade 12 physics project. Though, afterwards, a few other features were added.

## How to run
First, ensure the lastest version Python is installed on your device.

<br>

Once Python is installed, install either pygame or pygame community edition, though pygame ce is preferred. You can do this by running either of the following commands in your computer's terminal: <br>
For normal pygame (outdated + unmaintained idk why you'd use this over ce):
```
py -m pip install pygame
```
For pygame community edition (honestly just use this one instead):
```
py -m pip install pygame-ce
```
If everything is correct, it should install your desired version of pygame. If it doesn't work, try replacing py at the start with python.

<br>

After pygame is installed, clone the repo by going to your desired directory and running the following command:
```
git clone https://github.com/griffitre/Pysics.git
```
Once again, if typed correctly, it should make a copy of the repo and everything in it.

<br>

Now that Python and pygame are both installed and the repo is cloned, just run main.py and it should open a blank screen. Read the controls below to see how to actually view the different menus.

<br>

If you can't get it to work, heres a demo video of it: https://youtu.be/exviO2ezdaE

## Controls
There aren't any difficult complex controls, they're all really simple.

1. Keys 1-6 change the active menu, showing a different type of motion/different physics concept for each one
2. Pressing q simply quits the program
3. While in the ramp forces menu (from pressing 2), pressing the =/+ key will increase the ramp angle, while the -/_ key will decrease it.
4. Furthermore, in the ramp forces menu, pressing the left arrow or right arrow will give the square a boost of speed in the left or right direction respectively. This is used to both get the square onto the ramp and to give it momentum, allowing the program to demonstrate the difference between static and kinetic friction force.

