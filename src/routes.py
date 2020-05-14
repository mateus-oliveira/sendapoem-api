from flask import request

from middlewares.auth import token_required
from server import server
import views

#-----------------------------------------#
#    REQUISIÕES FEITAS À TABELA author    #
#-----------------------------------------#
@server.route('/login', methods=['POST'])
def sing_in(): 
    return views.sing_in(request)

@server.route('/author', methods = ['POST'])
def createAuthor(): 
    return views.createAuthor()

@server.route('/author', methods = ['GET', 'PUT', 'DELETE'])
@token_required
def author(): 
    return views.author(request)

@server.route('/authors', methods = ['GET'])
@token_required
def authors(): 
    return views.authors()

@server.route('/upload', methods = ['PUT'])
@token_required
def upload(): 
    return views.upload()

@server.route('/get_picture/<picture>', methods = ['GET'])
@token_required
def get_picture(picture): 
    return views.get_picture(picture)

@server.route('/author/forgot_password/', methods = ['POST'])
def forgot_password(): 
    return views.forgot_password()

@server.route('/author/reset_password/', methods = ['POST'])
def resetPassword(): 
    return views.resetPassword()

@server.route('/author/confirm_email', methods = ['POST'])
@token_required
def confirmEmail(): 
    return views.confirmEmail()


#-----------------------------------------#
#     REQUISIÕES FEITAS À TABELA poem     #
#-----------------------------------------#
@server.route('/feed', methods = ['GET'])
@token_required
def feed():
    return views.feed()

@server.route('/poem', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def poem(): 
    return views.poem(request)

@server.route('/poems', methods = ['GET'])
@token_required
def poems(): 
    return views.poems()

@server.route('/allpoems', methods = ['GET'])
@token_required
def allpoems(): 
    return views.allpoems()


#-----------------------------------------#
#   REQUISIÕES FEITAS À TABELA follower   #
#-----------------------------------------#
@server.route('/follower', methods = ['GET', 'POST', 'DELETE'])
@token_required
def follower(): 
    return views.follower(request)

@server.route('/follow_me', methods = ['GET'])
@token_required
def follow_me(): 
    return views.follow_me()

#-----------------------------------------#
#    REQUISIÕES FEITAS À TABELA comment   #
#-----------------------------------------#
@server.route('/comment', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def comment():
    return views.comment(request)


if __name__ == '__main__':
    server.run(debug=True)