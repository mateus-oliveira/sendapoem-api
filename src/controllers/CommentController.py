from flask import request, jsonify


def create_comment(mysql):
    id_author = request.headers['id_author']
    id_poem = request.headers['id_poem']
    message = request.form.get('title')
    
    sql = mysql.connection.cursor()

    sql.execute('''
        insert into comment (id_author, id_poem, message) 
        values ({}, {}, "{}") 
    '''.format(id_author, id_poem, message))
    sql.execute('''
        select * from comment where id_author = {} and id_poem = {}
    '''.format(id_author, id_poem))

    response = sql.fetchall()

    mysql.connection.commit()

    return jsonify({'comment': response[0]}), 200

def update_comment(mysql):
    id_comment = int(request.headers['id'])
    id_author = int(request.headers['id_author'])
    message = request.form.get('message')

    sql = mysql.connection.cursor()

    sql.execute('select * from comment where id = {}'.format(id_comment))
    response = sql.fetchall()

    if response[0]['id_author'] != id_author:
        return jsonify({'error': "Do you can't change this comment."})

    sql.execute('''
        update comment
        set message = "{}"
        where id = {}
    '''.format(message, id_comment))
    sql.execute('select * from comment where id = {}'.format(id_comment))
    
    response = sql.fetchall()

    mysql.connection.commit()

    return jsonify({'comment': response[0]}), 200

def delete_comment(mysql):   
    id_comment = request.headers['id']

    sql = mysql.connection.cursor()

    sql.execute('delete from comment where id = {}'.format(id_comment))

    mysql.connection.commit()

    return jsonify({'removed': True}), 200

def list_comments(mysql):
    sql = mysql.connection.cursor()

    id_poem = request.headers['id']

    sql.execute('select * from comment where id_poem = {}'.format(id_poem))

    response = sql.fetchall()

    mysql.connection.commit()

    return jsonify({'comments': response}), 200