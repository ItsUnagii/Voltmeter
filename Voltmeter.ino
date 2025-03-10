// Define pins
#define POS_PIN A0   // Voltage divider output
#define NEG_PIN A1
#define MOSFET_PIN 3   // MOSFET gate control pin

// Resistor values
const float R1 = 9930;   // 10kΩ
const float R2 = 46590;   // 47kΩ
const float MOSFET = 2.20;
const float voltageDividerRatio = 1.0169823232323232323232323232323; // (R1 + (R2 + MOSFET)) / (R2 + MOSFET);

void setup() {
    Serial.begin(9600);
    pinMode(MOSFET_PIN, OUTPUT);
    digitalWrite(MOSFET_PIN, LOW); // Initially turn MOSFET off
}

void loop() {
    digitalWrite(MOSFET_PIN, HIGH); // Turn MOSFET ON
    delay(750); // Stabilization time

    pinMode(POS_PIN, OUTPUT);
    digitalWrite(POS_PIN, LOW); // Discharge floating state
    delay(1);
    pinMode(POS_PIN, INPUT);

    analogRead(POS_PIN);  // Dummy read
    int posValue = analogRead(POS_PIN);  // Actual read
    float posVoltage = (posValue * 5.0) / 1023.0;
    float batteryVoltage = posVoltage * voltageDividerRatio;

    digitalWrite(MOSFET_PIN, LOW); // Turn MOSFET OFF

    Serial.print("Battery Voltage: ");
    Serial.print(batteryVoltage, 3);
    Serial.println(" V");

    delay(1000);
}
