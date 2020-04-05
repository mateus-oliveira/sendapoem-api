import os
from flask import Flask
from flask_mysqldb import MySQL


server = Flask(__name__)
mysql = MySQL(server)

# database credentials
server.config['MYSQL_USER'] = 'root'
server.config['MYSQL_PASSWORD'] = 'Hubbi@2020'
server.config['MYSQL_HOST'] = 'localhost'
server.config['MYSQL_DB'] = 'sendapoem'
server.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# upload conditions
dirname = os.path.abspath(os.path.dirname(__file__))
server.config['UPLOAD_FOLDER'] = os.path.join(dirname, '..', '..', 'uploads')
server.config['MAX_CONTENT_PATH'] = 2 * 1024**2
server.config['ALLOWED_EXTENSIONS'] = ('png', 'jpg', 'jpeg', 'gif')

# JSON web token
server.config['JWT'] = 'sendapoem'