import random
import string
from Database import *
from email.message import EmailMessage
import ssl
import smtplib
class Service:
    def login(userID, password):
        mydb = Database.connectToDB()
        try:
            result = Database.getUserFromUserTableForLogin(mydb, userID, password)
        except  TypeError:
            print("TypeError: User Details incorrect")
            return False
        return result

    def forgottenPassword(email):
        mydb = Database.connectToDB()
        try:
            letters = string.ascii_lowercase
            newPassword = ''.join(random.choice(letters) for i in range(10))
            email_sender = 'trackerpto@gmail.com'
            email_password = 'fdlsrxyzibrzjmyl'
            user = Database.forgottenPassword(mydb, email)
            print(user)
            email_reciever = user.email
            subject = "New Password"
            body = """Your new password is: """+newPassword
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_reciever
            em['Subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_reciever, em.as_string())
            Database.updateUserInfoPassword(mydb, user.userID, newPassword)
            return True
        except  TypeError:
            print("TypeError: Email doesn't exist")
            return False
        
    def getUserHolidayRequests(userID):
        mydb = Database.connectToDB()
        try:
            holidayRequests = Database.getPTORequest(mydb, userID)
            return holidayRequests
        except TypeError:
            return False

            