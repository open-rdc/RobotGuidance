#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif
#include <ros.h>
#include <rosserial_arduino/Adc.h>

ros::NodeHandle nh;

rosserial_arduino::Adc adc_msg;
ros::Publisher p("adc", &adc_msg);

int analogPin1 = 0;
int analogPin2 = 1;

int analog1;
int analog2;

void setup()
{ 
  Serial.begin(9600);
  nh.initNode();
  nh.advertise(p);
}

long adc_timer;

void loop(){
  analog1 = analogRead(analogPin1);
  analog2 = analogRead(analogPin2);
  
  adc_msg.adc0 = analog1;
  adc_msg.adc1 = analog2;
    
  p.publish(&adc_msg);

  nh.spinOnce();
  delay(500);
}
