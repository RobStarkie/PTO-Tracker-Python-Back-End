from flask import Flask
app = Flask(__name__)
from Database import *

mydb = Database.connectToDB()
Database.createTables(mydb)