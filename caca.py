from subprocess import check_output,call
from io import StringIO
import pandas as pd
import numpy as np
from time import sleep
from subprocess import Popen
import subprocess
import sys
def play_sound(id):
    if id==0:
        z = Popen(["play","beat.wav"],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif id == 1:
        z =Popen(["play","hihat.wav"],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif id == 2:
        z =Popen(["play","piano-D.wav"],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif id == 3:
        z =Popen(["play","piano-F.wav"],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif id == 4:
        z =Popen(["play","piano-G.wav"],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif id == 5:
        # z =Popen(["play","piano-F.wav"],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pass
    elif id == 6:
        pass
        # z =Popen(["play","piano-G.wav"],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def play_unit(row):
    for enc in np.transpose(compass)[row]:
        play_sound(enc)

prev=-1
# compass=np.array([[0,1,0,1,0,1,0,1], [2,-1,3,-1,4,-1,2,-1]])
compass=np.array([[-1,-1,-1,-1,-1,-1,-1,-1], [-1,-1,-1,-1,-1,-1,-1,-1]])
cnt=0
row=0
while True:
    sleep(0.4)

    momentary = StringIO(check_output(["tail","-n","4","/tmp/ramdisk/live.csv"]).decode("utf-8"))
    x = pd.read_csv(momentary,header=None).iloc[:-1,:3]
    stds = x.std().values
    play_unit(cnt)
    try:
#\s\s\s\s#preds = classifier.predict(x)
        res = -1 if max(stds)<2500 else np.argmax(stds)
        sign=1
        nneg =0
        for rowwy in x.values:
            if rowwy[res] < 0:
                nneg+=1
        #nneg = np.count_nonzero(x[:,res] < 0)
        npos = len(x) - nneg
        print(stds)
        if nneg>npos:
            sign=-1

        if res==prev:
            if cnt == 7:
                row += 1
            cnt = (cnt + 1)%8
            compass = np.vstack([compass,[-1,-1,-1,-1,-1,-1,-1,-1]])
            continue
#        else:
#            print("DIRECTION CHANGED")

        if res == -1:
        #    print("NOTHING")
            prev=res
            continue
      #      check_output(["play","piano-e.wav"])

        if res == 0:
            if sign > 0:
                print("forward")
                compass[row+1,(cnt+1)%8] = 2
            else:
                print("backward")
                compass[row+1,(cnt+1)%8] = 3
        elif res == 1:
            if sign > 0:
                print("right")
                compass[row+1,(cnt+1)%8] = 4
            else:
                print("left")
                compass[row+1,(cnt+1)%8] = 4
        elif res == 2:
            if sign > 0:
                print("up")
                compass[row+1,(cnt+1)%8] = 5
            else:
                print("down")
        else:
            print("NONE",res)
        prev=res
#\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s
#    print(stds)
    except Exception as e:
        print( "<p>Error: %s</p>" % str(e) )
    compass = np.vstack([compass,[-1,-1,-1,-1,-1,-1,-1,-1]])
    if cnt == 7:
        row += 1
    cnt = (cnt + 1)%8
#\s\s\s\s\s\s\s\s\s\s\s\s
