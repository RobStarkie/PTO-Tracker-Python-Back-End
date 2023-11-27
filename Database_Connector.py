import mysql.connector

class Database_Connector:
    def __init__(self):
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="YourPasswordHere",
          database = "PTO_DATABASE"
        )
