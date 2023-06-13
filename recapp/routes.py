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










""" ------------------------------- PEARSON CORRELATION ------------------------------- """

# Получение рекомендаций пользователю по коэффициенту корреляции Пирсона
@app.route('/api/create_prediction_Pearson', methods=['POST'])
def post_prediction_Pearson():
    if not request.json or not 'id' in request.json or not 'count_rating' in request.json or not 'number_of_crossings' in request.json or not 'correlation' in request.json or not 'normalization_number' in request.json or not 'count_of_output' in request.json:
        return bad_request()
    else:
        response = dbservice.create_prediction_Pearson(request.json['id'],request.json['count_rating'],request.json['number_of_crossings'],request.json['correlation'],request.json['normalization_number'],request.json['count_of_output'])
        return json_response(response)
    
# Funk SVD
@app.route('/api/create_tables_funk_svd', methods=['POST'])
def post_tables_funk_svd():
    if not request.json or not 'factors' in request.json or not 'learning_rate' in request.json or not 'regularization' in request.json or not 'gradient_count' in request.json:
        return bad_request()
    else:
        response = dbservice.create_tables_funk_svd(request.json['factors'], request.json['learning_rate'], request.json['regularization'], request.json['gradient_count'])
        return json_response(response)

# Рекомендации по Funk SVD
@app.route('/api/create_prediction_Funk_SVD', methods=['POST'])
def post_prediction_Funk_SVD():
    if not request.json or not 'id' in request.json or not 'count_of_output' in request.json:
        return bad_request()
    else:
        response = dbservice.create_prediction_Funk_SVD(request.json['id'], request.json['count_of_output'])
        return json_response(response)

# Тестирование рекомендаций по коэффициенту корреляции Пирсона
@app.route('/api/testing_prediction_Pearson', methods=['POST'])
def post_testing_prediction_Pearson():
    if not request.json or not 'count_rating' in request.json or not 'number_of_crossings' in request.json or not 'correlation' in request.json or not 'normalization_number' in request.json or not 'percentage_tested_users' in request.json or not 'percentage_tested_ratings' in request.json:
        return bad_request()
    else:
        response = dbservice.testing_prediction_Pearson(request.json['count_rating'],request.json['number_of_crossings'],request.json['correlation'],request.json['normalization_number'],request.json['percentage_tested_users'],request.json['percentage_tested_ratings'])
        return json_response(response)

# Тестирование рекомендаций по Funk SVD
@app.route('/api/testing_prediction_Funk_SVD', methods=['POST'])
def post_testing_prediction_Funk_SVD():
    if not request.json or not 'factors' in request.json or not 'learning_rate' in request.json or not 'regularization' in request.json or not 'gradient_count' in request.json or not 'percentage_tested_ratings' in request.json:
        return bad_request()
    else:
        response = dbservice.testing_prediction_Funk_SVD(request.json['factors'], request.json['learning_rate'], request.json['regularization'], request.json['gradient_count'], request.json['percentage_tested_ratings'])
        return json_response(response)








@app.route('/notfound')
def not_found_html():
    return render_template('404.html', title='404', err={ 'error': 'Not found', 'code': 404 })

def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))

def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)

def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)

