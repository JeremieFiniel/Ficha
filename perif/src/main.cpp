#include <Arduino.h>
#include <Keypad.h>
#include <LiquidCrystal_I2C.h>


#ifdef DEBUG
#define DEBUG(x) Serial.x
#else
#define DEBUG(x)
#endif

const byte ROWS = 4; //four rows
const byte COLS = 3; //three columns
char keys[ROWS][COLS] = {
    {'1','2','3'},
    {'4','5','6'},
    {'7','8','9'},
    {'*','0','#'}
};

enum State {
    INIT,
    WAIT,
};

enum Commande {
    NO,
    WRITE,
    PING
};


byte rowPins[ROWS] = {8, 3, 4, 6}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {7, 9, 5}; //connect to the column pinouts of the keypad

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

LiquidCrystal_I2C lcd(0x27,16,4);

enum Commande commande;
enum State state;

void buttonPressed() {
    Serial.print(";b");
}

void setup() {
    Serial.begin(9600);
    lcd.init();
    lcd.backlight();
    lcd.setCursor(0, 0);
    lcd.print("Strating up");

    DEBUG(println("<Startup>"));

    attachInterrupt(digitalPinToInterrupt(2), buttonPressed, RISING);

    commande = NO;

    state = INIT;
}

void loop() {
    char key = keypad.getKey();
    if (key)
        Serial.print(key);
}

void serialEvent() {
    while (Serial.available()) {
        char key = Serial.read();
        switch (commande) {
            case NO:
                switch (key) {
                    case 'w':
                        commande = WRITE;
                        DEBUG(println("Go to write mode"));
                        break;
                    case 'p':
                        Serial.print("PONG;");
                        break;
                }
                break;
            case WRITE:
                if (key == '\n')
                    lcd.setCursor(0,1);
                else if (key == ';')
                    lcd.clear();
                else if (key == '$')
                    commande = NO;
                else {
                    lcd.print(key);
                    DEBUG(print(key));
                }
                break;
        }
    }
}

