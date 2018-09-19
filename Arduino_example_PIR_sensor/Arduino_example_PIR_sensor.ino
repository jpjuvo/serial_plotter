/*
 * PIR sensor
 */

 int inputPin = 2;    //digital out pin for the PIR
 int pirState = LOW;  //PIR state
 int val = 0;         //variable for reading the pin status

void setup() {
  pinMode(inputPin, INPUT); //PIR as input
  Serial.begin(9600);       //setup serial out and baud rate, Other configs are by default 8N1
}

void loop() {
  val = digitalRead(inputPin);    //read PIR pin
  if(val != pirState) {
    printSampleSerial(1.0f);
    pirState = !pirState;
  }else{
    printSampleSerial(0);
  }

  delay(200);
}

void printSampleSerial(float sample) {
  //For floating point numbers, serial println second parameter specifies the number of decimals
  Serial.println(sample, 4);
}
