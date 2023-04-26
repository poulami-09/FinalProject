"""Main script to run the object detection routine."""
import argparse
import sys
import time

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

import RPi.GPIO as GPIO
import time
import gpiozero


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#MOTOR A
#ENA=25
IN1=16
IN2=19

#GPIO.setup(ENA,GPIO.OUT)
#ena_pwm=GPIO.PWM(ENA,100)
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)

#MOTOR B
#ENB=23
IN3=20
IN4=26

#GPIO.setup(ENB,GPIO.OUT)
#enb_pwm=GPIO.PWM(ENB,100)
GPIO.setup(IN3,GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)

GPIO.output(IN1,GPIO.LOW)
GPIO.output(IN2,GPIO.LOW)
GPIO.output(IN3,GPIO.LOW)
GPIO.output(IN4,GPIO.LOW)

#servo motor
GPIO.setup(5, GPIO.OUT)
pwm=GPIO.PWM(5, 50)
pwm.start(0)

#ULTRASONIC SENSOR
ECHO=7
TRIG=22
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(TRIG,GPIO.OUT)

#CAR MOVEMENTS
def forward():
    print("Moving Forward")
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.HIGH)
    time.sleep(10)


def left():
    print("Turning Left")
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.HIGH)
    time.sleep(10)

def right():
    print("Turning Right")
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(10)

def stop(tme):
    print("Stop")
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(tme)

def leftturn():
    print("left turn of servo")
    pwm.ChangeDutyCycle(10) #  left deg position
    time.sleep(2)
    
def rightturn():
    print("Right turn of servo by 45")
    pwm.ChangeDutyCycle(2.5) # right +45 deg position
    time.sleep(2)
    
def center():
    print("Servo returns to 0")
    pwm.ChangeDutyCycle(7.5) #  0 deg position
    time.sleep(2)
#measuring distance from ultrasonic sensor
def measure():
 GPIO.output(TRIG,1)
 time.sleep(0.0001)
 GPIO.output(TRIG,0)
 print("Ultrasonic sensor started")
  
 print("waiting for sensor to settle")
 time.sleep(0.2)
 GPIO.output(TRIG,True)
 time.sleep(0.00001)
 GPIO.output(TRIG,False)
 while GPIO.input(ECHO)==0:
        #print("Echo start")
    pulse_start=time.time()
 while GPIO.input(ECHO)==1:
    #print("Echo end")
    pulse_end=time.time()
 pulse_duration=pulse_end-pulse_start
 d=pulse_duration*17150
 d=round(d,2)
 print("distance:",d,"cm")
 time.sleep(2)    
 return d

def movement():
    sc=0
    sr=0
    sl=0

    try:
      while True:
    
       leftturn() #left turn of uv sensor
       time.sleep(0.5)
       sl=0
       d1=measure()
       print("d1= ",d1)

       if d1<=500.0:
          sl=1
      
       center() #middle turn of uv sensor
       time.sleep(0.5)
       sc=0
       d2=measure()
       print("d2= ",d2)
    
       if d2<=500.0:
          sc=1
    
       rightturn() #right
       time.sleep(0.5)
       sr=0
       d3=measure()
       print("d3= ",d3)
             
       if d3<=500.0:
          sr=1
      
       join=str(sl)+str(sc)+str(sr)
       print(join)
       time.sleep(5)
  #8 combinations are possible
       if join=="000" or join=="101": #Go forward
          forward()
          print("Car moves forward")
       elif join=="001" or join=="011":#turn left
         
          print("car moving left")
          stop(1)
          left()
          time.sleep(1)
          stop(1)
          forward()
       elif join=="100" or join=="110":#turn right
          print("Car moving right")
          stop(1)
          right()
          time.sleep(1)
          stop(1)
          forward()
       elif join=="111":
          print("Uturn and reverse")
          stop(1)

def run(model: str, camera_id: int, width: int, height: int, num_threads: int,
    enable_edgetpu: bool) -> None:
 """Continuously run inference on images acquired from the camera.
 Args:
  model: Name of the TFLite object detection model.
  camera_id: The camera id to be passed to OpenCV.
  width: The width of the frame captured from the camera.
  height: The height of the frame captured from the camera.
  num_threads: The number of CPU threads to run the model.
  enable_edgetpu: True/False whether the model is a EdgeTPU model.
 """

# Variables to calculate FPS
 counter, fps = 0, 0
 start_time = time.time()

# Start capturing video input from the camera
 cap = cv2.VideoCapture(camera_id)
 cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
 cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Visualization parameters
 row_size = 20  # pixels
 left_margin = 24  # pixels
 text_color = (0, 0, 255)  # red
 font_size = 1
 font_thickness = 1
 fps_avg_frame_count = 10

# Initialize the object detection model
 base_options = core.BaseOptions(
   file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
 detection_options = processor.DetectionOptions(
   max_results=3, score_threshold=0.3)
 options = vision.ObjectDetectorOptions(
   base_options=base_options, detection_options=detection_options)
 detector = vision.ObjectDetector.create_from_options(options)

# Continuously capture images from the camera and run inference
 while cap.isOpened():
  success, image = cap.read()
  if not success:
    sys.exit(
      'ERROR: Unable to read from webcam. Please verify your webcam settings.'
    )

  counter += 1
  image = cv2.flip(image, 1)

# Convert the image from BGR to RGB as required by the TFLite model.
  rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Create a TensorImage object from the RGB image.
  input_tensor = vision.TensorImage.create_from_array(rgb_image)

# Run object detection estimation using the model.
  detection_result = detector.detect(input_tensor)

# Draw keypoints and edges on input image
  image = utils.visualize(image, detection_result)

# Calculate the FPS
  if counter % fps_avg_frame_count == 0:
    end_time = time.time()
    fps = fps_avg_frame_count / (end_time - start_time)
    start_time = time.time()

# Show the FPS
  fps_text = 'FPS = {:.1f}'.format(fps)
  text_location = (left_margin, row_size)
  cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
            font_size, text_color, font_thickness)
  print(fps_text)

# Stop the program if the ESC key is pressed.
  if cv2.waitKey(1) == 27:
     break
  cv2.imshow('object_detector', image)

  cap.release()
  cv2.destroyAllWindows()


def main():
 movement()
 parser = argparse.ArgumentParser(
   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
 parser.add_argument(
   '--model',
   help='Path of the object detection model.',
   required=False,
   default='efficientdet_lite0.tflite')
 parser.add_argument(
   '--cameraId', help='Id of camera.', required=False, type=int, default=0)
 parser.add_argument(
   '--frameWidth',
   help='Width of frame to capture from camera.',
   required=False,
   type=int,
   default=640)
 parser.add_argument(
   '--frameHeight',
   help='Height of frame to capture from camera.',
   required=False,
   type=int,
   default=480)
 parser.add_argument(
   '--numThreads',
   help='Number of CPU threads to run the model.',
   required=False,
   type=int,
   default=4)
 parser.add_argument(
   '--enableEdgeTPU',
   help='Whether to run the model on EdgeTPU.',
   action='store_true',
   required=False,
   default=False)
 args = parser.parse_args()

 run(args.model, int(args.cameraId), args.frameWidth, args.frameHeight,
   int(args.numThreads), bool(args.enableEdgeTPU))


if __name__ == '__main__':
  main()
