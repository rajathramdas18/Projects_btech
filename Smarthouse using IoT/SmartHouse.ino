#include<SoftwareSerial.h>
int motor1 =3;//connected to the motor
int motor2 =6;
int acled =12;//led to indicate the circuit to the AC
int heaterled= 7;//led to ndicate the circuit to the heater
int lights =10;//controls for the lights of the room
void setup() {
  // put your setup code here, to run once:
 Serial.begin(9600);
pinMode(motor1,OUTPUT);
pinMode(motor2,OUTPUT);
pinMode(acled,OUTPUT);
pinMode(heaterled,OUTPUT);

}

void loop() {
  //digitalWrite(acled,HIGH);
  // put your main code here, to run repeatedly:
if(Serial.available()>0)
{
  char data=Serial.read();
  if(data=='a') digitalWrite(acled,HIGH);//for the ac
  if(data=='b') digitalWrite(heaterled,HIGH);//for the heater
  if(data=='c') //for the motor of garage
  {
    digitalWrite(motor1,HIGH);
    digitalWrite(motor2,LOW);
    delay(1000);
    digitalWrite(motor1,LOW);
    digitalWrite(motor2,LOW);
    delay(3000);
    digitalWrite(motor1,LOW);
    digitalWrite(motor2,HIGH);
    
    }
  if(data=='d') digitalWrite(lights,HIGH);
}
delay(50);
}
