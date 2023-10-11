

//NOTE:-ADJUST/SET BY POTENTIOMETER OF SOUND SENSOR IF LESS NUMBER OF PATTERN OBSERVE

#include <FastLED.h>

int r=100;
int g=0;
int b=255;

#define LED_PIN     3            //CONNECT DATA PIN OF PIXEL WITH 5 NUMBER PIN OF ARDUINO
#define NUM_LEDS    120          //CHANGE THE VALUE IF YOU WANT TO USE DIFFRENT NUMBER OF LED IN YOUR STRIP,HERE IN MY STRIP NUMBER OF LED IS 60 SO I SET IT 60.

CRGB leds[NUM_LEDS];
CRGB led[NUM_LEDS];
int s=0;

void setup() {

  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  for (int i = NUM_LEDS/2; i >= 0; i--) 
  {
     leds[i] = CRGB (r,g,b);
     leds[NUM_LEDS-i] = CRGB (r,g,b);
     delay(40);
    FastLED.show();
  }
  Serial.begin(9600);
  pinMode(A0,INPUT);

}
void loop()
{
  s=analogRead(A0);
  s=s*2;
  Serial.println(s);
 // Serial.println(s);
 // delay(50);
  if((s>=600)&&(s<=700))
  {
    leds[(NUM_LEDS/2)-1]=CRGB (0, 0, 255);
    leds[NUM_LEDS/2]=CRGB (0, 0, 255);
  }
  else if((s>=701)&&(s<=800))
  {
    leds[(NUM_LEDS/2)-1]=CRGB (153, 153, 0);
    leds[NUM_LEDS/2]=CRGB (153, 153, 0);
  }
  else if((s>=801)&&(s<=900))
   {
     leds[(NUM_LEDS/2)-1]=CRGB (255, 50, 255);
    leds[NUM_LEDS/2]=CRGB (255, 50, 255);
   }
   else if((s>=901)&&(s<=1000))
  {
    leds[(NUM_LEDS/2)-1]=CRGB (10, 25, 217);
    leds[NUM_LEDS/2]=CRGB (10, 25, 217);
  }

    else if((s>=1001)&&(s<=1100))
   {
     leds[(NUM_LEDS/2)-1]=CRGB (50, 50, 150);
    leds[NUM_LEDS/2]=CRGB (50, 50, 150);
   }
   else if((s>=1101)&&(s<=1200))
   {
     leds[(NUM_LEDS/2)-1]=CRGB (230, 0, 10);
    leds[NUM_LEDS/2]=CRGB (230, 0, 10);
   }
    else
    {
      leds[(NUM_LEDS/2)-1] = CRGB ( r,s-100,b);
      leds[NUM_LEDS/2] = CRGB ( r,s-100,b);
    }
      for (int i = 0; i <= ((NUM_LEDS/2)-2); i++) 
    {
      leds[i] = leds[i+1];
      leds[NUM_LEDS-1-i] = leds[(NUM_LEDS)-i-2];
      
    }
  FastLED.show();
  delay(25);

}