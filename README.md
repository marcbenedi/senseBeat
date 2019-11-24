# SenseBeat

This project is created for hackTUM '19.
Devpost : https://devpost.com/software/freebeat

## Inspiration
Music is the essential part of our lives. Everybody has a melody in mind sometimes. We want to make your movements audible, so you can hear your body’s sound. Our inspiration originally came from playing drums. We imagined, with motion detection technology, one can use motion to make music.

## What it does
It is a life experience application that takes movements and turns them into sounds. Using motion detector as input provider, we use directional movements to create music notes, and by using the notes your own songs.

## How I built it
We used Arduino Nano and a motion sensor(MPU6050) to create the data. We used machine learning and statistical analysis to estimate the direction of the motion using the accelerator. We used Python for data analysis and musical display. For the music notes, we used .wav files of piano key recordings, guitar key recordings and some drum beat recordings.

## Challenges I ran into
We had a problem doing the setup for Bluetooth. It took a lot of time to sustain the communication between the Bluetooth device and the computer. We had a problem finding appropriate music notes. The hardware that we had is not suitable for the body, so we think about using mobile phones to collect movement data.

## Accomplishments that I'm proud of
Setting up the hardware part and collecting data from it. Analyzing this data and assigning it to the voices. Getting a song from the movement of a person.

## What I learned
We knew how to use Arduino, but Arduino Nano was new for us. We learned getting signals from sensors and board by physical connection. Also, communication with Bluetooth is new for everyone in group.

## What's next for SenseBeat
Option to create other instrument sounds such as bass, violin, etc. Make the notes have other duration options. Learn more gestures, make the interaction continuous.
