#include<Servo.h>
Servo myservo;
const int Pin=5;//soil humidity sensor
const int limit=500;

int pos,k=0;
int pump_relay = 12;
const int capteur_D = 4;//rain water sensor

void setup()
{
      pinMode(capteur_D, INPUT);//rain water
      myservo.attach(2);//servo motor
      myservo.write(0);
      pinMode(pump_relay, OUTPUT);
      Serial.begin(9600);
}

void loop()
{
   int value;
   digitalWrite(12,HIGH);//pump is off initially
   delay(1000);
   myservo.write(0);
  //Rain water 
 
if(digitalRead(capteur_D) == LOW) //rain water sensor value reading
  {
    Serial.println("Digital value : wet"); //raining
    //For Servo Motor
     if(k==0){
   Serial.println("Servo started.");
  for(pos=0;pos<=180;pos++)//tank lid is opening
  {
    myservo.write(pos);
   delay(100);

   }
   k=1;
  }
  }
   
else//not raining
  {
    Serial.println("Digital value : dry");//not raining
    delay(25);
    if(k==1)//if lid is open
    {
      for(pos=180;pos>=0;pos--)//tank lid is closing
      {
        myservo.write(pos);
        delay(100);
      } 
      delay(25);
   Serial.println("Servo stopped.");
    }
    k=0;
    delay(10); 
  }
 //Soil Moisture 
   value=digitalRead(Pin);
   Serial.print("Soil Moisture: ");
   Serial.println(value);
  if (value==0)//if soil moisture is more
  {

      digitalWrite(12,HIGH);//relay module switches off pump
      Serial.println("Pump stopped");
      delay(100);
      myservo.write(0);
  }
  else//if soil moisture is less
  {
    digitalWrite(12,LOW);//relay module switches on pump
    Serial.println("Pump started");
    delay(5000);
    myservo.write(0);
  }
    delay(10000); 
  }
