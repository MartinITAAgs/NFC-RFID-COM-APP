#include <MFRC522v2.h>
#include <MFRC522DriverSPI.h>
#include <MFRC522DriverPinSimple.h>
//este codigo se emplea en un ESP32-S3 mini, librería MFRC522v2

MFRC522DriverPinSimple ss_pin(10);
MFRC522DriverSPI driver{ss_pin};
MFRC522 mfrc522{driver};

void setup() {
  Serial.begin(115200);
  SPI.begin(12, 13, 11, 10);
  mfrc522.PCD_Init();
}

void loop() {
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String uid = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      if (mfrc522.uid.uidByte[i] < 0x10) uid += "0";
      uid += String(mfrc522.uid.uidByte[i], HEX);
    }
    uid.toUpperCase();

    // Enviamos SOLO el UID por serial para que la App de PC lo procese
    Serial.println(uid);

    mfrc522.PICC_HaltA();
    delay(1000); 
  }
}