#include <Arduino.h>
#include <Keypad.h>

const byte ROWS = 4; //four rows
const byte COLS = 3; //three columns
char keys[ROWS][COLS] = {
    {'1','2','3'},
    {'4','5','6'},
    {'7','8','9'},
    {'*','0','#'}
};

byte rowPins[ROWS] = {7, 2, 3, 5}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {6, 8, 4}; //connect to the column pinouts of the keypad

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

int LED = 13;

void setup() {
    Serial.begin(9600);
    pinMode(LED, OUTPUT);
    Serial.println("<Startup>");
}

void loop() {
    char key = keypad.getKey();
    if (key)
        Serial.print(key);
}

void serialEvent() {
    while (Serial.available()) {
        Serial.print((char)Serial.read());
    }
}

