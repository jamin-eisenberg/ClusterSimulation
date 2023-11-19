/* autogenerated by Processing revision 1292 on 2023-11-19 */
import processing.core.*;
import processing.data.*;
import processing.event.*;
import processing.opengl.*;

import processing.io.GPIO;

import java.util.HashMap;
import java.util.ArrayList;
import java.io.File;
import java.io.BufferedReader;
import java.io.PrintWriter;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.IOException;

public class ClusterSimulation extends PApplet {



final int TRIG_PIN = 23;
final int ECHO_PIN = 24;

public void setup() {
  /* size commented out by preprocessor */;

  GPIO.pinMode(TRIG_PIN, GPIO.OUTPUT);
  GPIO.pinMode(ECHO_PIN, GPIO.INPUT);
}

public void draw() {
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


  public void settings() { fullScreen(); }

  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "ClusterSimulation" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
