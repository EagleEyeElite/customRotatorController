https://cdn.instructables.com/ORIG/FCN/YABW/IHNTEND4/FCNYABWIHNTEND4.pdf
https://create.arduino.cc/projecthub/ryanchan/how-to-use-the-l298n-motor-driver-b124c5

int motor1pin1 = 2;
int motor1pin2 = 3;
int speedPin1 = 9;

int motor2pin1 = 4;
int motor2pin2 = 5;
int speedPin2 = 10;

//void Move ( Dir direction , int distance );


enum Dir_m {
  CW,
  ACW
};

enum Dir {
   up,
   down,
   cw,
   acw
};


void setup() {
  // put your setup code here, to run once:
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(speedPin1, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);
  pinMode(speedPin2, OUTPUT);
}

void stopAll() {
  analogWrite(speedPin1, 0);
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, LOW);
  analogWrite(speedPin2, 0);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, LOW);
}

void move_p(Dir dir, unsigned int Speed) {
  switch(dir) {
    case up:
      setDir(0, CW, Speed);
      setDir(1, ACW, Speed);
      break;
    case down:
      setDir(0, ACW, Speed);
      setDir(1, CW, Speed);
      break;
    case cw:
      setDir(0, CW, Speed);
      setDir(1, CW, Speed);
      break;
    case acw:
      setDir(0, ACW, Speed);
      setDir(1, ACW, Speed);
      break;
  }
}


void setDir(unsigned int motor, Dir_m dir, unsigned int Speed) {
  
  unsigned int hm[] = {LOW, HIGH};
  if(dir == ACW) {
    hm[0] = HIGH;
    hm[1] = LOW;
  }

  switch (motor) {
    case 0:
      digitalWrite(motor1pin1, hm[0]);
      digitalWrite(motor1pin2, hm[1]);
      analogWrite(speedPin1, Speed);
      break;
    case 1:
      digitalWrite(motor2pin1, hm[0]);
      digitalWrite(motor2pin2, hm[1]);
      analogWrite(speedPin2, Speed); 
      break;
    default:
      // default statements
      break;
  }
}

void loop() {
  //setDir(0, CW, 50);
  //setDir(1, CW, 50);
  delay(5000);
  move_p(up, 100);
  delay(1000);
  stopAll();
  delay(500);
  move_p(down, 100);
  delay(1000);
  stopAll();
  delay(500);
  move_p(cw, 100);
  delay(1000);
  stopAll();
  delay(500);
  move_p(acw, 100);
  delay(1000);

  stopAll();
  while(1);
}
