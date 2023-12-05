from datetime import *
from Database import *
from user import *
from Status import *
from Service import *

def test_loginUserFound():
    testUser = User(1,1,"test@test.com","Rob","Stark","das","picture",12333446,False,1278654,25,False)
    email = "test@test.com"
    password = "das"
    result = Service.login(email, password)

    assert (result==True)

def test_loginNoUserFound():
    #incorrect userID, correct password
    userID = 2
    password = "das"
    result = Service.login(userID, password)
    print(result)
    assert (result == False)
    #correct userID, incorrect password
    userID = 1
    password = "vgvgh"
    result = Service.login(userID, password)
    print(result)
    assert (result == False)

def test_loginIncorrectVariableTypes():
    userID = False
    password = "asdas"
    result = Service.login(userID, password)
    print(result)
    assert (result == False)

def test_forgottenPassword():
    mydb = Database.connectToDB()
    initalUser = User(4,2,"trackerpto@gmail.com", "James", "May","TopGear", "picture", 12333446, False, 1278654, 25,False )
    Service.addNewUser(initalUser)
    result = Service.forgottenPassword(initalUser.email)
    editedUser = Database.getUserFromUserTable(mydb, 4)
    assert (initalUser.password != editedUser.password)
    assert (result == True)

def test_forgottenPasswordIncorrectEmail():
    mydb = Database.connectToDB()
    result = Service.forgottenPassword("tes@test.com")

    assert(result==False)

def test_getUserHolidayRequests():
    userID = 3
    holidayRequests = Service.getUserHolidayRequests(userID)

    assert(holidayRequests[0].requestID == 3)
    assert(holidayRequests[1].requestID == 4)

def test_getUserHolidayRequestsIncorrectUserID():
    userID = 5555555555
    holidayRequests = Service.getUserHolidayRequests(userID)
    assert(holidayRequests == [])

def test_generateNewPassword():
    password = Service.generateNewPassword()
    assert (password is not None)

def test_editMyAccount():
    newPassword = Service.generateNewPassword()
    testUser = User(5,1,"testEmail@email.com", "Jeremy", "Clarkson", "GrandTour", "picture", 12333446, False, 1278654, 25 , False)
    Service.addNewUser(testUser)
    result = Service.editUserAccountByUser(testUser.userID, newPassword)
    mydb = Database.connectToDB()
    updatedUser = Database.getUserFromUserTable(mydb, 5)
    assert (updatedUser.password == newPassword)
    
def test_newHolidayRequest():
    hr = HolidayRequest(None,3,"2019-06-22","2019-06-25",Status.APPROVED)
    Service.addNewHolidayRequest(hr)
    result = Service.getUserHolidayRequests(3)
    assert (hr.userID == result[1].userID)
    assert (datetime.date(2019,6,22) == result[1].startDate)
    assert (datetime.date(2019,6,25) == result[1].endDate)
    assert (hr.status == result[1].status)

def test_newHolidayRequestIncorrectDateFormate1():
    hr = HolidayRequest(None,4,"15-6-2020","2019-6-16",Status.APPROVED)
    result = Service.addNewHolidayRequest(hr)
    assert(result==False)

def test_newHolidayRequestIncorrectDateFormate2():
    hr = HolidayRequest(None,4,"15","2019-6-16",Status.APPROVED)
    result = Service.addNewHolidayRequest(hr)
    assert(result==False)

def test_newHolidayRequestIncorrectDateFormate3():
    hr = HolidayRequest(None,4,"s","2019-6-16",Status.APPROVED)
    result = Service.addNewHolidayRequest(hr)
    assert(result==False)

def test_getTeamMembers():
    lineManager = User(1278654,1,"testtest@email.com", "Richard", "Hammond", "Crash", "picture", 12333446, True, 2321213, 25 , False)
    teamMembers = Service.getTeamMembers(lineManager.userID)
    print(teamMembers)
    assert (teamMembers[0] == 1)
    assert (teamMembers[1] == 2)
    assert (teamMembers[2] == 4)
    assert (teamMembers[3] == 5)







