
import mysql.connector

mysql = mysql.connector.connect(
    user='root', 
    password='Mateus@2020',
    host='localhost',
    database='sendapoem',
    port="3306",
    auth_plugin='mysql_native_password',
)