# Ficha

This project contain 3 subprojects for different target
- Device side: code to run in Raspberry
- Arduino side (perif): code for arduino to interact with LCD screen, keypad and button
- Server side: code to run in server to retreave images from devices

## Device side

In root directory.
Contain requirements to install in raspberry.
Contain main.py, the programme in itself.

To install requrement :
`pip install -r requirements.txt`

To run Ficha programme in raspberry (Arduino flashed must be connected throw USB)
`./main.py`

## Arduino side

In perif directory.
Contain code for arduino to interact with LCD screen, keypad and button.
Project is based on platform.io and currently configure to run on Arduino Nano.

To build project :
`pio run`

To upload code to USB connected Arduino :
`pio run -t upload`

## Server side

In server directory.
To run server, node.js must be installed :
`node server.js`
