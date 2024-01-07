# Import mysql
import mysql.connector

# Create the connection to mySQl database
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="jackovand27",
  password="Thespace14"  
  )

# open a cursor to the database
conn = mydb.cursor()

# Execute SQL command to create a database 
conn.execute("CREATE DATABASE manage")
