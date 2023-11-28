import mysql.connector
from User import *

class Database:
    def connectToDB():
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="AquaductStreet9",
        database = 'hr_management'
        )
        return mydb
        
    def createTables(mydb):
        fd = open('database_create.sql', 'r')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')
        cursor = mydb.cursor()
        for command in sqlCommands:
            cursor.execute(command)

    def addNewUserToDB(mydb, user):
        lineManager=0
        if user.lineManager == True:
            lineManager=1
        sqlCommand = "INSERT INTO users (UserID, Email, FirstName, SecondName, Password, ProfilePicture, PhoneNumber, LineManager, LineManagerID, TotalHolidays) SELECT * FROM (SELECT '"+str(user.userID)+"','"+user.email+"','"+user.firstName+"','"+user.secondName+"','"+user.password+"','"+user.profilePicture+"','"+str(user.phoneNumber)+"','"+str(lineManager)+"','"+str(user.lineManagerID)+"','"+str(user.totalHolidays)+"'"+") AS tmp WHERE NOT EXISTS (SELECT UserID FROM users WHERE UserID = "+str(user.userID)+") LIMIT 1;"
        print(sqlCommand)
        cursor = mydb.cursor()
        cursor.execute(sqlCommand)
        mydb.commit()

    def getUserFromUserTable(mydb, userID):
        print("getuser")
        cursor = mydb.cursor()
        sqlCommand = "SELECT * FROM users WHERE UserID = "+str(userID)+";"
        cursor.execute(sqlCommand)
        result = cursor.fetchone()
        lineManager=False
        if result[7] == "1":
            lineManager=True
        tempUser = User(int(result[0]), result[1], result[2], result[3],result[4], result[5], int(result[6]), lineManager, int(result[8]), int(result[9]))
        return tempUser
    
    def updateUserInfoPassword(mydb, userID, password):
        cursor = mydb.cursor()
        sqlCommand = "UPDATE users SET Password = '"+password+"' WHERE UserID = '"+str(userID)+"';"
        print(sqlCommand)
        cursor.execute(sqlCommand)
        mydb.commit()

    def updateEntireUser(mydb, user):
        lineManager=0
        if user.lineManager == True:
            lineManager=1
        sqlCommand = "UPDATE users SET Email = '"+user.email+"', FirstName = '"+user.firstName+"', SecondName= '"+user.secondName+"',  Password= '"+user.password+"',  ProfilePicture = '"+user.profilePicture+"', PhoneNumber = '"+str(user.phoneNumber)+"', LineManager = '"+str(lineManager)+"', LineManagerID = '"+str(user.lineManagerID)+"', TotalHolidays = '"+str(user.totalHolidays)+"' WHERE UserID = '"+str(user.userID)+"';"
        print(sqlCommand)
        cursor = mydb.cursor()
        cursor.execute(sqlCommand)
        mydb.commit()