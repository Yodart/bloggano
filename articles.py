from flask import Flask, Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_connect
from auth import require_auth_token
import datetime
import jwt
import psycopg2
import sys

articles = Blueprint('articles', __name__)


@ articles.route('/article', methods=['POST'])
@db_connect
@require_auth_token
def create_article(current_account, db_cursor, db_connection):
    creator = current_account['username']
    ammount = request.json['ammount']
    try:
        db_cursor.execute(
            "INSERT INTO articles (ammount,account_number) values(%s,%s)", (ammount, account_number))
        db_cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (ammount, account_number))
        db_connection.commit()
        return jsonify({'message': 'Ammounted articleed!'}), 200
    except:
        return {'error': "Unable to make article", "traceback": str(sys.exc_info())}, 401


@ articles.route('/article/<int:article_id>', methods=['GET'])
@db_connect
@require_auth_token
def query_single_article(current_account, db_cursor, db_connection, article_id):
    try:
        db_cursor.execute(
            "SELECT id,account_number,ammount,timestamp FROM articles WHERE id=%s AND account_number = %s LIMIT 1", (article_id, current_account['account_number']))
        account_data = db_cursor.fetchall()[0]
        return {'id': account_data[0],
                'account_number': account_data[1],
                'ammount': account_data[2],
                'timestamp': account_data[3]}, 200
    except:
        return {'error': "Unable to fetch /article/<id>", "traceback": str(sys.exc_info())}, 401


@ articles.route('/articles/<int:acc_number>', methods=['GET'])
@db_connect
@require_auth_token
def query_articles(current_account, db_cursor, db_connection, acc_number):
    if current_account['account_number'] != acc_number:
        return jsonify({"error": "Sensity user data, please log into the account"}), 401
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    try:
        db_cursor.execute(
            "SELECT id,account_number,ammount,timestamp FROM articles WHERE account_number = %s LIMIT %s OFFSET %s", (acc_number, limit, offset))
        articles = []
        for article in db_cursor.fetchall():
            articles.append({'id': article[0],
                             'account_number': article[1],
                             'ammount': article[2],
                             'timestamp': article[3]})
        return jsonify({'articles': articles}), 200
    except:
        return {'error': "Unable to fetch /articles/<acc_number>", "traceback": str(sys.exc_info())}, 401
