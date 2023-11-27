from Database import *
from User import *

def test_database_createTables():

    mydb = Database.connectToDB()
    Database.createTables(mydb)
    #add user to table
    
    #assert cursor == "('hr_management',),('information_schema',),('mysql',),('performance_schema',)"

def test_createAddingAndRetrievingUserFromUserTable():
    mydb = Database.connectToDB()
    testUser = User(1,"test@email.com", "Rob", "Stark","password", "picture", 12333446, False, 1278654, 25 )
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

