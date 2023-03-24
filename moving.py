import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#MOTOR A
ENA=25
IN1=19
IN2=16

GPIO.setup(ENA,GPIO.OUT)
ena_pwm=GPIO.PWM(ENA,100)
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)

#MOTOR B
ENB=23
IN3=26
IN4=20

GPIO.setup(ENB,GPIO.OUT)
enb_pwm=GPIO.PWM(ENB,100)
GPIO.setup(IN3,GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)

#CAR MOVEMENTS
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

def stop(tme):
    ena_pwm.start(0)
    enb_pwm.start(0)
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(tme)
  
def uturn(tm):
    ena_pwm.start(0)
    enb_pwm.start(0)
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)
    time.sleep(tm)
    
print("Car moves forward")
forward()
time.sleep(5)

print("Car moves left")
left()
forward()
time.sleep(5)
stop(1)

print("Car moves right")
right()
forward()
time.sleep(5)
stop(1)

print("Car makes uturn")
uturn(1)
forward()
time.sleep(5)
stop(1)

print("Car reverses")
reverse()
forward()
time.sleep(5)
stop(1)
