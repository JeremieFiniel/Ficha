#!/usr/bin/python3
import RPi.GPIO as GPIO
import subprocess
import time
import picamera
import os
import datetime as dt
from threading import Thread
import socket

server = socket.socket()
server_host = "192.168.1.50"
server_port = 8123

def setText(text):
    print(text);


def capture():
    global cameraRecorde
    if cameraRecorde:
        print("Camera allready recorde")
    else:
        cameraRecorde = True

        print("Start motor")
        GPIO.output(relay, GPIO.HIGH)

        date = dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

        camera = picamera.PiCamera()
        print("Recorde start")
        setText('Recording video')

        camera.start_recording(date+'.h264')
        camera.wait_recording(10)

        print("Stop motor")
        GPIO.output(relay, GPIO.LOW)

        setText('Stop recording')
        camera.stop_recording()
        setText('Identifiez vous')
        print("Recorde stop")
        camera.close()
        cameraRecorde = False

        print("Rename video file")
        command = "MP4Box -add {}.h264 {}.mp4".format(date, date)
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))

        print('File renamed')

        print('Remove old file')
        os.remove(date+'.h264')

        print('Send video to server')
        server.connect((server_host, server_port))
        server.send(date+'.mp4')
        with open(date+'.mp4', 'rb') as file:
            chunk = file.read(1024*8)
            while chunk:
                server.send(chunk)
                chunk = file.read(1024*8)

        print("done sending")
        server.close()



relay = 26

GPIO.setmode(GPIO.BCM)

cameraRecorde = False

GPIO.setup(relay, GPIO.OUT, initial=GPIO.LOW)

setText('Identifiez vous')

while True:
    raw_input('Press Enter to continue...')
    thread = Thread(target=capture)
    thread.start()
