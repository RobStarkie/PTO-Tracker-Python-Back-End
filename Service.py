from Database import *

class Service:
    def login(userID, password):
        mydb = Database.connectToDB()
        try:
            result = Database.getUserFromUserTableForLogin(mydb, userID, password)
        except  TypeError:
            print("TypeError: User Details incorrect")
            return False
        return result
