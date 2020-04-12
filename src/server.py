from flask import request, jsonify
from functools import wraps
from werkzeug.utils import secure_filename
from utils.sendemail import *

from config.config import mysql, server
from controllers.AuthorController import *
from controllers.CommentController import *
from controllers.PoemController import *
from controllers.FollowerController import *

import jwt
import datetime 


# BODY_FORM = request.form.get('value')
# BODY_JSON = request.get_json()
# FILES = request.files['file']
# HEADER = request.headers['value']
# QUERY = request.args.get('value')


#-----------------------------------------#
#       AUTENTICAÇÃO JSON WEB TOKEN       #
#-----------------------------------------#
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'error': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, server.config['JWT'])
        except:
            return jsonify({'error': 'Token is invalid!'}), 403

        return f(*args, *kwargs)
    
    return decorated


#-----------------------------------------#
#    REQUISIÕES FEITAS À TABELA author    #
#-----------------------------------------#
@server.route('/login', methods=['POST'])
def sing_in(): 
    email = request.get_json()['email']
    token_jwt = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=(24*60))}, server.config['JWT'])
    return login(mysql, token_jwt, cod_confirm_email)

@server.route('/author', methods = ['POST'])
def createAuthor(): 
    return create_author(mysql, welcome_email)

@server.route('/author', methods = ['GET', 'PUT', 'DELETE'])
@token_required
def author(): 
    if request.method == 'GET':
        return find_author(mysql) 

    elif request.method == 'PUT':
        return update_author(mysql)

    else:
        return delete_author(mysql)

@server.route('/authors', methods = ['GET'])
@token_required
def authors(): 
    return list_authors(mysql)

@server.route('/upload', methods = ['PUT'])
@token_required
def upload(): 
    return upload_picture(mysql, server)

@server.route('/get_picture/<picture>', methods = ['GET'])
@token_required
def get_picture(picture): 
    return get_author_picture(server, picture)

@server.route('/author/forgot_password/', methods = ['POST'])
def forgot_password(): 
    return get_forgot_password(mysql, pwd_email)

@server.route('/author/reset_password/', methods = ['POST'])
def resetPassword(): 
    return reset_password(mysql)

@server.route('/author/confirm_email', methods = ['POST'])
@token_required
def confirmEmail(): 
    return confirm_email(mysql)


#-----------------------------------------#
#     REQUISIÕES FEITAS À TABELA poem     #
#-----------------------------------------#
@server.route('/feed', methods = ['GET'])
@token_required
def feed():
    return feed_poems(mysql)

@server.route('/poem', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def poem(): 
    if request.method == 'POST': 
        return create_poem(mysql)

    elif request.method == 'GET':
        return find_poem(mysql) 

    elif request.method == 'PUT':
        return update_poem(mysql)

    else:
        return delete_poem(mysql)

@server.route('/poems', methods = ['GET'])
@token_required
def poems(): 
    return list_poems_by_author(mysql)

@server.route('/allpoems', methods = ['GET'])
@token_required
def allpoems(): 
    return list_poems(mysql)


#-----------------------------------------#
#   REQUISIÕES FEITAS À TABELA follower   #
#-----------------------------------------#
@server.route('/follower', methods = ['GET', 'POST', 'DELETE'])
@token_required
def follower(): 
    if request.method == 'POST':
        return follow(mysql)

    elif request.method == 'DELETE':
        return unfollow(mysql)
    
    else:
        return get_following(mysql)

@server.route('/follow_me', methods = ['GET'])
@token_required
def follow_me(): 
    return get_followed(mysql)

#-----------------------------------------#
#    REQUISIÕES FEITAS À TABELA comment   #
#-----------------------------------------#
@server.route('/comment', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def comment():
    if request.method == 'POST': 
        return create_comment(mysql)

    elif request.method == 'GET':
        return list_comments(mysql) 

    elif request.method == 'PUT':
        return update_comment(mysql)

    else:
        return delete_comment(mysql)


if __name__ == '__main__':
    server.run(debug=True)