int ledPin2 = 12;
int ledPin = 13;  // The LED is connected to pin 13 (built-in LED on most Arduinos)



int joystick_1_Y = A0; // Joystick's X-axis is connected to analog pin A0
int joystick_1_X = A1; // Joystick's Y-axis is connected to analog pin A1

int joystick_2_Y = A3; // Joystick's X-axis is connected to analog pin A0
int joystick_2_X = A2;

int joystick_1_value1 = 0;   // Variable to store the X-axis analog value
int joystick_1_value2 = 0;   // Variable to store the Y-axis analog value

int joystick_2_value1 = 0;   // Variable to store the X-axis analog value
int joystick_2_value2 = 0;   // Variable to store the Y-axis analog value

void setup() {
  pinMode(ledPin, OUTPUT);  // Set pin 13 (LED) as an output pin
  pinMode(ledPin2, OUTPUT); 
  
  Serial.begin(9600);       // Start the serial communication at 9600 baud rate
}

// the setup function runs once when you press reset or power the board


int treatValue(int data) {
  return (data * 9 / 1024) + 48;
}

void loop() {
  // reads the value of the joystick's X-axis
  joystick_1_value1 = analogRead(joystick_1_X);  
  delay(100);  // Small delay to ensure the readings don't interfere with each other
  joystick_1_value2 = analogRead(joystick_1_Y);  
  
  joystick_2_value1 = analogRead(joystick_2_X);
  delay(100);
  joystick_2_value2 = analogRead(joystick_2_Y);

if (joystick_1_value1 > 512) digitalWrite(ledPin, HIGH);
if (joystick_1_value1 < 512) digitalWrite(ledPin, LOW);
if (joystick_2_value1 > 520) digitalWrite(ledPin2, HIGH);
if (joystick_2_value1 < 520) digitalWrite(ledPin2, LOW);


  delay(100);
}
  

  // Serial output to print joystick values in a specific format
 



