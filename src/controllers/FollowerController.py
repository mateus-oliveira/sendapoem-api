from flask import request, jsonify


def follow(mysql):
    id_author_following = request.headers['id_following']
    id_author_followed = request.get_json()['id_followed']
    
    sql = mysql.connection.cursor()

    sql.execute('''
        select * from follower
        where id_author_following = {}
    '''.format(id_author_following))

    followers = sql.fetchall()

    if len(followers) >= 7500:
        return jsonify({'error': 'You are followed 7500 authors.'}), 400

    sql.execute('''
        insert into follower (id_author_following, id_author_followed) 
        values ({}, {}) 
    '''.format(id_author_following, id_author_followed))

    mysql.connection.commit()

    return jsonify({'follow': True}), 200

def unfollow(mysql):
    id_author_following = request.headers['id_following']
    id_author_followed = request.get_json()['id_followed']
    
    sql = mysql.connection.cursor()
    sql.execute('''
        delete from follower 
        where id_author_following = {} and id_author_followed = {}
    '''.format(id_author_following, id_author_followed))

    mysql.connection.commit()

    return jsonify({'unfollow': True}), 200

def get_followed(mysql):
    id_author_followed = request.headers['id']
    
    sql = mysql.connection.cursor()
    sql.execute('''
        select * from follower
        where id_author_followed = {}
    '''.format(id_author_followed))

    response = sql.fetchall()

    mysql.connection.commit()

    return jsonify({'followers': response}), 200

def get_following(mysql):
    id_author_following = request.headers['id']
    
    sql = mysql.connection.cursor()
    sql.execute('''
        select * from follower
        where id_author_following = {}
    '''.format(id_author_following))

    response = sql.fetchall()

    mysql.connection.commit()

    return jsonify({'followers': response}), 200