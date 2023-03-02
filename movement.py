import RPi.GPIO as GPIO          
from time import sleep

in1 = 24 #left1 
in2 = 23 #right 1
in3 = 22 #left 2
in4 = 21 #right 2

TRIG=20
ECHO=19
GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG,False)

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

GPIO.setup(11,GPIO.OUT) #Servo motor

#Ultrasonic sensor
print("waiting for sensor to settle")
time.sleep(0.2)
GPIO.output(TRIG,True)
time.sleep(0.00001)
GPIO.output(TRIG,False)
     while GPIO.input(ECHO)==0:
       pulse_start=time.time()
     while GPIO.input(ECHO)==1:
        pulse_end=time.time()
    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17150
    distance=round(distance,2)
    print("distance:",distance,"cm")
    time.sleep(2)
    if (distance>15):
        wheels('f')
    elif(distance<15):
        wheels('s')
        
def wheels(char x):
    print("s-stop f-forward b-backward l-left r-right e-exit")
    print("\n")    

     while(1):
         
         if(x=='f'):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.HIGH)
         GPIO.output(in3,GPIO.LOW)
         GPIO.output(in4,GPIO.LOW)
         print("forward")

        elif (x=='b'):
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.LOW)
         GPIO.output(in3,GPIO.HIGH)
         GPIO.output(in4,GPIO.HIGH)
         print("backward")

        elif x=='s':
         print("stop")
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.LOW)
         GPIO.output(in3,GPIO.LOW)
         GPIO.output(in41,GPIO.LOW)


        else:
         print("<<<  wrong data  >>>")
         print("please enter the defined data to continue.....")
 def rotate():
    servo.start(0)
    print ("Rotating 45 degrees")
   duty = 2
   while duty <= 14:
     servo.ChangeDutyCycle(duty)
     duty = duty + 1
