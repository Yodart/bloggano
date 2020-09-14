from flask import Flask, Blueprint, request, jsonify, make_response, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from db import db_connect
import datetime
import jwt
import sys

auth = Blueprint('auth', __name__)


def require_auth_token(f):
    @wraps(f)
    @db_connect
    def decorated(db_cursor, db_connection, *args, **kwargs):
        token = None
        user = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'error': 'Missing auth token'}), 401
        try:
            data = jwt.decode(token, 'secret')
            db_cursor.execute(
                "SELECT id,name,last_name,user_number,balance FROM users WHERE user_number=%s", ([data['user_number']]))
            user_data = db_cursor.fetchall()[0]
            user = {'id': user_data[0],
                    'name': user_data[1],
                    'last_name': user_data[2],
                    'user_number': user_data[3],
                    'balance': user_data[4]}
        except:
            return jsonify({'error': 'Invalid auth token.'}), 401
        return f(user, *args, **kwargs)
    return decorated


@auth.route('/login')
@db_connect
def login(db_cursor, db_connection):
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    try:
        db_cursor.execute(
            "SELECT id,name,last_name,user_number,balance,password FROM users WHERE user_number=%s", ([auth.username]))
        user_data = db_cursor.fetchall()[0]
        user = {'id': user_data[0],
                'name': user_data[1],
                'last_name': user_data[2],
                'user_number': user_data[3],
                'balance': user_data[4],
                'password': user_data[5]}

        if check_password_hash(user['password'], auth.password):
            token = jwt.encode(
                {'user_number': user['user_number'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)}, 'secret')
            return jsonify({'token': token.decode('UTF-8')}), 200

        return {'message': "Wrong Password"}, 401
    except:
        return {'error': "Unable to find user", "traceback": str(sys.exc_info())}, 401
