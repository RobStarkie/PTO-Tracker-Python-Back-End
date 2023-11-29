import datetime
from Database import *
from User import *
from Status import *
from Service import *

def test_loginUserFound():
    testUser = User(1,"test@email.com", "Rob", "Stark","das", "picture", 12333446, False, 1278654, 25 )
    userID = "1"
    password = "das"
    result = Service.login(userID, password)

    assert (testUser.userID ==result.userID)
    assert (testUser.email ==result.email)
    assert (testUser.firstName ==result.firstName)
    assert (testUser.secondName ==result.secondName)
    assert (testUser.password == result.password)
    assert (testUser.profilePicture ==result.profilePicture)
    assert (testUser.phoneNumber ==result.phoneNumber)
    assert (testUser.lineManager ==result.lineManager)
    assert (testUser.lineManagerID ==result.lineManagerID)
    assert (testUser.totalHolidays ==result.totalHolidays)

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