from grove_lcd import *
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

def capture():
	global cameraRecorde
	if cameraRecorde:
		print("Camera allready recorde")
	else:
		date = dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
		camera = picamera.PiCamera()
		cameraRecorde = True
		print("Recorde start")
		setText('Recording video')
		camera.start_recording(date+'.h264')
		camera.wait_recording(10)
		setText('Stop recording')
		camera.stop_recording()
		setText('Welcome to Fisha')
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

		print "done sending"
		server.close()



def buttonPressedCB(button):
	time.sleep(.1)
	if GPIO.input(button) :
		setText ("Button %s pressed"%buttons[button]);
		print('Button pressed %s is %s'%(button, buttons[button]))
		if buttons[button] == "OK":
			thread = Thread(target=capture)
			thread.start()


buttons = {
	4  : "Annule",
	17 : 1,
	18 : 7,
	27 : 0,
	22 : 8,
	23 : 4,
	24 : 5,
	25 : 2,
	5 : "OK",
	6 : 9,
	13 : 6,
	19 : 3
}

GPIO.setmode(GPIO.BCM)

cameraRecorde = False

print('Initialize buttons')

for button, value in buttons.items():
	GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(button, GPIO.RISING, callback=buttonPressedCB, bouncetime=200)

setText('Identifiez vous')

while True:
	raw_input('Press Enter to continue...')
	thread = Thread(target=capture)
	thread.start()
