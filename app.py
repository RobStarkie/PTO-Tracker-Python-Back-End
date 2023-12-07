from flask import Flask
from Database import *
from Database import Database
import json
from flask import Flask, request, jsonify
from flask import Flask, request, jsonify, Response
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager
from flask_cors import CORS, cross_origin
from Service import *
import json

mydb = Database.connectToDB()
Database.createTables(mydb)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
CORS(app)
jwt = JWTManager(app)

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

@app.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    admin = False
    try:
        
        if Service.login(email, password)==False:
            return {"msg": "Wrong email or password"}, 401
        user=Service.getUserByEmail(email)
        if user.admin ==True:
            admin = True
    except TypeError:
        return {"msg": "Wrong email or password"}, 401
    access_token = create_access_token(identity=email)
    response = {"access_token":access_token, "admin": admin}
    return response

@app.route("/logout", methods=["POST"])
def logout():
    current_user = get_jwt_identity()
    print(logged_in_as=current_user)
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response



@app.route("/getHolidays", methods =["GET"])
@jwt_required()
def getHolidays():
    print("getting holidays")
    current_user = get_jwt_identity()
    print(current_user)
    user = Service.getUserByEmail(current_user)
    print("userID: "+str(user.userID))
    hr = Service.getUserHolidayRequests(user.userID)
    print("hr: ")
    print(hr[0].requestID)
    #hr = np.array(hr)
    print(hr)
    list = []
    for x in hr:
        a = x.userID
        list.append(a)
        b = x.startDate.strftime("%Y-%m-%d")
        list.append(b)
        c = x.endDate.strftime("%Y-%m-%d")
        list.append(c)
        d = x.status.name
        list.append(d)
    print(list)
    return json.dumps(list)

@app.route("/addNewHolidayRequest", methods =["POST"])
@jwt_required()
def addNewHolidayRequest():

    try:
        startDate = request.json.get("startDate", None)
        endDate = request.json.get("endDate", None)
        date1 = datetime.strptime(startDate, '%Y-%m-%d').date()
        date2 = datetime.strptime(endDate, '%Y-%m-%d').date()
        if(date1<=date2):
            current_user = get_jwt_identity()
            user = Service.getUserByEmail(current_user)
            hr = HolidayRequest(None, user.userID, startDate, endDate, Status.REVIEW)
            Service.addNewHolidayRequest(hr)
            return {"msg": "New Holiday Request Added"}, 200
            return {"msg": "Date is goof"}, 200
        else:
            return{"msg": "Dates are incorrect"}, 500            
    except TypeError:
        print(TypeError)
        return {"msg": "Couldnt add holiday request: "+ TypeError}, 401
    
@app.route("/addNewUser", methods =["POST"])
@jwt_required()
def addNewUser():
    try:
        userID = request.json.get("userID")
        TeamID = request.json.get("TeamID")
        Email = request.json.get("Email")
        FirstName = request.json.get("FirstName") 
        SecondName = request.json.get("SecondName")
        Password = request.json.get("Password")
        ProfilePicture = request.json.get("ProfilePicture")
        PhoneNumber = request.json.get("PhoneNumber")
        LineManager = request.json.get("LineManager")
        LineManagerID = request.json.get("LineManagerID")
        TotalHolidays = request.json.get("TotalHolidays")
        Admin = request.json.get("Admin")
        user = User(userID, TeamID, Email, FirstName, SecondName, Password, ProfilePicture, PhoneNumber, LineManager, LineManagerID, TotalHolidays, Admin)
        Service.addNewUser(user)
        return {"msg": "Added new user"}, 200
    except TypeError:
        return {"msg": "Failed to add new user" + TypeError}, 401
    
@app.route("/getUser", methods =["POST"])
@jwt_required()
def getUser():
    try:
        userID = request.json.get("userID")
        print(userID)
        user = Service.getUserByID(userID)
        response = {'UserID': user.userID, 'TeamID': user.teamID, 'Email': user.email, 'FirstName': user.firstName, 'SecondName': user.secondName, 'password': user.password, 'ProfilePicture': user.profilePicture, 'phoneNumber': user.phoneNumber, 'LineManager': user.lineManager, 'LineManagerID': user.lineManagerID, 'TotalHolidays': user.totalHolidays, 'Admin': user.admin}
        return response
    except TypeError:
        print(TypeError)
        return {"msg": "Couldnt edit user: "+ TypeError}, 401 

@app.route("/editUser", methods =["POST"])
@jwt_required()
def editUser(): 
    try:
        userID = request.json.get("userID")
        TeamID = request.json.get("TeamID")
        Email = request.json.get("Email")
        FirstName = request.json.get("FirstName") 
        SecondName = request.json.get("SecondName")
        Password = request.json.get("Password")
        ProfilePicture = request.json.get("ProfilePicture")
        PhoneNumber = request.json.get("PhoneNumber")
        LineManager = request.json.get("LineManager")
        LineManagerID = request.json.get("LineManagerID")
        TotalHolidays = request.json.get("TotalHolidays")
        Admin = request.json.get("Admin")
        user = User(userID, TeamID, Email, FirstName, SecondName, Password, ProfilePicture, PhoneNumber, LineManager, LineManagerID, TotalHolidays, Admin)
        print(user)
        Service.updateEntireAccount(user)
        return {"msg": "Edited existing account"}, 200
    except TypeError:
        return {"msg": "Failed to add new user"}, 401
    
@app.route("/editAccount", methods =["POST"])
@jwt_required()
def editPassword():
    try:
        password = request.json.get('password')
        current_user = get_jwt_identity()
        print(current_user)
        print(password)
        Service.editUserAccountByUser(current_user, password)
    except TypeError:
        return {"msg": "Failed to change password"}, 401


from datetime import datetime, timedelta
from govuk_bank_holidays.bank_holidays import BankHolidays

@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    identity=get_jwt_identity()
    response = jsonify({"user":identity})
    return response


@app.route('/api/team-view', methods=["GET"])
@jwt_required()
def get_team_holidays():    
    userId = get_jwt_identity()
    line_manager_id = Database.getCurrentUserLineManagerID(mydb, userId)
    # Gets the line managerId for the current user
    if line_manager_id is None:
        return {"msg":"Line Manager not found for this user"}, 404

    # Gets all users who are under lineManagers UserID
    team_userids = Database.getTeamMembers(mydb, line_manager_id)
    if not team_userids:
        return {"msg": "No team members found for this Line Manager"}, 404
    
    team_details = []

    for memberId in team_userids:
        user_details = Database.getUserDetails(mydb, memberId)
        if user_details:
            user_details['holidays'] = Database.getPTORequestDict(mydb, memberId)
            team_details.append(user_details)
    return team_details


@app.route("/make-holiday-request", methods=["GET"])
@jwt_required()
def count_work_hours():
    start_date = request.json.get("start-date", None)
    end_date = request.json.get("end-date", None)
    work_hours_per_day = [8,8,8,8,5] #change this to get from db
    total_holiday_hours = 137 #change this to get from db
    bank_holidays = BankHolidays()
    holidays = {holiday['date'] for holiday in bank_holidays.get_holidays()}

    current_date = start_date
    total_work_hours = 0

    while current_date <= end_date:
        # Check if the current day is a weekday and not a bank holiday
        if current_date.weekday() < 5 and current_date not in holidays:
            total_work_hours += work_hours_per_day[current_date.weekday()]

        # Move to the next day
        current_date += timedelta(days=1)

    return total_holiday_hours - total_work_hours #holiday hours remaining

"""# Example usage:
start_date = datetime(2023, 1, 1)  # Replace with your start date
end_date = datetime(2023, 12, 31)   # Replace with your end date
work_hours_per_day = [8, 8, 8, 8, 5]  # Replace with your work hours for each day
total_holiday_hours = 137

total_work_hours = count_work_hours(start_date, end_date, work_hours_per_day, total_holiday_hours)
print(f"Holiday hours remaining {start_date.date()} and {end_date.date()}: {total_work_hours}")
"""
