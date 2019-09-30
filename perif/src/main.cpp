#include <Arduino.h>
#include <Keypad.h>
#include <LiquidCrystal_I2C.h>

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

LiquidCrystal_I2C lcd(0x27,16,4);

void setup() {
    Serial.begin(9600);
    lcd.init();
    lcd.backlight();
    lcd.setCursor(0, 0);
    lcd.print("Coucou");
    Serial.println("<Startup>");
}

void loop() {
    char key = keypad.getKey();
    if (key)
        Serial.print(key);
}

void serialEvent() {
    while (Serial.available()) {
        char key = Serial.read();
        if (key == '\n')
            lcd.setCursor(0,1);
        else if (key == ';')
            lcd.clear();
        else {
            lcd.print(key);
            Serial.print(key);
        }
    }
}

