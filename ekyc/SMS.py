from twilio.rest import Client 
from random import randint
class SMS():
    def __init__(self,  account_sid= 'account_sid',
                        auth_token = 'auth_token',
                        messaging_service_sid='messaging_service_sid'):

        self.account_sid            = account_sid
        self.auth_token             = auth_token 
        self.messaging_service_sid  = messaging_service_sid
        self.client = Client(account_sid, auth_token) 
    
    def send_otp(self,tel,otp_code):
        data = "OTP code is "+ otp_code
        message = self.client.messages.create(  
                                    messaging_service_sid=self.messaging_service_sid, 
                                    body=data,      
                                    to=tel 
                                ) 
        
        print(message.sid)
    
    def send_messages(self,tel,data):        
        message = self.client.messages.create(  
                                    messaging_service_sid=self.messaging_service_sid, 
                                    body=data,      
                                    to=tel 
                                ) 
        
        print(message.sid)

if __name__ == "__main__":
    account_sid = 'account_sid' 
    auth_token = 'auth_token'
    messaging_service_sid='messaging_service_sid'
    otp = SMS(account_sid,auth_token,messaging_service_sid)
    otp_code = str(randint(0,9999)).zfill(6)
    otp.send_messages("+66xxxxx","test")
