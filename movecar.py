#sudo apt-get install python3-rpi.gpio
#sudo pip3 install gpiozero

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
#for continuous checking of distance
sc=0
sr=0
sl=0

try:
  while True:
    
    leftturn() #left
    time.sleep(0.5)
    sl=0
    d1=measure()
    print("d1= ",d1)

    if d1<=500.0:
      sl=1
      
    center() #middle
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
         
    
except KeyboardInterrupt:
    stop(1)
    GPIO.cleanup()
pwm.stop()
GPIO.cleanup()
