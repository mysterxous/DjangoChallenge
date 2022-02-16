import smtplib, ssl

class Mail:
    
    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = ' '
        self.password = ' '

    def send(self, email, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.ehlo()
        # service.set_debuglevel(1)
        service.login(self.sender_mail, self.password)
        
        try:
            service.sendmail(self.sender_mail, email, f"Subject: {subject}\n{content}")
        except:
            print("Email delivery failure")

        
        service.quit()
    
    def send_otp(self,email, otp):
        subject = "Verify Your email address"
        content = "Thank you for verifying your %s account.\n \n Here is your verification code: %s" % (email,otp)
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, )
        # service.starttls()
        # service.ehlo()
        # service.set_debuglevel(1)
        service.login(self.sender_mail, self.password)
        
        # service.sendmail(self.sender_mail, email, f"Subject: {subject}\n{content}")
        try:
            service.sendmail(self.sender_mail, email, f"Subject: {subject}\n{content}")
        except:
            print("Email delivery failure")

        service.close()
        # service.quit()


if __name__ == '__main__':

    email = " "
    subject = "Verify Your email address"
    # content = "Thanks for verifying your %s account.\n\n Your code is: %s"% (email,"9999")
    content = "Thank you for verifying your %s account.\n \n Here is your verification code: %s" % (email,"9999")

    mail = Mail()
    mail.send_otp(email,"5555")