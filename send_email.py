
import smtplib  
import ssl    
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

#subject='automatic message generated via python -reaz' 
#body='body of the email: this is a test email'

class EMAIL(object): 
    
    def __init__(self): 
        
        self.subject="Home Security Picked Up Signal" 
        self.body="Possible detection of a person outside the door"
        
        self.sender_email= 'reazrpi@gmail.com'  
        self.password='satisclose'   
        
        self.recipients=['reazrpi@gmail.com','reaz.rahman@macaulay.cuny.edu'] 
        
        self.smtp_server='smtp.gmail.com' 
        self.port=587 


    def send_email_with_images(self,filenames):   
          
        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = self.sender_email
        msg['To'] = ", ".join(self.recipients)
    
        text = MIMEText(self.body)  
        msg.attach(text) 
        
        
        for each_file in filenames: 
            image_data=open(each_file,'rb').read() 
            attached_image=MIMEImage(image_data, name=os.path.basename(each_file)) 
            msg.attach(attached_image)
            
        
    
        try:   
            s = smtplib.SMTP(self.smtp_server,self.port)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(self.sender_email, self.password)
            s.sendmail(self.sender_email,self.recipients, msg.as_string())
            s.quit() 
            print ('Email successfully sent with attached images') 
        
        except: 
            print ('SORRY! something went wrong, email couldnt be sent')
            
        

    def send_email_with_text(self): 
        
        smtp_server='smtp.gmail.com' 
        port=587 
        sender_email='reazrpi@gmail.com'  
        password='satisclose'  
        
        #receiver_email='reazrpi@gmail.com'  
        recipients=['reazrpi@gmail.com','reaz.rahman@macaulay.cuny.edu']
        
        context = ssl.create_default_context()
        
        
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = ", ".join(recipients)
        message["Subject"] = self.subject 
        message.attach(MIMEText(self.body, "plain"))
        
        
        
        # Try to log in to server and send email 
        text=message.as_string()
        try:
            server = smtplib.SMTP(smtp_server,port)
            server.ehlo() # Can be omitted
            server.starttls(context=context) # Secure the connection
            server.ehlo() # Can be omitted
            server.login(sender_email, password)
            
            server.sendmail(sender_email, recipients, text) 
            
            print ('email successfully sent')
        
        except Exception as e:
            print ('ATTN!!! Failed to send the email')
            print(e)
        finally:
            server.quit()  

if __name__=="__main__": 
    
    email=EMAIL()  
    email.send_email_with_images(['image1.jpg','image2.jpg','image3.jpg'])
    
