import RPi.GPIO as GPIO
import time
from gpiozero import servo

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
//MOTOR A
ENA=25
IN1=19
IN2=16

GPIO.setup(ENA,GPIO.OUT)
ena_pwm=GPIO.PWM(ENA,100)
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)

//MOTOR B

ENB=23
IN3=26
IN4=20

GPIO.setup(ENB,GPIO.OUT)
enb_pwm=GPIO.PWM(EBA,100)
GPIO.setup(IN3,GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)
//servo motor
GRIO.setup(SERVO_TRIG,GPIO.OUT)
servo=Servo(SERVO_TRIG)

//ULTRASONIC SENSOR
ECHO=7
TRIG=22
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(TRIG,GPIO.OUT)

//CAR MOVEMENTS
def forward():
    ena_pwm.start(100)
    enb_pwm.start(100)
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)

def reverse():
    ena_pwm.start(100)
    enb_pwm.start(100)
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)

def left():
    ena_pwm.start(100)
    enb_pwm.start(100)
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)

def right():
    ena_pwm.start(100)
    enb_pwm.start(100)
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)

def stop():
    ena_pwm.start(0)
    enb_pwm.start(0)
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.LOW)
  //  time.sleep(tme)
  
def uturn():
    ena_pwm.start(0)
    enb_pwm.start(0)
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)
    time.sleep(tme)


//measuring distance from ultrasonic sensor
def measure():
  GPIO.output(TRIG,1)
  time.sleep(0.0001)
  GPIO.output(TRIG,0)
  
  while GPIO.input(ECHO)==0:
    pass
  start=time.time()
  while GPIO.input(ECHO)==1:
    pass
  stop=time.time()
  d=(stop-start)*1700

 //for continuous checking of distance
sc=0
sr=0
sl=0
dist=0
try:
  while True:
    
    servo.max() //left
    time.sleep(0.5)
    sl=0
    
    dist=measure()
    if dist<=20.0:
      sl=1
      
    servo.max() //middle
    time.sleep(0.5)
    sc=0
    
    dist=measure()
    if dist<=20.0:
      sc=1
    
    servo.max() //right
    time.sleep(0.5)
    sr=0
    
    dist=measure()
    if dist<=20.0:
      sl=1
      
   join=str(sl)+str(sc)+str(sr)
  print(join)
  
  //8 combinations are possible
  if join=="000" or join=="101": //Go forward
    forward()
    print("Straight")
  elif join=="001" or join=="011"://turn left
    print("left")
    stopm(1)
    reverse()
    time.sleep(1)
    stopm(1)
    left()
    time.sleep(1)
    stopm(1)
    forward()
  elif join=="100" or join=="110"://turn right
    print("right")
    stopm(1)
    reverse()
    time.sleep(1)
    stopm(1)
    right()
    time.sleep(1)
    stopm(1)
    forward()
 elif join="111":
    stopm(1)
    reverse()
    time.sleep(1)
    stopm(1)
    uturn()
    time.sleep(3.5)
    forward()
    
except KeyboardInterrupt:
    stopm(1)
    GPIO.cleanup()
    
GPIO.cleanup()
    
