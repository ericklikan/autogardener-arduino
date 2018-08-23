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
    if(!strcmp(cmd,"INFO")){
        //return device info
        Serial.println("AutoGardenerProject");
    }
    else if(!strcmp(cmd,"WATER")){
        if (args == 0){
            waterPlant();
        }
        else{
            lastCommand = 0;
        }
    }
    else if(!strcmp(cmd,"COLSM")){
        if(args == 0){
            collectSoilMoisture();
        }
        else{
            lastCommand = 1;  
        }
    }
    else if(!strcmp(cmd,"COLLT")){
        float temp = dht22.readTemperature();
        Serial.println(temp); //Relative Temperature in degrees Celsius
    }
    else if(!strcmp(cmd,"COLLH")){
        float hum = dht22.readHumidity();
        Serial.println(hum); //Relative Humidity in percentage
    }
    else if(atoi(cmd) != 0 && lastCommand == -1){
        Serial.println("done");
        return;
    }
    else if(args > 0 && lastCommand != -1){
        switch(lastCommand){
            //waterPlant
            case 0:
                waterPlant(atof(cmd));
            break;

            //collectSoilMoisture
            case 1:
                collectSoilMoisture(atoi(cmd));
            break;
            
            default:
                Serial.println("Error:WrongParam");
            break;
        }
        //rewrite args as 1 because it doesnt take more than 1 param
        lastCommand = -1;
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

