CREATE DATABASE IF NOT EXISTS hr_management;
USE hr_management;
CREATE TABLE IF NOT EXISTS users (
    UserID VARCHAR(255) PRIMARY KEY,
    Email VARCHAR(255) UNIQUE,
    FirstName VARCHAR(255),
    SecondName VARCHAR(255),
    Password VARCHAR(255),
    ProfilePicture VARCHAR(255),
    PhoneNumber VARCHAR(20),
    LineManager BOOLEAN,
    LineManagerID VARCHAR(255),
    TotalHolidays INT
);
CREATE TABLE IF NOT EXISTS pto_requests (
    RequestID VARCHAR(255) PRIMARY KEY,
    UserID VARCHAR(255),
    Start DATE,
    End DATE,
    Status VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES users(UserID)
);

CREATE TABLE IF NOT EXISTS teams (
    TeamID VARCHAR(255) PRIMARY KEY,
    UserID VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES users(UserID)
);