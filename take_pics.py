import time 
import picamera 

class CAMERA(object): 
    
    def __init__(self,take=3,sleep=3): 
        
        self.how_many=take   
        self.sleep_time=sleep
        self.filenames=[]
        
    def take_pic(self,imagename): 
        
        with picamera.PiCamera() as camera: 
            camera.resolution=(1024,768) 
            camera.start_preview()  
            #camera warm up 
            time.sleep(2) 
            camera.capture(imagename) 
    
    def take_multiple_pics(self): 
        
        for i in range(self.how_many): 
            imagename='image'+str(i)+'.jpg'  
            self.filenames.append(imagename)
            self.take_pic(imagename) 
            time.sleep(self.sleep_time)