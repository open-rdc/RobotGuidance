/*
position  analog_value  degree

center        246         308
right         509       17(377)
left            0         222

up            511           0
down          846           0

left-right  263analog_value = 69degree        1analog_value = 0.26235degree
up-down     335analog_value = 90degree        1analog_value = 0.26866degree
*/

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

int analogPin1 = 1;
int analogPin2 = 0;

int analog1;
int analog2;
int analog1_zero = 246;
int analog2_zero = 679;

float analog2degree1 = 0.26235;
float analog2degree2 = 0.26866;

int degree1;
int degree2;

void setup()
{ 
  nh.initNode();
  nh.advertise(p);
}

long adc_timer;

void loop(){
  analog1 = analogRead(analogPin1);
  analog2 = analogRead(analogPin2);

  degree1 = int((analog1 - analog1_zero) * analog2degree1);
  degree2 = int((analog2 - analog2_zero) * analog2degree2);

  if(degree1 < 0){
    adc_msg.adc0 = abs(degree1);
    adc_msg.adc1 = 0;
  }
  else{
    adc_msg.adc0 = 0;
    adc_msg.adc1 = degree1;
  }
  if(degree2 < 0){
    adc_msg.adc2 = abs(degree2);
    adc_msg.adc3 = 0;
  }
  else{
    adc_msg.adc2 = 0;
    adc_msg.adc3 = degree2;
  }
    
  p.publish(&adc_msg);

  nh.spinOnce();
  delay(200);
}
