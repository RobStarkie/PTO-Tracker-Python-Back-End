import datetime
import random
import re
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
    
    def addNewUser(user):
        mydb = Database.connectToDB()
        if Service.checkEmail(user.email)==False:
            return False
        
        try:
            if Database.searchUser(mydb, user.userID) == False:
                Database.addNewUserToDB(mydb, user)
                return True
            else:
                return False
        except TypeError:
            return False

    def checkEmail(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if(re.fullmatch(regex, email)):
            return True
            print("Valid Email")
    
        else:
            return False
            print("Invalid Email")

    def forgottenPassword(email):
        mydb = Database.connectToDB()
        try:
            newPassword = Service.generateNewPassword()
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
        
    def generateNewPassword():
        letters = string.ascii_lowercase
        password = ''.join(random.choice(letters) for i in range(10))
        return password
        
        
    def getUserHolidayRequests(userID):
        mydb = Database.connectToDB()
        try:
            holidayRequests = Database.getPTORequest(mydb, userID)
            return holidayRequests
        except TypeError:
            return False
        
    def editUserAccountByUser(userID, password):
        mydb = Database.connectToDB()
        try:
            Database.updateUserInfoPassword(mydb, userID, password)
            return True
        except TypeError:
            return False
    
    def addNewHolidayRequest(hr):
        mydb = Database.connectToDB()
        if (Service.validateDate(hr.startDate) == True) and (Service.validateDate(hr.endDate) == True):
            hr.startDate = Service.insertDateIntoDatetime(hr.startDate)
            hr.endDate = Service.insertDateIntoDatetime(hr.endDate)
            print(hr.startDate)
            print(hr.endDate)
            try:
                Database.addNewPTORequest(mydb, hr)
                return True
            except TypeError:
                return False
        else:
            #incorrect formate
            return False
        
    def validateDate(date):
        print(date)
        res = False
        try:
            res = bool(datetime.date.fromisoformat(date))
        except ValueError:
            print("Incorrect Date Format")
            res = False
        return res
    
    def insertDateIntoDatetime(passedDate):
        passedDate = passedDate.split("-")
        year = int(passedDate[0])
        month = int(passedDate[1])
        day = int(passedDate[2])
        try:
            passedDate = datetime.date(year,month,day)
            print(passedDate)
            return passedDate
        except ValueError:
            return False
        
    def getTeamMembers(userID):
        mydb = Database.connectToDB()
        try:
            user = Database.getUserFromUserTable(mydb, userID)
            print(user.lineManager)
            if user.lineManager== True:
                teamMembers = Database.getTeamMembers(mydb, userID)
                return teamMembers
            else:
                print("userID isnt a line manager")
                return False
        except TypeError:
            print("incorrect userID")
            return False