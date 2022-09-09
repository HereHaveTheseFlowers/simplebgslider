import ctypes
import sched
import time
import os
import PySimpleGUI as sg
import threading
import winshell
from win32com.client import Dispatch

speed = 120
images = []
root = os.scandir()
event_schedule = sched.scheduler(time.time, time.sleep)
global num
num = 0
image = ''
ROOT_DIR = os.path.abspath(os.curdir)
event_schedule = sched.scheduler(time.time, time.sleep)
startup = winshell.startup()

# List all images in the pictures folder
def scanpictures():
    global images
    images = []
    for entry in root:
        if entry.is_dir() and entry.name == "pictures":
            pictures = os.scandir(entry.path)
            for image in pictures:
                images.append(image.name)
scanpictures()

def start():
    lines = checkconfig()
    lines[1] = "stop: false\n"
    lines[0] = "start: true\n"
    with open('config.txt', 'w') as config:
        config.writelines(lines)
    if os.path.isfile(ROOT_DIR + "\\simplebgslider_script.exe"):
        os.startfile(ROOT_DIR + "\\simplebgslider_script.exe")
        if window and window['alarm']:
            window['alarm'].update("Started simplebgslider_script.exe! You can close the program now.")
        if window:
            window.close()
    else:
        if window and window['alarm']:
            window['alarm'].update("simplebgslider_script.exe is missing...")

def stop():
    lines = checkconfig()
    lines[1] = "stop: true\n"
    with open('config.txt', 'w') as config:
        config.writelines(lines)

def checkconfig():
    if not os.path.isfile(ROOT_DIR + "\\config.txt"):
        lines = ['start: false', 'stop: false', 'speed: ']
        lines[2] = 'speed: ' + str(speed)
        with open('config.txt', 'w') as config:
            config.write('\n'.join(lines))
        with open('config.txt', 'r') as config2:
            lines2 = config2.readlines()
        return lines2
    else:
        with open('config.txt', 'r') as config1:
            lines1 = config1.readlines()
        if len(lines1) >= 3:
            return lines1
        else:
            lines3 = ['start: false', 'stop: false', 'speed: ']
            lines3[2] = 'speed: ' + str(speed)
            with open('config.txt', 'w') as config3:
                config3.write('\n'.join(lines3))
            with open('config.txt', 'r') as config4:
                lines4 = config4.readlines()
            return lines4
layout = [[sg.Text("Hi! This this a simple bg wallpaper slider (windows only).\nDrop all the images into the pictures folder, then press Start down here.")],
            [sg.Text("Currently in the folder there are " + str(len(images)) + " pictures")],
            [sg.Text('Change slide every: (in seconds)', size =(25, 1)), sg.Input(default_text='120', key='speed')],
            [sg.Text("", key='alarm' )],
            [sg.Button("Start the program")],
            [sg.Button("Make it start on win launch")],
            [sg.Button("Stop the program (also the one that is running on startup)")],
            [sg.Button("Close")]]

# Create the window
window = sg.Window("SimpleBGSlider", layout)

# Create an event loop
while True:
    event, values = window.read()
    # Start
    if event == "Start the program":
        if values['speed']:
            speed = values['speed']
        lines = checkconfig()
        lines[2] = "speed: " + str(speed)
        with open('config.txt', 'w') as config:
            config.writelines(lines)
        stop()
        sleepamount = int(speed) + 2
        window['alarm'].update("The program will start in " + str(sleepamount) + " seconds. Dont close this window, it will automatically close.")
        def callback():
            event_schedule.enter(sleepamount, 1, start)
            event_schedule.run()
        t = threading.Thread(target=callback)
        t.start()
    # Stop the program if the user presses the Stop button
    if event == "Stop the program (also the one that is running on startup)":
        stop()
        if window and window['alarm']:
            window['alarm'].update("Stopping the program... This may take "+str(speed)+" seconds but you can close the program now.")
    # End program if user closes window or
    # presses the Close button
    if event == "Close" or event == sg.WIN_CLOSED:
        break
    if event == "Make it start on win launch":
        if os.path.isfile(ROOT_DIR + "\\simplebgslider_script.exe"):
            path = os.path.join(startup, "startup.lnk")
            target = ROOT_DIR+"\\simplebgslider_script.exe"
            wDir = ROOT_DIR
            icon = ROOT_DIR+"\\simplebgslider_script.exe"
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = icon
            shortcut.save()
            if window and window['alarm']:
                window['alarm'].update("Success! Now the program will start on windows launch. You can disable it in TaskManager")
        else:
            if window and window['alarm']:
                window['alarm'].update("simplebgslider_script.exe is missing...")

window.close()


