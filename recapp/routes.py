from . import dbservice
from recapp import app, db
# Подключаем библиотеку для "рендеринга" html-шаблонов из папки templates
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for
import functools

import json










""" ------------------------------- СТРАНИЦЫ ------------------------------- """

# Главная страница
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')










""" ------------------------------- BOOKS ------------------------------- """

# Создание таблицы книг
# @app.route('/api/create_books_table', methods=['POST'])
# def post_books_table():
#     response = dbservice.create_books_table()
#     return json_response(response)

# Обновление количества и средних оценок книг
@app.route('/api/update_books_count_and_average_ratings', methods=['PUT'])
def put_books_count_and_average_ratings():
    response = dbservice.update_books_count_and_average_ratings()
    return json_response(response)

""" --------------- BOOKS FREQUENCY --------------- """

# Подсчёт частоты появления количества оценок у пользователей
@app.route('/api/create_frequency_of_books_table', methods=['POST'])
def post_frequency_of_books_table():
    response = dbservice.create_frequency_of_books_table()
    return json_response(response)

""" ------------------------------- USERS ------------------------------- """

# Создание таблицы пользователей
# @app.route('/api/create_users_table', methods=['POST'])
# def post_users_table():
#     response = dbservice.create_users_table()
#     return json_response(response)

# Обновление количества и средних оценок пользователей
@app.route('/api/update_users_count_and_average_ratings', methods=['PUT'])
def put_users_count_and_average_ratings():
    response = dbservice.update_users_count_and_average_ratings()
    return json_response(response)

""" --------------- USERS FREQUENCY --------------- """

# Подсчёт частоты появления количества оценок у пользователей
@app.route('/api/create_frequency_of_users_table', methods=['POST'])
def post_frequency_of_users_table():
    response = dbservice.create_frequency_of_users_table()
    return json_response(response)

""" ------------------------------- RATINGS ------------------------------- """

# Создание таблицы оценок
# @app.route('/api/create_ratings_table', methods=['POST'])
# def post_ratings_table():
#     response = dbservice.create_ratings_table()
#     return json_response(response)




@app.route('/notfound')
def not_found_html():
    return render_template('404.html', title='404', err={ 'error': 'Not found', 'code': 404 })

def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))

def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)

def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)

