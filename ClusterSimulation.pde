import processing.io.*;

final int TRIG_PIN = 23;
final int ECHO_PIN = 24;

void setup() {
  fullScreen();

  GPIO.pinMode(TRIG_PIN, GPIO.OUTPUT);
  GPIO.pinMode(ECHO_PIN, GPIO.INPUT);
}

void draw() {
  background(255, 255, 0);

  //GPIO.digitalWrite(TRIG_PIN, GPIO.LOW);
  //busyWaitMicros(2);
  //GPIO.digitalWrite(TRIG_PIN, GPIO.HIGH);
  //busyWaitMicros(10);
  //GPIO.digitalWrite(TRIG_PIN, GPIO.LOW);

  //long startTime = System.nanoTime();

  //GPIO.waitFor(ECHO_PIN, GPIO.FALLING, 1000);

  //long endTime = System.nanoTime();

  //int distance = (int) ((endTime - startTime) / 5882.35294118); // mm
  
  //fill(0);
  //textSize(100);
  //text("Distance: " + distance, width / 2, height / 2);
}


//void busyWaitMicros(long micros) {
//  long waitUntil = System.nanoTime() + (micros * 1_000);
//  while (waitUntil > System.nanoTime()) {
//  }
//}
