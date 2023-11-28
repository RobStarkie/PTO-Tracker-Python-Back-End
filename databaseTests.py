
import datetime
from Database import *
from User import *
from Status import *


def test_database_createTables():
    mydb = Database.connectToDB()
    Database.createTables(mydb)
    assert (mydb != None )

def test_createAddingAndRetrievingUserFromUserTable():
    mydb = Database.connectToDB()
    testUser = User(1,"test@email.com", "Rob", "Stark","das", "picture", 12333446, False, 1278654, 25 )
    Database.addNewUserToDB(mydb, testUser)
    result = Database.getUserFromUserTable(mydb, 1)
    assert (testUser.userID ==result.userID)
    assert (testUser.email ==result.email)
    assert (testUser.firstName ==result.firstName)
    assert (testUser.secondName ==result.secondName)
    assert (testUser.password ==result.password)
    assert (testUser.profilePicture ==result.profilePicture)
    assert (testUser.phoneNumber ==result.phoneNumber)
    assert (testUser.lineManager ==result.lineManager)
    assert (testUser.lineManagerID ==result.lineManagerID)
    assert (testUser.totalHolidays ==result.totalHolidays)

def test_changeUserPassword():
    mydb = Database.connectToDB()
    newPassword = "hagen"
    testUser = User(2,"mattsTest@email.com", "Matt", "Connolly", "password", "picture", 12333446, False, 1278654, 25 )
    Database.addNewUserToDB(mydb, testUser)
    Database.updateUserInfoPassword(mydb, 2, newPassword)
    result = Database.getUserFromUserTable(mydb, 2)
    assert (testUser.userID ==result.userID)
    assert (testUser.email ==result.email)
    assert (testUser.firstName ==result.firstName)
    assert (testUser.secondName ==result.secondName)
    assert (newPassword == result.password)
    assert (testUser.profilePicture ==result.profilePicture)
    assert (testUser.phoneNumber ==result.phoneNumber)
    assert (testUser.lineManager ==result.lineManager)
    assert (testUser.lineManagerID ==result.lineManagerID)
    assert (testUser.totalHolidays ==result.totalHolidays)

def test_changeUserProfile():
    mydb = Database.connectToDB()
    initalProfile = User(3,"someTest@email.com", "Matt", "Connolly", "password", "picture", 12333446, False, 1278654, 25 )
    newProfile  = User(3,"donkey@email.com", "Donkey", "Kong", "mario", "luigi", 555555, False, 555555, 35 )
    Database.addNewUserToDB(mydb, initalProfile)
    Database.updateEntireUser(mydb, newProfile)
    result = Database.getUserFromUserTable(mydb, 3)
    assert (newProfile.userID ==result.userID)
    assert (newProfile.email ==result.email)
    assert (newProfile.firstName ==result.firstName)
    assert (newProfile.secondName ==result.secondName)
    assert (newProfile.password == result.password)
    assert (newProfile.profilePicture ==result.profilePicture)
    assert (newProfile.phoneNumber ==result.phoneNumber)
    assert (newProfile.lineManager ==result.lineManager)
    assert (newProfile.lineManagerID ==result.lineManagerID)
    assert (newProfile.totalHolidays ==result.totalHolidays)

def test_getUserPTORequests():
    mydb = Database.connectToDB()
    requests = Database.getPTORequest(mydb,1)
    tempRequests = HolidayRequest(None,2,datetime.date(2018, 6, 15),datetime.date(2017, 6, 15),Status.APPROVED)
    requests = Database.getPTORequest(mydb, 2)

    assert(tempRequests.userID == requests[0].userID)
    assert(tempRequests.startDate == requests[0].startDate)
    assert(tempRequests.endDate == requests[0].endDate)
    assert(tempRequests.status == requests[0].status)

def test_addUserPTORequest():
    mydb = Database.connectToDB()
    tempRequests = HolidayRequest(None,1,datetime.date(2019, 6, 15),datetime.date(2019, 6, 16),Status.APPROVED)
    Database.addNewPTORequest(mydb, tempRequests)
    requests = Database.getPTORequest(mydb, 1)

    assert(tempRequests.userID == requests[0].userID)
    assert(tempRequests.startDate == requests[0].startDate)
    assert(tempRequests.endDate == requests[0].endDate)
    assert(tempRequests.status == requests[0].status)

def test_changePTORequestTOApproved():
    mydb = Database.connectToDB()
    tempRequests = HolidayRequest(None, 3,datetime.date(2019, 6, 15),datetime.date(2019, 6, 16),Status.DENIED)
    Database.addNewPTORequest(mydb, tempRequests)
    requests = Database.getPTORequest(mydb, 3)
    Database.changeStateOfRequest(mydb, requests[0].requestID, Status.APPROVED)
    requests = Database.getPTORequest(mydb, 3)

    assert(tempRequests.userID == requests[0].userID)
    assert(tempRequests.startDate == requests[0].startDate)
    assert(tempRequests.endDate == requests[0].endDate)
    assert(Status.APPROVED == requests[0].status)
