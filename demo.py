def fun():
    return [1, 2, 3], 2


a, b = fun()
print(a)

# import mysql.connector

# mydb = mysql.connector.connect(host='localhost',
#                                user='root',
#                                passwd='123456',
#                                database='classInfomation')

# mycursor = mydb.cursor()
# #mycursor.execute("CREATE DATABASE runoob_db")
# mycursor.execute("CREATE TABLE sites (name VARCHAR(255), url VARCHAR(255))")

# for x in mycursor:
#     print(x)