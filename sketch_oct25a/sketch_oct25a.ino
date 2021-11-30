

#include <Wire.h> 
#include <LiquidCrystal_I2C.h>


LiquidCrystal_I2C lcd(0x27,16,2);  // set the LCD address to 0x27 for a 16 chars and 2 line display
int state = 0;

void setup()
{
  Serial.begin(9600);
  lcd.init();                      // initialize the lcd 
  // Print a message to the LCD.
  lcd.backlight();
  lcd.setCursor(0,0); 
  lcd.print("waiting");
}

void loop()
{
  
  
  
  if (state == 0){ //  
    lcd.init(); 
    lcd.setCursor(0,0); 
    lcd.print("State : Dry");
  }else if(state ==1){//
    lcd.setCursor(0,0); 
    lcd.print("State : Water");
  }else if(state ==2){ //
    lcd.init(); 
    lcd.setCursor(0,0); 
    lcd.print("State : Ice");
  }

  state++;
  delay(3000);
  if(state==3) state = 0;

}
