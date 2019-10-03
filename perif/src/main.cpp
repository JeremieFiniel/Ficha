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

enum State {
    INIT,
    WAIT,
};

enum Commande {
    NO,
    WRITE,
    PING
};


byte rowPins[ROWS] = {7, 2, 3, 5}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {6, 8, 4}; //connect to the column pinouts of the keypad

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

LiquidCrystal_I2C lcd(0x27,16,4);

enum Commande commande;
enum State state;

class Debug {
    public:
        Debug(){};
        void println(String str) {
            if (enable)
                Serial.println(str);
        }
        void print(String str) {
            if (enable)
                Serial.print(str);
        }
        bool enable;

};

Debug debug;

void setup() {
    Serial.begin(9600);
    lcd.init();
    lcd.backlight();
    lcd.setCursor(0, 0);
    lcd.print("Coucou");
    debug.enable = false;

    debug.println("<Startup>");

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
                        debug.println("Go to write mode");
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
                    debug.print(key);
                }
                break;
        }
    }
}

