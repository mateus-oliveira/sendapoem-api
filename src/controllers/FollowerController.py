from flask import request, jsonify

from server import server
from utils.sendemail import *
from database.config import mysql

def follow(mysql):
    id_author_following = request.headers['id_following']
    id_author_followed = request.get_json()['id_followed']
    
    sql = mysql.cursor()

    sql.execute('''
        select * from follower
        where id_author_following = {}
    '''.format(id_author_following))

    followers = sql.fetchall()[0]

    if len(followers) >= 7500:
        return jsonify({'error': 'You are followed 7500 authors.'}), 400

    sql.execute('''
        insert into follower (id_author_following, id_author_followed) 
        values ({}, {}) 
    '''.format(id_author_following, id_author_followed))

    mysql.commit()

    return jsonify({'follow': True}), 200

def unfollow(mysql):
    id_author_following = request.headers['id_following']
    id_author_followed = request.get_json()['id_followed']
    
    sql = mysql.cursor()
    sql.execute('''
        delete from follower 
        where id_author_following = {} and id_author_followed = {}
    '''.format(id_author_following, id_author_followed))

    mysql.commit()

    return jsonify({'unfollow': True}), 200

def get_followed(mysql):
    id_author_followed = request.headers['id']
    
    sql = mysql.cursor()
    sql.execute('''
        select * from follower
        where id_author_followed = {}
    '''.format(id_author_followed))

    response = sql.fetchall()[0]

    mysql.commit()

    return jsonify({'followers': response}), 200

def get_following(mysql):
    id_author_following = request.headers['id']
    
    sql = mysql.cursor()
    sql.execute('''
        select * from follower
        where id_author_following = {}
    '''.format(id_author_following))

    response = sql.fetchall()[0]

    mysql.commit()

    return jsonify({'followers': response}), 200