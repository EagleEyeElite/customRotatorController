/*
 * HBridge design
 * 
 * cicruit design: http://www.learningaboutelectronics.com/Articles/H-bridge-circuit-with-transistors.php
 */

// pinout Arduino (all PWM)
#define H1_1 3
#define H1_2 5
#define H2_1 6
#define H2_2 9

// bridge[slectBridge][selectPin]
int bridge[2][2] = {{H1_1, H1_2}, {H2_1, H2_2}};

void setup() {
  // If not set as Output, the NPN Transistor smokes up,
  // figgured that out by try and error
  pinMode(bridge[0][0], OUTPUT);
  pinMode(bridge[0][1], OUTPUT);
  pinMode(bridge[1][0], OUTPUT);
  pinMode(bridge[1][1], OUTPUT);

  digitalWrite(bridge[0][0], LOW);
  digitalWrite(bridge[0][1], LOW);
  digitalWrite(bridge[1][0], LOW);
  digitalWrite(bridge[1][1], LOW);
}

// select brigde, select dir
void dir(int b, bool direction) {
  // both may never on at the same time
  digitalWrite(bridge[b][0], LOW);
  digitalWrite(bridge[b][1], LOW);

  delay(100);
  if (direction)
    digitalWrite(bridge[b][0], HIGH);
  else
    digitalWrite(bridge[b][1], HIGH);
}

void turnOff() {
  digitalWrite(bridge[0][0], LOW);
  digitalWrite(bridge[0][1], LOW);
  digitalWrite(bridge[1][0], LOW);
  digitalWrite(bridge[1][1], LOW);
}

// the loop function runs over and over again forever
void loop() {
  dir(0, true);
  dir(1, true);
  delay(4000);
  dir(0, false);
  dir(1, false);
  delay(4000);
  turnOff();
  while(1);
}
