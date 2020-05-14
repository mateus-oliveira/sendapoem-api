from flask import jsonify
from functools import wraps
from utils.sendemail import *

from database.config import mysql
from controllers.AuthorController import *
from controllers.CommentController import *
from controllers.PoemController import *
from controllers.FollowerController import *

from server import server

import jwt
import datetime


#-----------------------------------------#
#    REQUISIÕES FEITAS À TABELA author    #
#-----------------------------------------#
def sing_in(request): 
    email = request.get_json()['email']
    token_jwt = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=(24*60))}, server.config['JWT'])
    return login(mysql, token_jwt, cod_confirm_email)


def createAuthor(): 
    return create_author(mysql, welcome_email)

def author(request): 
    if request.method == 'GET':
        return find_author(mysql) 

    elif request.method == 'PUT':
        return update_author(mysql)

    else:
        return delete_author(mysql)

def authors(): 
    return list_authors(mysql)

def upload(): 
    return upload_picture(mysql, server)

def get_picture(picture): 
    return get_author_picture(server, picture)


def forgot_password(): 
    return get_forgot_password(mysql, pwd_email)


def resetPassword(): 
    return reset_password(mysql)

def confirmEmail(): 
    return confirm_email(mysql)


#-----------------------------------------#
#     REQUISIÕES FEITAS À TABELA poem     #
#-----------------------------------------#
def feed():
    return feed_poems(mysql)

def poem(): 
    if request.method == 'POST': 
        return create_poem(mysql)

    elif request.method == 'GET':
        return find_poem(mysql) 

    elif request.method == 'PUT':
        return update_poem(mysql)

    else:
        return delete_poem(mysql)

def poems(): 
    return list_poems_by_author(mysql)

def allpoems(): 
    return list_poems(mysql)


#-----------------------------------------#
#   REQUISIÕES FEITAS À TABELA follower   #
#-----------------------------------------#
def follower(): 
    if request.method == 'POST':
        return follow(mysql)

    elif request.method == 'DELETE':
        return unfollow(mysql)
    
    else:
        return get_following(mysql)

def follow_me(): 
    return get_followed(mysql)

#-----------------------------------------#
#    REQUISIÕES FEITAS À TABELA comment   #
#-----------------------------------------#
def comment():
    if request.method == 'POST': 
        return create_comment(mysql)

    elif request.method == 'GET':
        return list_comments(mysql) 

    elif request.method == 'PUT':
        return update_comment(mysql)

    else:
        return delete_comment(mysql)