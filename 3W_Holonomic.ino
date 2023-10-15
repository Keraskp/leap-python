//3 motor Holonomic Control  06/08/2022
int ch1,ch2,ch3,ch4,ch5,dirch,acrl;
int rotate,fbwCh;
    
void setup() 
      {

      // For Motor 1
        pinMode(10,OUTPUT);//Direction
        pinMode(11,OUTPUT);//Acceleration
      // For Motor 2
        pinMode(8,OUTPUT);//Direction
        pinMode(9,OUTPUT);//Acceleration
      // For Motor 3
        pinMode(6,OUTPUT);//Direction
        pinMode(7,OUTPUT);//Acceleration


      //Receive PWM Sugnal from RF receiever
      
      pinMode(31,INPUT);// Cw CCW rotation channel 1 right Horizontal swich
      pinMode(32,INPUT);// REserve channel 2 left Horizontal swich
      pinMode(33,INPUT);// for Speed value/ acceleraton channel 3   left Verticle switch    
      pinMode(34,INPUT);// for Forward - Backward Signal that attached to channel 4 right Verticle switch
      pinMode(35,INPUT);// Channel 5 Direction selection/ motor selection
      Serial.begin(9600);

      }


void loop() 
      {

     

      ch1=pulseIn(31,HIGH);// Rotate Choice Choice
      rotate=map(ch1,990,1934,0,255);
      
     // ch2=pulseIn(32,HIGH);// Direction Choice
      //fbwCh=map(ch2,1191,1783,0,255);
      
      ch3=pulseIn(33,HIGH);// Acceleration Choice
      acrl=map(ch3,998,1982,0,255);

      ch4=pulseIn(34,HIGH);// Direction Choice
      fbwCh=map(ch4,1033,1998,0,255);

      ch5=pulseIn(35,HIGH);// Direction Choice
      dirch=map(ch5,985,1970,0,255);
    /*  
      Serial.print("\nRaw Ch1 val=");
      Serial.print(ch1);
      Serial.print(" map =");
      Serial.print(rotate);
      Serial.print("Raw Ch3 val=");
      Serial.print(ch3);
      Serial.print(" map =");
      Serial.print(acrl);
      Serial.print("Raw Ch4 val=");
      Serial.print(ch4);
      Serial.print(" map =");
      Serial.print(fbwCh);
      Serial.print("Raw Ch5 val=");
      Serial.print(ch5);
      Serial.print(" map =");
      Serial.print(dirch);
*/

     
      if(acrl>255 or acrl<0) 
      acrl=0;
     
     

      if(rotate>200)
      {
      rotate_CW(acrl);
      }
      else if(rotate<80)
      {
      rotate_ACW(acrl);
      }
      else
      {
       rotate_CW(0);
       rotate_ACW(0); 
      }

//Move motor 1
      if(dirch<100 and fbwCh>200 )
      {
       move_mfbw(0,HIGH,acrl, LOW,acrl, HIGH);
      }
      else if(dirch<100 and fbwCh<80)
      {
        move_mfbw(0,HIGH,acrl, HIGH,acrl, LOW);
      }
//Move motor 2
      if((dirch>110 and dirch<150) and fbwCh>200 )
      {
       move_mfbw(acrl,HIGH,0, LOW,acrl, LOW);
      }
      else if((dirch>110 and dirch<150) and fbwCh<80)
      {
        move_mfbw(acrl,LOW,0, HIGH,acrl, HIGH);
      }
       
//Move motor 3
      if(dirch>200 and fbwCh<80 )
      {
       move_mfbw(acrl,HIGH,acrl, LOW,0, LOW);
      }
      else if(dirch>200 and fbwCh>200)
      {
        move_mfbw(acrl,LOW,acrl, HIGH,0, HIGH);
      } 

 } //complete loop

void move_mfbw(int m1a, bool m1d,int m2a, bool m2d,int m3a, bool m3d)
{
       //Motor 1
       digitalWrite(6,m1d);
       analogWrite(7,m1a);
       //Motor 2       
       digitalWrite(8,m2d);
       analogWrite(9,m2a);
       //Motor 3
       digitalWrite(10,m3d);
       analogWrite(11,m3a);     
}

void rotate_CW(int acrl)
{
       digitalWrite(6,LOW);
       analogWrite(7,acrl);
       digitalWrite(8,LOW);
       analogWrite(9,acrl);
       digitalWrite(10,LOW);
       analogWrite(11,acrl);     
}

void rotate_ACW(int acrl)
{
       digitalWrite(6,HIGH);
       analogWrite(7,acrl);
       digitalWrite(8,HIGH);
       analogWrite(9,acrl);
       digitalWrite(10,HIGH);
       analogWrite(11,acrl);     
}
