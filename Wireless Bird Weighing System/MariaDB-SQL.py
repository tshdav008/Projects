import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="bird"
)

mycursor = mydb.cursor()

sql = "INSERT INTO bird (id, weight) VALUES (%s, %s)"
val = ("John", 220)
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
