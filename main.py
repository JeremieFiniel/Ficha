from grove_lcd import *
import RPi.GPIO as GPIO
import time
import picamera
from threading import Thread

def capture():
	global cameraRecorde
	if cameraRecorde:
		print("Camera allready recorde")
	else:
		camera = picamera.PiCamera()
		cameraRecorde = True
		print("Recorde start")
		setText('Recording video')
		camera.start_recording('video.h264')
		camera.wait_recording(10)
		setText('Stop recording')
		camera.stop_recording()
		setText('Welcome to Fisha')
		print("Recorde stop")
		camera.close()
		cameraRecorde = False

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

setText('Welcome to Fisha')

input("Press Enter to continue...")

