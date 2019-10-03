#!/usr/bin/python3
import pip
import subprocess
import time
import os
import datetime as dt
from threading import Thread
import socket
import string


try:
    import RPi.GPIO as GPIO
except ImportError:
    pip.main(['install', 'RPi.GPIO'])
    import RPi.GPIO as GPIO
try:
    import picamera
except ImportError:
    pip.main(['install', 'picamera'])
    import picamera

try:
    import serial
except ImportError:
    pip.main(['install', 'pyserial'])
    import serial

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


class Code:
    code = []
    def append(c):
        code.append(c)

    def clean:
        code = []


relay = 26

GPIO.setmode(GPIO.BCM)

cameraRecorde = False

GPIO.setup(relay, GPIO.OUT, initial=GPIO.LOW)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)

ser.write(b'p')
ser.flush()
read = ser.read_until(';')

if not read.endswith(b'PONG;'):
    raise Exception('Do not manage to connect to hardware')

ser.timeout=None

ser.write(b'w')
ser.write(b';Identifiez vous:\n');

code = Code()

while True:
    read = ser.read()
    print("read ", read)
    ser.write(read)
    code.append(read)

    #thread = Thread(target=capture)
    #thread.start()
