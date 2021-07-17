import RPi.GPIO as GPIO
import time
import subprocess

def execute_unix(inputcommand):
    p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return output

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
while 1:

    GPIO.setmode(GPIO.BCM)
    print("Distance Measurement In Progress")
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG, False)
    print("Waiting For Sensor To Settle")
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17000

    distance = round(distance, 2)
    
    print("Distance:",distance,"cm")
    
    # 1 foot = 12 inches = 30.48cm
    if distance <= 31:
        dist = str(distance)
        string = "Careful obstacle is "+dist+" centimeters away"
        c = 'espeak -ven+m4 -k5 -s140 --punct="<characters>" "%s" 2>>/dev/null' % string
        execute_unix(c)
        print("Alert!")
        time.sleep(2)
    GPIO.cleanup()
