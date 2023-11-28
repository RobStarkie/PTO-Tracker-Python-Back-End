from Status import *

class HolidayRequest:
    def __init__ (self, userID, startDate, endDate, status) :
        self.userID = userID
        self.startDate = startDate
        self.endDate = endDate
        self.status = status
