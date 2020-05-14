import os
from flask import Flask

server = Flask(__name__)

# upload conditions
dirname = os.path.abspath(os.path.dirname(__file__))
server.config['UPLOAD_FOLDER'] = os.path.join(dirname, '..', '..', 'uploads')
server.config['MAX_CONTENT_PATH'] = 2 * 1024**2
server.config['ALLOWED_EXTENSIONS'] = ('png', 'jpg', 'jpeg', 'gif')

# JSON web token
server.config['JWT'] = 'sendapoem'