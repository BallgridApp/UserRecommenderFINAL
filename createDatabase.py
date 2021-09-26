import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="myusername",
  password="suckmeeecock"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")