import os
import sys
from datetime import datetime
from random import randint
from flask import request, jsonify, send_from_directory, abort
from werkzeug.utils import secure_filename


def create_author(mysql, welcome_email):
    name = request.get_json()['name']
    email = request.get_json()['email']
    phone = request.get_json()['phone']
    password = request.get_json()['password']
    
    sql = mysql.connection.cursor()
    sql.execute('select * from author where email = "{}"'.format(email))

    response = sql.fetchall()

    if len(response) > 0: 
        return jsonify({'Erro': 'O email já foi usado em outro cadastro.'}), 401

    sql.execute('''
        insert into author (name, email, phone, password) 
        values ("{}", "{}", "{}", "{}") 
    '''.format(name, email, phone, password))
    sql.execute('select * from author where email = "{}"'.format(email))

    response = sql.fetchall()
    response[0]['password'] = None

    mysql.connection.commit()

    welcome_email(email, name)

    return jsonify({'author': response[0]}), 200

def find_author(mysql):
    id_author = request.headers['id']

    sql = mysql.connection.cursor()
    sql.execute('select * from author where id = {}'.format(id_author))

    response = sql.fetchall()
    response[0]['password'] = None

    mysql.connection.commit()

    return jsonify({'author': response[0]}), 200

def update_author(mysql):
    id_author = request.headers['id']
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')

    sql = mysql.connection.cursor()

    sql.execute('''
        update author
        set name = "{}", email = "{}", phone = "{}", password = "{}"
        where id = {}
    '''.format(name, email, phone, password, id_author))

    sql.execute('select * from author where id = {}'.format(id_author))
    
    response = sql.fetchall()
    response[0]['password'] = None

    mysql.connection.commit()

    return jsonify({'author': response[0]}), 200

def delete_author(mysql):   
    id_author = request.headers['id']

    sql = mysql.connection.cursor()

    sql.execute('delete from comment where id_author = {}'.format(id_author))
    sql.execute('delete from poem where id_author = {}'.format(id_author))
    sql.execute('delete from author where id = {}'.format(id_author))

    mysql.connection.commit()

    return jsonify({'removed': True}), 200

def list_authors(mysql):
    sql = mysql.connection.cursor()

    sql.execute('select * from author')

    response = sql.fetchall()

    for author in response:
        author['password'] = None

    mysql.connection.commit()

    return jsonify({'authors': response}), 200

def upload_picture(mysql, server):
    picture = request.files['picture']

    rand_int = randint(10000000000000000, 99999999999999999)

    picture_name = str(rand_int) + picture.filename

    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, '..', '..', 'uploads', secure_filename(picture_name))
    picture.save(path)  
    
    size = os.stat(path).st_size
    if size > (2 * 1024**2):
        os.remove(path) 
        return jsonify({'error': 'File out of size.'}), 400

    ext = picture_name.split('.')
    if ext[len(ext) - 1] not in server.config['ALLOWED_EXTENSIONS']:
        os.remove(path) 
        return jsonify({'error': 'Picture not have a valid extension.'}), 400
    
    id_author = request.headers['id']

    # Atualizando no banco de dados o caminho da foto
    sql = mysql.connection.cursor()
    sql.execute('''
        update author 
        set picture = "/get_picture/{}" 
        where id = {}
    '''.format(picture_name, id_author))
    sql.execute('select * from author where id = {}'.format(id_author))
    
    response = sql.fetchall()
    response[0]['password'] = None

    mysql.connection.commit()

    return jsonify({'author': response[0]}), 200

def get_author_picture(server, picture):
    mimetype = 'image/{}'.format(picture.split('.')[1])

    try:
        return send_from_directory(
            server.config['UPLOAD_FOLDER'], 
            filename=picture, 
            mimetype=mimetype, 
            as_attachment=False,
        )
    except FileNotFoundError:
        abort(404)

def login(mysql, token_jwt, cod_confirm_email):
    email = request.get_json()['email']
    password = request.get_json()['password']

    sql = mysql.connection.cursor()
    sql.execute('''
        select * from author
        where email = '{}' and password = '{}'
    '''.format(email, password))
    
    author = sql.fetchall()

    if not author:
        return jsonify({'error': 'Usuário não encontrado.'})

    if author[0]['status'] == 4:
        token_email = randint(100000, 999999)

        now = datetime.now()
        timestamp = datetime.timestamp(now) + (60*1000 * 60)
        timestamp = datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S.%f')

        sql.execute('''
            select * from code
            where id_author = '{}'
        '''.format(author[0]['id']))
        code = sql.fetchall()

        if code:
            sql.execute('''
                update code 
                set value = "{}", expires = "{}" 
                where id = {}
            '''.format(token_email, timestamp, code[0]['id']))
            code = sql.fetchall()
        else:
            sql.execute('''
                insert into code (id_author, value, expires)
                values ({}, "{}", "{}")
            '''.format(author[0]['id'], token_email, timestamp))
            code = sql.fetchall()

        cod_confirm_email(author[0]['email'], author[0]['name'], token_email)
    
    author[0]['password'] = None

    mysql.connection.commit()

    return jsonify({'author': author[0], 'token': token_jwt.decode('UTF-8')})

def confirm_email(mysql):
    value = request.form.get('value')
    id_author = request.headers['id']

    sql = mysql.connection.cursor()

    sql.execute('''
        select * from code
        where id_author = '{}'
    '''.format(id_author))
    code = sql.fetchall()

    if not code:
        return jsonify({'error': 'Código não encontrado!'}), 400

    sql.execute('delete from code where id_author = {}'.format(id_author))

    sql.execute('''
        update author
        set status = {}
        where id = {}
    '''.format(1, id_author))
    
    sql.execute('select * from author where id = {}'.format(id_author))
    
    author = sql.fetchall()

    author[0]['password'] = None

    mysql.connection.commit()

    return jsonify({'author': author[0]}), 200

def get_forgot_password(mysql, pwd_email):
    email = request.form.get('email')

    sql = mysql.connection.cursor()

    sql.execute('''
        select * from author 
        where email = "{}"
    '''.format(email))

    author = sql.fetchall()

    if not author:
        return jsonify({'error': "Author don't found!"}), 400

    token =  randint(100000, 999999)

    now = datetime.now()
    timestamp = datetime.timestamp(now) + (60*1000 * 60)
    timestamp = datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S.%f')

    sql.execute('''
        select * from code
        where id_author = '{}'
    '''.format(author[0]['id']))
    code = sql.fetchall()

    if code:
        sql.execute('''
            update code 
            set value = "{}", expires = "{}" 
            where id = {}
        '''.format(token, timestamp, code[0]['id']))
        code = sql.fetchall()
    else:
        sql.execute('''
            insert into code (id_author, value, expires)
            values ({}, "{}", "{}")
        '''.format(author[0]['id'], token, timestamp))
        code = sql.fetchall()

        
    pwd_email(author[0]['email'], author[0]['name'], token)

    author[0]['password'] = None

    mysql.connection.commit()

    return jsonify({'password': True}), 200

def reset_password(mysql):
    email = request.get_json()['email']
    password = request.get_json()['password']
    token = request.get_json()['token']

    sql = mysql.connection.cursor()

    sql.execute('''
        select * from author
        where email = '{}'
    '''.format(email))
    
    author = sql.fetchall()

    if not author:
        return jsonify({'error': 'Usuário não encontrado.'})

    sql.execute('''
        select * from code
        where id_author = '{}'
    '''.format(author[0]['id']))
    code = sql.fetchall()

    if not code:
        return jsonify({'error': 'Código não encontrado!'}), 400

    if int(code[0]['value']) != token:
        return jsonify({'error': 'Código incorreto!'}), 400

    now = datetime.now()
    timestamp = datetime.timestamp(now)
    timestamp = datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
    if timestamp > str(code[0]['expires']):
        return jsonify({'error': 'Código expirado!'}), 400

    sql.execute('''
        update author
        set password = "{}"
        where id = {}
    '''.format(password, author[0]['id']))

    sql.execute('delete from code where id_author = {}'.format(author[0]['id']))
    
    mysql.connection.commit()

    return jsonify({'new_password': True}), 204