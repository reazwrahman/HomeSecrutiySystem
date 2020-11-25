import RPi.GPIO as GPIO 
import time

class LED(object):

    def __init__(self,pin):

        self.pin=pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,GPIO.OUT)

    def control (self,status):
 
        if status=='on':
            GPIO.output(self.pin,GPIO.HIGH)

        elif status=='off':
            GPIO.output(self.pin,GPIO.LOW)
    
    def dim(self): 
        
        pwm=GPIO.PWM(self.pin,100) #initialize at 100hz frequency
        pwm.ChangeDutyCycle(50)

if __name__=="__main__": 
    
    def main(): 
        while True:
            a=LED(26)
            a.control('on')
            time.sleep(1)
            a.control('off') 
            a.dim()
            time.sleep(1) 
    
    main()
