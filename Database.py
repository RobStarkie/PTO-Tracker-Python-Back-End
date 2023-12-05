import mysql.connector
from user import *
from HolidayRequest import *
from Status import *

class Database:
    @staticmethod
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
    
    def searchUser(mydb, userID):
        info = []
        info.append(userID)
        sqlCommand = "SELECT UserID FROM users WHERE UserID = %s;"
        cursor = mydb.cursor()
        cursor.execute(sqlCommand,info)
        result = cursor.fetchone()
        if result is not None:
            return True
        else:
            return False

    def addNewUserToDB(mydb, user):
        info = []
        info.append(user.userID)
        info.append(user.teamID)
        info.append(user.email)
        info.append(user.firstName)
        info.append(user.secondName)
        info.append(user.password)
        info.append(user.profilePicture)
        info.append(user.phoneNumber)
        if user.lineManager == False:
            info.append(0)
        else:
            info.append(1)
        info.append(user.lineManagerID)
        info.append(user.totalHolidays)
        if user.admin == False:
            info.append(0)
        else:
            info.append(1)
        sqlCommand = "INSERT INTO users (UserID, TeamID, Email, FirstName, SecondName, Password, ProfilePicture, PhoneNumber, LineManager, LineManagerID, TotalHolidays, Admin) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        print(sqlCommand)
        print(info)
        cursor = mydb.cursor()
        cursor.execute(sqlCommand, info)
        mydb.commit()

    def getUserFromUserTable(mydb, userID):
        print("getuser")
        cursor = mydb.cursor()
        sqlCommand = "SELECT * FROM users WHERE UserID = "+str(userID)+";"
        cursor.execute(sqlCommand)
        result = cursor.fetchone()
        lineManager=False
        if result[8] == 1:
            lineManager=True
        Admin = False
        if result[11] == 1:
            Admin = True
        print(result)
        tempUser = User(int(result[0]), int(result[1]), result[2], result[3],result[4], result[5], result[6], int(result[7]), lineManager, int(result[9]), int(result[10]), Admin)
        return tempUser
    
    def getUserFromUserTableEmail(mydb, email):
        print("getuser")
        list = []
        list.append(email)
        cursor = mydb.cursor()
        sqlCommand = "SELECT * FROM users WHERE Email = %s;"
        cursor.execute(sqlCommand, list)
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return {"msg": "User with this Id and password does not exist"}
        
        lineManager=False
        if result[8] == 1:
            lineManager=True
        Admin = False
        if result[11] == 1:
            Admin = True
        print(result)
        tempUser = User(int(result[0]), int(result[1]), result[2], result[3],result[4], result[5], result[6], int(result[7]), lineManager, int(result[9]), int(result[10]), Admin)
        return tempUser

    def getUserFromUserTableForLogin(mydb, email, password):
        cursor = mydb.cursor()
        info = []
        info.append(email)
        info.append(password)
        sqlCommand = "SELECT * FROM users WHERE (Email = %s AND Password = %s);"
        cursor.execute(sqlCommand, info)
        result = cursor.fetchone()
        lineManager=False
        if result[8] == 1:
            lineManager=True
        Admin = False
        if result[11] == 1:
            Admin = True
        print(result)
        tempUser = User(int(result[0]), int(result[1]), result[2], result[3],result[4], result[5], result[6], int(result[7]), lineManager, int(result[9]), int(result[10]), Admin)
        if (tempUser.email == email):
            return True
        else:
            return False
    
    def get_user_id_from_email(mydb, email):
        cursor = mydb.cursor()
        cursor.execute("SELECT UserID FROM users WHERE Email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]  # Return the UserID
        else:
            return None  # No user found with this email
    
    def forgottenPassword(mydb, email):
        cursor = mydb.cursor()
        info = []
        info.append(email)
        sqlCommand = "SELECT * FROM users WHERE (Email = %s);"
        cursor.execute(sqlCommand, info)
        result = cursor.fetchone()
        lineManager=False
        if result[8] == 1:
            lineManager=True
        Admin = False
        if result[11] == 1:
            Admin = True
        print(result)
        tempUser = User(int(result[0]), int(result[1]), result[2], result[3],result[4], result[5], result[6], int(result[7]), lineManager, int(result[9]), int(result[10]), Admin)
        return tempUser

    
    def updateUserInfoPassword(mydb, userID, password):
        cursor = mydb.cursor()
        info = []
        info.append(password)
        info.append(userID)
        sqlCommand = "UPDATE users SET Password = %s WHERE UserID = %s;"
        print(sqlCommand, info)
        cursor.execute(sqlCommand, info)
        mydb.commit()

    def updateEntireUser(mydb, user):
        info = []
        info.append(user.teamID)
        info.append(user.email)
        info.append(user.firstName)
        info.append(user.secondName)
        info.append(user.password)
        info.append(user.profilePicture)
        info.append(user.phoneNumber)
        if user.lineManager == False:
            info.append(0)
        else:
            info.append(1)
        info.append(user.lineManagerID)
        info.append(user.totalHolidays)
        if user.admin == False:
            info.append(0)
        else:
            info.append(1)
        info.append(user.userID)
        sqlCommand = "UPDATE users SET TeamID = %s, Email = %s, FirstName = %s, SecondName= %s,  Password= %s,  ProfilePicture = %s, PhoneNumber = %s, LineManager = %s, LineManagerID = %s, TotalHolidays = %s, Admin = %s  WHERE UserID = %s;"
        print(sqlCommand)
        cursor = mydb.cursor()
        cursor.execute(sqlCommand, info)
        mydb.commit()

    def getPTORequest(mydb, userID):
        cursor = mydb.cursor()
        sqlCommand = "SELECT * FROM pto_requests WHERE UserID = "+str(userID)+";"
        cursor.execute(sqlCommand)
        result = cursor.fetchall()
        list = []
        for x in result:
            hr = HolidayRequest(int(x[0]), int(x[1]), x[2], x[3], x[4])
            match hr.status:
                case "Status.APPROVED":
                    hr.status = Status.APPROVED
                case "Status.DENIED":
                    hr.status = Status.DENIED
                case "Status.REVIEW":
                    hr.status = Status.REVIEW
            list.append(hr)
        return list
    
    def addNewPTORequest(mydb, request):
        cursor = mydb.cursor()
        sqlCommand = "INSERT INTO pto_requests (UserID, Start, End, Status) SELECT * FROM ( SELECT '"+str(request.userID)+"' , '"+str(request.startDate)+"' , '"+str(request.endDate)+"' , '"+str(request.status)+"') AS tmp WHERE NOT EXISTS (SELECT * FROM pto_requests where UserID = '"+str(request.userID)+"' AND Start = '"+str(request.startDate)+"' AND End = '"+str(request.endDate)+"') LIMIT 1;"
        cursor.execute(sqlCommand)
        mydb.commit()

    def changeStateOfRequest(mydb, requestID, status):
        cursor = mydb.cursor()
        sqlCommand = "UPDATE pto_requests SET Status = '"+str(status)+"' where requestID = '"+str(requestID)+"';"
        cursor.execute(sqlCommand)
        mydb.commit()

    def getTeamMembers(mydb, userID):
        cursor = mydb.cursor()
        id = []
        id.append(userID)
        sqlCommand = "SELECT DISTINCT UserID FROM users WHERE LineManagerID = %s;"
        cursor.execute(sqlCommand, id)
        result = cursor.fetchall()
        return [int(x[0]) for x in result]
    