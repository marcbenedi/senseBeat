from subprocess import check_output,call
from io import StringIO
import pandas as pd
import numpy as np
from time import sleep
from subprocess import Popen
import subprocess
import sys
import curses
import keyboard

def add_empty_row(array):
    return np.vstack([array,[-1,-1,-1,-1,-1,-1,-1,-1]])

def play_sound(id):
    sound = ""
    if id==0:
        sound = "beat.wav"
        z = Popen(["play",sound],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif id == 1:
        sound = "hihat.wav"
        z = Popen(["play",sound],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif id == 2:
        if piano:
            sound = "piano-C.wav"
        else:
            sound = "guitar-C.wav"
        z = Popen(["play",sound],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif id == 3:
        if piano:
            sound = "piano-D.wav"
        else:
            sound = "guitar-D.wav"
        z = Popen(["play",sound],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif id == 4:
        if piano:
            sound = "piano-E.wav"
        else:
            sound = "guitar-E.wav"
        z = Popen(["play",sound],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif id == 5:
        sound = "piano-F.wav"
        z = Popen(["play",sound],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif id == 6:
        if piano:
            sound = "piano-G.wav"
        else:
            sound = "guitar-G.wav"
        z = Popen(["play",sound],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif id == 7:
        if piano:
            sound = "piano-A.wav"
        else:
            sound = "guitar-A.wav"
        z = Popen(["play",sound],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def play_unit(row):
    for enc in np.transpose(compass)[row]:
        play_sound(enc)

piano = True
beat = True

def print_instructions():
    if piano:
        stdscr.addstr(3, 0, "[1]: Select instrument - (Piano) | Guitar")
    else:
        stdscr.addstr(3, 0, "[1]: Select instrument - Piano | (Guitar)")
    if beat:
        stdscr.addstr(4, 0, "[2]: Select beat - (Beat 1) | Beat 2")
    else:
        stdscr.addstr(4, 0, "[2]: Select beat - Beat 1 | (Beat 2)")
    stdscr.addstr(5, 0, "[3]: Clear loop")

stdscr = curses.initscr()
# curses.noecho()
# curses.cbreak()

prev=-1
# compass=np.array([[0,1,0,1,0,1,0,1], [2,-1,3,-1,4,-1,2,-1]])
# compass=np.array([[0,1,0,1,0,1,0,1], [-1,-1,-1,-1,-1,-1,-1,-1]])
compass=np.array([[0,1,0,1,1,0,0,1], [-1,-1,-1,-1,-1,-1,-1,-1]])
# compass=np.array([[0,0,1,0,1,0,0,1], [-1,-1,-1,-1,-1,-1,-1,-1]])
cnt=0
row=0

while True:
    sleep(0.4)
    play_unit(cnt)
    stdscr.clear()
    stdscr.refresh()

    if keyboard.is_pressed('1'):
        if piano:
            piano = False
        else:
            piano = True

    if keyboard.is_pressed('2'):
        if beat:
            beat = False
            compass[0] = [0,0,1,0,1,0,0,1]
        else:
            beat = True
            compass[0] = [0,1,0,1,1,0,0,1]

    if keyboard.is_pressed('3'):
        compass = np.array(compass[0])

    stdscr.addstr(0, 0, 'Beat: '+str(cnt)+' Iteration:'+str(row))
    # stdscr.refresh()


    try:
        x = StringIO(check_output(["tail","-n","5","/tmp/ramdisk/live.csv"]).decode("utf-8"))
        x = pd.read_csv(x,header=None).iloc[:-2,:3]
        stds = x.std().values

        res = -1 if max(stds)<2500 else np.argmax(stds)
        sign=1
        nneg =0

        for rowwy in x.values:
            if rowwy[res] < 0:
                nneg+=1

        npos = len(x) - nneg

        if nneg>npos:
            sign=-1

        if res==prev:
            if cnt == 7:
                row += 1
            cnt = (cnt + 1)%8
            compass = add_empty_row(compass)
            stdscr.addstr(1, 0, "Action: None")
            print_instructions()
            stdscr.refresh()
            continue
        if res == -1:
            prev=res
            stdscr.addstr(1, 0, "Action: None")
            print_instructions()
            stdscr.refresh()
            continue
        if res == 0:
            if sign > 0:
                stdscr.addstr(1, 0, "Action: Forward")
                # stdscr.refresh()
                compass[row+((cnt+1)//8),(cnt+1)%8] = 2
            else:
                stdscr.addstr(1, 0, "Action: Backwards")
                # stdscr.refresh()
                compass[row+((cnt+1)//8),(cnt+1)%8] = 3
        elif res == 1:
            if sign > 0:
                stdscr.addstr(1, 0, "Action: Right")
                # stdscr.refresh()
                compass[row+((cnt+1)//8),(cnt+1)%8] = 4
            else:
                stdscr.addstr(1, 0, "Action: Left")
                # stdscr.refresh()
                compass[row+((cnt+1)//8),(cnt+1)%8] = 5
        elif res == 2:
            if sign > 0:
                stdscr.addstr(1, 0, "Action: Up")
                # stdscr.refresh()
                compass[row+((cnt+1)//8),(cnt+1)%8] = 6
            else:
                stdscr.addstr(1, 0, "Action: Down")
                # stdscr.refresh()
                compass[row+((cnt+1)//8),(cnt+1)%8] = 7
        else:
            stdscr.addstr(1, 0, "Action: None")
            # stdscr.refresh()
        prev=res

    except Exception as e:
        print( "<p>Error: %s</p>" % str(e) )

    print_instructions()

    compass = add_empty_row(compass)
    if cnt == 7:
        row += 1
    cnt = (cnt + 1)%8

    # curses.echo()
    # curses.nocbreak()
    # curses.endwin()
