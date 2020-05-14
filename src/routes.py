from flask import request

from .controllers.AuthorController import *
from .controllers.CommentController import *
from .controllers.PoemController import *
from .controllers.FollowerController import *

from .server import server
from .middlewares.auth import token_required

import jwt
import datetime


#-----------------------------------------#
#    REQUISIÕES FEITAS À TABELA author    #
#-----------------------------------------#
@server.route('/login', methods=['POST'])
def sing_in(): 
    email = request.get_json()['email']
    token_jwt = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=(24*60))}, server.config['JWT'])
    return login(token_jwt)

@server.route('/author', methods = ['POST'])
def createAuthor():
    return create_author()

@server.route('/author', methods = ['GET', 'PUT', 'DELETE'])
@token_required
def author(): 
    if request.method == 'GET':
        return find_author() 

    elif request.method == 'PUT':
        return update_author()

    else:
        return delete_author()

@server.route('/authors', methods = ['GET'])
@token_required
def authors(): 
    return list_authors()

@server.route('/upload', methods = ['PUT'])
@token_required
def upload(): 
    return upload_picture()

@server.route('/get_picture/<picture>', methods = ['GET'])
@token_required
def get_picture(picture): 
    return get_author_picture(picture)

@server.route('/author/forgot_password/', methods = ['POST'])
def forgot_password(): 
    return get_forgot_password()

@server.route('/author/reset_password/', methods = ['POST'])
def resetPassword(): 
    return reset_password()

@server.route('/author/confirm_email', methods = ['POST'])
@token_required
def confirmEmail(): 
    return confirm_email()


#-----------------------------------------#
#     REQUISIÕES FEITAS À TABELA poem     #
#-----------------------------------------#
@server.route('/feed', methods = ['GET'])
@token_required
def feed():
    return feed_poems()

@server.route('/poem', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def poem(): 
    if request.method == 'POST': 
        return create_poem()

    elif request.method == 'GET':
        return find_poem() 

    elif request.method == 'PUT':
        return update_poem()

    else:
        return delete_poem()

@server.route('/poems', methods = ['GET'])
@token_required
def poems(): 
    return list_poems_by_author()

@server.route('/allpoems', methods = ['GET'])
@token_required
def allpoems(): 
    return list_poems()


#-----------------------------------------#
#   REQUISIÕES FEITAS À TABELA follower   #
#-----------------------------------------#
@server.route('/follower', methods = ['GET', 'POST', 'DELETE'])
@token_required
def follower(): 
    if request.method == 'POST':
        return follow()

    elif request.method == 'DELETE':
        return unfollow()
    
    else:
        return get_following()


@server.route('/follow_me', methods = ['GET'])
@token_required
def follow_me(): 
    return get_followed()

#-----------------------------------------#
#    REQUISIÕES FEITAS À TABELA comment   #
#-----------------------------------------#
@server.route('/comment', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def comment():
    if request.method == 'POST': 
        return create_comment()

    elif request.method == 'GET':
        return list_comments() 

    elif request.method == 'PUT':
        return update_comment()

    else:
        return delete_comment()


if __name__ == '__main__':
    server.run(debug=True)