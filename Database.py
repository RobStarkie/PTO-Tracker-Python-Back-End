import mysql.connector

class Database:
  def connectToDB():
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="AquaductStreet9",
    )
    return mydb
  
  def createTables(mydb):
    fd = open('database_create.sql', 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')
    cursor = mydb.cursor()
    for command in sqlCommands:
      cursor.execute(command)
    cursor.execute("SHOW DATABASES")
    for x in cursor:
      print(x)