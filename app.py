from flask import Flask
from Database import *
from Database import Database
import json
from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager
from flask_cors import CORS, cross_origin

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
    userId = Database.get_user_id_from_email(mydb, email)

    if userId is None:
        return {"msg": "User not found"}, 404
    user = Database.getUserFromUserTableForLogin(mydb, userId, password)
    if isinstance(user, dict):
        return user, 401

    if user:
        access_token = create_access_token(identity=userId)
        return {"access_token": access_token}
    else:
        return {"msg": "Wrong email or password"}, 401


@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


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