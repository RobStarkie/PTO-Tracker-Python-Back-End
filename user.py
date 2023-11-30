class User:
    def __init__(self, userID, teamID, email, firstName, secondName, password, profilePicture, phoneNumber, lineManager, lineManagerID, totalHolidays, admin):
        self.userID = userID
        self.teamID = teamID
        self.email = email
        self.firstName = firstName
        self.secondName = secondName   
        self.password = password
        self.profilePicture = profilePicture
        self.phoneNumber = phoneNumber
        self.lineManager = lineManager
        self.lineManagerID = lineManagerID
        self.totalHolidays = totalHolidays
        self.admin = admin