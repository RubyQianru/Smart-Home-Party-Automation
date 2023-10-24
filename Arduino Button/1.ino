const int buttonPin = 2; // Define the pin connected to the push button
int buttonState = 0;    // Variable to store the button state

void setup() {    
  Serial.begin(9600);
  pinMode(buttonPin, INPUT); // Set the button pin as an input
}

void loop() {
  buttonState = digitalRead(buttonPin); // Read the button state

  if (buttonState == HIGH) { // If button is pressed
    // Send a signal to your computer here
    Serial.println("OpenURL");
  }
  delay(1000);
}
