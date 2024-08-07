/*Heather Wimberley - EEE4113F Group 14

The following was developed using the HX711 Arduino library by Bogden Necula. The repo is found at:
https://github.com/bogde/HX711

The code was developed following and the modifying the tutorial found at:
https://randomnerdtutorials.com/esp32-load-cell-hx711/
created by Sara Santos
*/

#include <Arduino.h>
#include "HX711.h"
#include "soc/rtc.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 16; //HX711 data pin
const int LOADCELL_SCK_PIN = 4;

//TARE button wiring
const int TARE_PIN = 14;

//sampling frequency in Hz
const int freq = 10;

//integer t is used to create timing without delaying system
int t;

//flag if the tare button has been pushed or not
boolean fTare = false;

//create the HX711 object from the library
HX711 scale;

void setup() {
  Serial2.begin(115200,SERIAL_8N1,18,17); //set up the UART line to the Raspberry Pi with RX = pin 18 and TX = pin 17
  Serial.begin(115200); //set up the USB serial for testing purposes
  pinMode(TARE_PIN,INPUT_PULLUP); //setup the tare button as an internal pullup input. Note that this button is active low

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN); //connect the scale object to the pins
            
  scale.set_scale(-483); //set the calibration factor. This was predetermined using an object of known weight and 
                          //following the steps in the HX711 library README
  scale.tare();               // reset the scale to 0

  t = millis();         //set the current t value as the current milliseconds
}

void loop() {
  if (millis() >= (1/freq*1000+t)){ //once the amount of time determined by the frequency has passed, read the scale
    //scale.power_up(); //uncomment if the frequency is less than 5Hz. This helps to wake up the scale from power down mode

    //if the tare flag is true, reset the offset of the scale to produce readings of 0
    if (fTare == true){
      double sum = scale.read_average(5);
      scale.set_offset(sum);
      fTare = false;
    }


    //Serial2.println(scale.get_units()); //send the data to the Raspberry Pi
    Serial.println(scale.get_units()); //send the data to the USB serial port
    //scale.power_down();  //uncomment if the frequency is less than 5Hz
    t = millis();  //set the new time
    
  }

  //the tare flag acts as a latch so once it has been raised, it doesnt reset until the scale has been tared
  //the following raises the flag if the button is pressed and the flag is currently false
  if (digitalRead(TARE_PIN)==LOW&&!fTare)
  {
    fTare = true;
  }
}

