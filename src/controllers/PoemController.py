from flask import request, jsonify


def create_poem(mysql):
    id_author = request.headers['id']
    title = request.form.get('title')
    body = request.form.get('body')
    
    sql = mysql.connection.cursor()

    sql.execute('''
        insert into poem (id_author, title, body) 
        values ("{}", "{}", "{}") 
    '''.format(id_author, title, body))
    sql.execute('select * from poem where id_author = "{}" and title = "{}"'.format(id_author, title))

    response = sql.fetchall()

    mysql.connection.commit()

    return jsonify({'poem': response[0]}), 200

def find_poem(mysql):
    id_poem = request.headers['id']

    sql = mysql.connection.cursor()
    sql.execute('select * from poem where id = {}'.format(id_poem))

    response = sql.fetchall()

    mysql.connection.commit()

    return jsonify({'poem': response[0]}), 200

def update_poem(mysql):
    id_poem = int(request.headers['id'])
    id_author = int(request.headers['id_author'])
    title = request.form.get('title')
    body = request.form.get('body')

    sql = mysql.connection.cursor()

    sql.execute('select * from poem where id = {}'.format(id_poem))
    response = sql.fetchall()

    if response[0]['id_author'] != id_author:
        return jsonify({'error': "Do you can't change this poem."})

    sql.execute('''
        update poem
        set title = "{}", body = "{}"
        where id = {}
    '''.format(title, body, id_poem))
    sql.execute('select * from poem where id = {}'.format(id_poem))
    
    response = sql.fetchall()

    mysql.connection.commit()

    return jsonify({'poem': response[0]}), 200

def delete_poem(mysql):   
    id_poem = request.headers['id']

    sql = mysql.connection.cursor()

    sql.execute('delete from comment where id_poem = {}'.format(id_poem))
    sql.execute('delete from poem where id = {}'.format(id_poem))

    mysql.connection.commit()

    return jsonify({'removed': True}), 200

def list_poems(mysql):
    sql = mysql.connection.cursor()

    sql.execute('select * from poem')

    response = sql.fetchall()

    mysql.connection.commit()

    return jsonify({'poems': response}), 200

def list_poems_by_author(mysql):
    sql = mysql.connection.cursor()

    id_author = request.headers['id']

    sql.execute('select * from poem where id = {}'.format(id_author))

    response = sql.fetchall()

    mysql.connection.commit()

    return jsonify({'poems': response}), 200