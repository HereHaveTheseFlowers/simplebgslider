import ctypes
import sched
import time
import os

images = []
root = os.scandir()
event_schedule = sched.scheduler(time.time, time.sleep)
global num
num = 0
image = ''
speed = 3
ROOT_DIR = os.path.abspath(os.curdir)
picturefolder = ''

for entry in root:
    if entry.is_dir() and entry.name == "pictures":
        picturefolder = entry.path

def attempttochangebg():
    if not os.path.isfile(ROOT_DIR + "\\config.txt"):
        return
        print('couldnt find config.txt :< ')
    with open('config.txt', 'r') as config:
        lines = config.readlines()
    if len(lines) >= 3:
        speed = int(lines[2].replace('speed: ', ''))
        if lines[1] == "stop: true\n":
            return
    else:
        return
    global num
    images = []
    for newimage in os.scandir(picturefolder):
        images.append(newimage.name)
        print(newimage.name)
    if(len(images) == 0):
        print("there are no images in the picture folder...")
        return
    image = ROOT_DIR + "\\pictures\\" + images[num]
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image , 0)
    print("made a new bg")
    if num >= (int(len(images)) - 1):
        num = 0
    else:
        num = num + 1
    event_schedule.enter(speed, 1, attempttochangebg)

event_schedule.enter(speed, 1, attempttochangebg)
event_schedule.run()
