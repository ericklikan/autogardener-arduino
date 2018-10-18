#include <DHT.h>
#include <DHT_U.h>
#include <AsyncTimer.h>

#define DHTPIN 3
#define DHTTYPE DHT22

DHT dht22 = DHT(DHTPIN,DHTTYPE);

//Function prototypes
void parseCommand(char* cmd);

//DIGITAL PINS
const int pumpPin = 10;  
const int buttonPin = 5; //This will activate the pump for x seconds

//ANALOG PINS
const int soilMoisturePins[] = {3,4}; //analog pins for soil moisture
const int soilMoisturePinsSize = 1;

//global vars
float temp = 0;
float hum = 0;
int soilMoisture[] = {0,0};
AsyncTimer SMTimers[] = {
    AsyncTimer(5000),
    AsyncTimer(5000)  
};
bool pumpRunning = false;

AsyncTimer pumpTimer;

void setup() {
    Serial.begin(9600);
    pinMode(pumpPin,OUTPUT);
    pinMode(buttonPin,INPUT);
    for(int x = 0;x < 2;x++){
        pinMode(soilMoisturePins[x],INPUT);
    }
}

// Setup Serial Data port
const byte numChars = 5;
char receivedChars[numChars+1];
float fparam;
boolean newData = false;
boolean getNumData = false;
int args = 0; 
int lastCommand = -1;

void receiveData(){
    static byte index = 0;
    char endMarker = '\n'; //indicate end of char
    char rc; //received character in Serial.read()

    while(Serial.available() && newData == false){
        rc = Serial.read();
        // read up to 4 bytes or /n indicating new line
        if(rc != endMarker && index < numChars){
            receivedChars[index] = rc;
            index++;
        }
        else if(rc == endMarker){
            receivedChars[index] = '\0';
            index = 0;
            newData = true;
        }
    }
    
}

void showNewData() {
    if (newData == true) {
        if (args <= 0){
            args = atoi(receivedChars);
        }
        parseCommand(receivedChars);
        args--;

        newData = false;
    }
}

//Water plant
void  waterPlant(float seconds = 3.0){
    if(!pumpRunning){
        pumpTimer = AsyncTimer(seconds * 1000, stopWatering);
        pumpTimer.start();
        startWatering();
    }
}

void startWatering() {
    pumpRunning = true;
    analogWrite(pumpPin,255);  
}

void stopWatering() {
    pumpRunning = false;
    analogWrite(pumpPin,0);
}

//Get Soil Moisture
int getSoilMoisture(int pin = 0){
    unsigned int moistureValue = analogRead(soilMoisturePins[pin]);
    float dry = 1024.0;
    float wet = 0.0;
    float val = 0.0;
    val = 100.0 - ((moistureValue-wet) * 100.0 / (dry-wet));
    if (val > 100)
      return 100;
    else if (val < 0)
      return 0;
    else {
      return val;
    }
}
 
//Command Parser when serial comes in
void parseCommand(char* cmd){
    Serial.println("busy");
    if(!strcmp(cmd,"WATER")){
        if (args == 0){
            waterPlant();
        }
        else{
            lastCommand = 0;
            return;
        }
    }

    else if(!strcmp(cmd,"STWAT")){
        if (args == 0){
            startWatering();
        }
        else{
            lastCommand = 0;
            return;
        }
    }

    else if(!strcmp(cmd,"SPWAT")){
        if (args == 0){
            stopWatering();
        }
        else{
            lastCommand = 0;
            return;
        }
    }

    else if(atoi(cmd) != 0 && lastCommand == -1){
        return;
    }
    else if(args >= 0 && lastCommand != -1){
        switch(lastCommand){
            //waterPlant
            case 0:
                waterPlant(atof(cmd));
            break;
        }
    }
    else{
        //Error:NoCommand
        Serial.println("Error:CommandNotFound");
    }
    Serial.println("done");
 
    if(lastCommand == -1){
        args = 0;  
    }
}

void sendNewData() {
    float newTemp = dht22.readTemperature();
    if(temp != newTemp && !isnan(newTemp)){
        temp = newTemp;
        Serial.print("TEMP");
        Serial.println(temp);
    }

    float newHum = dht22.readHumidity();
    if(hum != newHum && !isnan(newHum)){
        hum = newHum;
        Serial.print("HUMI");
        Serial.println(hum);
        
    }
    
    for(int i = 0;i < soilMoisturePinsSize;i++) {
        int newSoilMoisture = getSoilMoisture(i);
        if(soilMoisture[i] != newSoilMoisture && !isnan(newSoilMoisture) && SMTimers[i].checkExpiration()) {
            soilMoisture[i] = newSoilMoisture;
            Serial.print("SM0");
            Serial.print(i);
            Serial.println(soilMoisture[i]);
            SMTimers[i].start();
        }  
    }
}


/**************/
/***  MAIN  ***/
/**************/
void loop() {
  receiveData();
  showNewData();
  sendNewData();
  if( digitalRead(5) ){
      waterPlant();  
  }
  pumpTimer.checkExpiration();
}
