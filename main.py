from grove_lcd import *
import RPi.GPIO as GPIO
import time
import picamera
from threading import Timer

def capture():
	global cameraRecorde
	if cameraRecorde:
		print("Camera allready recorde")
	else:
		cameraRecorde = True
		print("Recorde start")
		setText('Recording video')
		camera.start_recording('video.h264')
		camera.wait_recording(10)
		setText('Stop recording')
		camera.stop_recording()
		setText('Welcome to Fisha')
		cameraRecorde = False

def buttonPressedCB(button):
	time.sleep(.1)
	if GPIO.input(button) :
		setText ("Button %s pressed"%buttons[button]);
		print('Button pressed %s is %s'%(button, buttons[button]))
		thread = Thread(target=capture)
		thread.start()


buttons = {
	4  : "Annule",
	17 : 7,
	27 : 4,
	22 : 1,
	23 : 0,
	24 : 8,
	25 : 5,
	21 : 2,
	20 : 9,
	16 : "OK"
}

GPIO.setmode(GPIO.BCM)

camera = picamera.PiCamera()
camera.resolution(640, 480)
cameraRecorde = False

print('Initialize buttons')

for button, value in buttons.items():
	GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(button, GPIO.RISING, callback=buttonPressedCB, bouncetime=200)

setText('Welcome to Fisha')

input("Press Enter to continue...")

