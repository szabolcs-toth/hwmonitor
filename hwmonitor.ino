#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4); // I2C address 0x27, 16 column and 2 rows

long int rewrite = 0;                         //this will hold our last rewritten time from millis() function
const short firstRow = 0;                    //some constants that define where the rows will be
const short secondRow = 1;
const short thirdRow = 2;
const short fourthRow = 3;

const short label = 0;
const short percentage = 5;
const short percSign = 10;
const short total = 13;

void setup(void) {
  lcd.init(); // initialize the lcd
  lcd.backlight();
  Serial.begin(9600);                         //open serial interface with baud of 9600 (have to be the same as in python script)
}

String serialReceive;                         //some Strings, that will contain values got from Serial buffer. First one will contain the entire data string, others will contain only substrings that belongs to them
String CPUstat;
String RAMstat;
String HDDspace;
String SSDspace;
String CPUcores;
String RAMtotal;

void loop(void) {
  if(Serial.available() > 0) {                //if any data is available in serial buffer
    serialReceive = Serial.readString();      //read it as string and put into serialReceive variable
  }

  CPUstat = serialReceive.substring(0, 5);    //split the long ass received string to substrings. Values i used are those that i defined (5 characters/information) if not stated else
  RAMstat = serialReceive.substring(5, 10);
  SSDspace = serialReceive.substring(10, 15);
  HDDspace = serialReceive.substring(15, 20);
  CPUcores = serialReceive.substring(20, 24);
  RAMtotal = serialReceive.substring(24, 30);
    
  if (millis()-rewrite > 100) {               //lcd handler statement.. 
    
    drawLCD();                   
  }
  
  delay(10);                                  //wait for 10ms, as lcd needs some time to get refreshed
}

void drawLCD(void) {
  lcd.clear();  
  
  lcd.setCursor(label, firstRow);              //set printing position to edge of screen, first row
  lcd.print("CPU :");                         //print legend text
  lcd.setCursor(percentage, firstRow);             //set printing position to a bit further
  lcd.print(CPUstat);                        //print the value received and split from the Serial
  lcd.setCursor(percSign, firstRow);             //set printing position to a bit further
  lcd.print(" %");                           //print percent sign
  lcd.setCursor(total, firstRow);             //set printing position to a bit further
  lcd.print(CPUcores);                       //print additional information

  lcd.setCursor(label, secondRow);             //and basically the same for everything repeats..
  lcd.print("RAM :");
  lcd.setCursor(percentage, secondRow);
  lcd.print(RAMstat);
  lcd.setCursor(percSign, secondRow);
  lcd.print(" %");
  lcd.setCursor(total, secondRow);
  lcd.print(RAMtotal);

  lcd.setCursor(label, thirdRow);
  lcd.print("HDD1:");
  lcd.setCursor(percentage, thirdRow);
  lcd.print(SSDspace);
  lcd.setCursor(percSign, thirdRow);
  lcd.print(" %");
  lcd.setCursor(total, thirdRow);
  lcd.print("(C:/)");

  lcd.setCursor(label, fourthRow);
  lcd.print("HDD2:");
  lcd.setCursor(percentage, fourthRow);
  lcd.print(HDDspace);
  lcd.setCursor(percSign, fourthRow);
  lcd.print(" %");
  lcd.setCursor(total, fourthRow);
  lcd.print("(D:/)");

  delay(1000);                 // display the above for two seconds                // display the above for two seconds
}
