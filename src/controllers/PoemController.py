from flask import request, jsonify


def create_poem(mysql):
    id_author = request.headers['id']
    title = request.get_json()['title']
    body = request.get_json()['body']
    
    sql = mysql.cursor()

    sql.execute('''
        insert into poem (id_author, title, body) 
        values ("{}", "{}", "{}") 
    '''.format(id_author, title, body))
    sql.execute('select * from poem where id_author = "{}" and title = "{}"'.format(id_author, title))

    response = sql.fetchall()[0]

    mysql.commit()

    return jsonify({'poem': response[0]}), 200

def find_poem(mysql):
    id_poem = request.headers['id']

    sql = mysql.cursor()
    sql.execute('select * from poem where id = {}'.format(id_poem))

    response = sql.fetchall()[0]

    mysql.commit()

    return jsonify({'poem': response[0]}), 200

def update_poem(mysql):
    id_poem = int(request.headers['id'])
    id_author = int(request.headers['id_author'])
    title = request.form.get('title')
    body = request.form.get('body')

    sql = mysql.cursor()

    sql.execute('select * from poem where id = {}'.format(id_poem))
    response = sql.fetchall()[0]

    if response[0]['id_author'] != id_author:
        return jsonify({'error': "Do you can't change this poem."})

    sql.execute('''
        update poem
        set title = "{}", body = "{}"
        where id = {}
    '''.format(title, body, id_poem))
    sql.execute('select * from poem where id = {}'.format(id_poem))
    
    response = sql.fetchall()[0]

    mysql.commit()

    return jsonify({'poem': response[0]}), 200

def delete_poem(mysql):   
    id_poem = request.headers['id']

    sql = mysql.cursor()

    sql.execute('delete from comment where id_poem = {}'.format(id_poem))
    sql.execute('delete from poem where id = {}'.format(id_poem))

    mysql.commit()

    return jsonify({'removed': True}), 200

def list_poems(mysql):
    sql = mysql.cursor()

    sql.execute('select * from poem')

    response = sql.fetchall()[0]

    mysql.commit()

    return jsonify({'poems': response}), 200

def list_poems_by_author(mysql):
    sql = mysql.cursor()

    id_author = request.headers['id']

    sql.execute('select * from poem where id = {}'.format(id_author))

    response = sql.fetchall()[0]

    mysql.commit()

    return jsonify({'poems': response}), 200

def feed_poems(mysql):
    id_author = request.headers['id']
    page = request.get_json()['page']
    limit = 10
    offset = (page - 1) * limit

    sql = mysql.cursor()

    sql.execute('''
        select * from follower
        where id_author_following = {}
    '''.format(id_author))
    following = sql.fetchall()[0]

    id_authors = ["id_author = {}".format(id_author)]
    for follower in following:
        id_authors.append("id_author = {}".format(follower['id_author_followed']))

    where = "where {}".format(" or ".join(id_authors))

    sql.execute('''
        select * from poem
        {}
        order by id desc
        limit {} offset {}
    '''.format(where, limit, offset))

    poems = sql.fetchall()[0]

    mysql.commit()

    return jsonify({'poems': poems}), 200