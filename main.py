#!/usr/bin/python3
import pip
import subprocess
import time
import os
import datetime as dt
from threading import Thread
import socket
import string
from enum import Enum

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
    global ser
    global state
    if cameraRecorde:
        print("Camera allready recorde")
    else:
        try:
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
                raise

            print('File renamed')
            ser.write(b';Fermer la poubel')
            state = State.WaitForTrashClose

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
        except:
            state = State.WaitForTrashClose

def askForCode():
    global code
    global state
    global ser
    state = State.WaitForLoggin
    ser.write(b';Identifiez vous:\n')
    code.clean()

def badCode():
    ser.write(b';Code invalide')
    time.sleep(3)
    askForCode()

def valideCode(code):
    global userLogged
    global state
    userLogged = True
    ser.write(b';Deposez votre\npoubel')
    state = State.WaitForTrashReady

class Code():
    global state
    p_code = []

    def append(self, c):
        global ser
        if c >= b'0' and c <= b'9':
            self.p_code.append(c)
            ser.write(c)
        elif c == b'#':
            if len(self.p_code) != 5:
                print('bade code, length : ', len(self.p_code))
                print(self.p_code)
                badCode()
            else:
                valideCode(self.p_code)
        elif c == b'*':
            askForCode()


    def clean(self):
        self.p_code = []

    def get(self):
        return self.p_code

class State(Enum):
    WaitForLoggin = 1
    WaitForTrashReady = 2
    WaitForPicture = 3
    WaitForTrashClose = 4

state = State.WaitForLoggin

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

code = Code()
askForCode()

while True:
    read = ser.read()
    if read == b';':
        read = ser.read()
        if read == b'b':
            print("Button pressed ");
            if state is State.WaitForTrashReady:
                ser.write(b';Analyse en cours...')
                thread = Thread(target=capture)
                thread.start()
                state = State.WaitForPicture
            if state is State.WaitForTrashClose:
                state = State.WaitForLoggin
                askForCode()
    else:
        if state is State.WaitForLoggin:
            print("read ", read)
            code.append(read)

    #thread = Thread(target=capture)
    #thread.start()
