#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 3
#define DHTTYPE DHT22

DHT dht22 = DHT(DHTPIN,DHTTYPE);

//Function prototypes
void parseCommand(char* cmd);

//not yet in use

//DIGITAL PINS
const int pumpPin = 10;  
const int buttonPin = 5; //This will activate the pump for x seconds

//ANALOG PINS
const int soilMoisturePins[] = {3,4}; //analog pins for soil moisture


void setup() {
    Serial.begin(9600);
    pinMode(pumpPin,OUTPUT);
    pinMode(buttonPin,INPUT);
    for(int x = 0;x < 2;x++){
        pinMode(soilMoisturePins[x],INPUT);
    }
}

// Setup Serial Data port
const byte numChars = 32;
char receivedChars[numChars];
boolean newData = false;
boolean getNumData = false;
char lastCommand[32] = "";

void receiveData(){
    static byte index = 0;
    char endMarker = '\n';
    char rc;

    while(Serial.available() && newData == false){
        rc = Serial.read();
        if(rc != endMarker){
            receivedChars[index] = rc;
            index++;
            if(index >= numChars){
              index = numChars - 1;
            }
        }
        else{
            receivedChars[index] = '\0';
            index = 0;
            newData = true;
        }
    }
}

void showNewData() {
    if (newData == true) {
        parseCommand(receivedChars);
        newData = false;
    }
}


//Water plant
void  waterPlant(float seconds = 3.0){
    analogWrite(pumpPin,255);  
    int t = int(seconds) * 1000;
    delay(t);
    analogWrite(pumpPin,0);
    
}

//Get Soil Moisture
void collectSoilMoisture(int pin = 0){
    int moistureValue = analogRead(soilMoisturePins[pin]);
    Serial.println(moistureValue);
}

//Command Parser when serial comes in
void parseCommand(char* cmd){
    Serial.println("busy");
    if(!strcmp(cmd,"info")){
        //return device info
        Serial.println("AutoGardenerProject");
    }
    else if(!strcmp(cmd,"waterPlant")){
        //set global flag to collect number  
        waterPlant();
    }
    else if(!strcmp(cmd,"collectSoilMoisture")){
        //set global flag to collect number  
        collectSoilMoisture();
    }
    else if(!strcmp(cmd,"collectTemp")){
        float temp = dht22.readTemperature();
        Serial.println(temp); //Relative Temperature in degrees Celsius
    }
    else if(!strcmp(cmd,"collectHum")){
        float hum = dht22.readHumidity();
        Serial.println(hum); //Relative Humidity in percentage
    }
    else{
        //Error:NoCommand
        Serial.println("Error:CommandNotFound");
    }
    Serial.println("done");
}



/**************/
/***  MAIN  ***/
/**************/
void loop() {
  receiveData();
  showNewData();
  if( digitalRead(5) ){
      waterPlant();  
  }
}

