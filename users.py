from flask import Flask, Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_connect
from auth import require_auth_token
import datetime
import jwt
import psycopg2
import sys

users = Blueprint('users', __name__)


@ users.route('/user', methods=['POST'])
@db_connect
def create_user(db_cursor, db_connection):
    hashed_password = generate_password_hash(
        request.json['password'], method='sha256')
    username = request.json['username']
    try:
        db_cursor.execute(
            "SELECT username,password FROM users WHERE username=%s", ([username]))
        user_data = db_cursor.fetchall()[0]
        return jsonify({'error': 'username taken.'}), 401
    except:
        try:
            db_cursor.execute(
                "INSERT INTO users (username,password) values(%s,%s)", (username, hashed_password))
            db_connection.commit()
            return jsonify({'message': 'user Created!'}), 200
        except:
            return {'error': "Unable to create user", "traceback": str(sys.exc_info())}, 401


@ users.route('/user/<int:user_id>', methods=['GET'])
@db_connect
@require_auth_token
def query_single_user(current_user, db_cursor, db_connection, user_id):
    if current_user['id'] != user_id:
        return jsonify({"error": "Sensity user data, please log into the user"}), 401
    try:
        db_cursor.execute(
            "SELECT id,name,last_name,user_number,balance FROM users WHERE user_number=%s", ([user_id]))
        user_data = db_cursor.fetchall()[0]
        return {'id': user_data[0],
                'name': user_data[1],
                'last_name': user_data[2],
                'user_number': user_data[3],
                'balance': user_data[4]}, 200
    except:
        return {'error': "Unable to fetch /user/<id>", "traceback": str(sys.exc_info())}, 401


@ users.route('/user/<int:acc_number>', methods=['PUT'])
@db_connect
@require_auth_token
def edit_user(current_user, db_cursor, db_connection, acc_number):
    if current_user['user_number'] != acc_number:
        return jsonify({"error": "Sensity user data, please log into the user"}), 401
    try:
        user = {'name': request.json['name'] if 'name' in request.json else current_user['name'],
                'last_name': request.json['last_name'] if 'last_name' in request.json else current_user['last_name'],
                }
        db_cursor.execute(
            "UPDATE users SET name = %s , last_name = %s WHERE user_number = %s", (user['name'], user['last_name'], acc_number))
        db_connection.commit()
        return {'response': 'User was edited'}, 200
    except:
        return {'error': "Unable to edit user", "traceback": str(sys.exc_info())}, 401


@ users.route('/user/<int:acc_number>', methods=['DELETE'])
@db_connect
@require_auth_token
def delete_user(current_user, db_cursor, db_connection, acc_number):
    if current_user['user_number'] != acc_number:
        return jsonify({"error": "Sensity user data, please log into the user"}), 401
    try:
        db_cursor.execute(
            "DELETE FROM users WHERE user_number = %s", ([acc_number]))
        db_connection.commit()
        return {'response': 'User deleted'}, 200
    except:
        return {'error': "Unable to delete user", "traceback": str(sys.exc_info())}


@ users.route('/users', methods=['GET'])
@db_connect
@require_auth_token
def get_users(current_user, db_cursor, db_connection):
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    try:
        db_cursor.execute(
            "SELECT name,last_name,user_number,created_at,balance FROM users ORDER BY created_at LIMIT %s OFFSET %s", (limit, offset))
        users = []
        for user in db_cursor.fetchall():
            users.append({'id': user[0],
                          'name': user[1],
                          'last_name': user[2],
                          'user_number': user[3],
                          'balance': user[4]})
        return jsonify({'users': users})
    except:
        return {'error': "Unable to fetch all users", "traceback": str(sys.exc_info())}
