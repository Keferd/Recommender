from . import dbservice
from recapp import app, db
# Подключаем библиотеку для "рендеринга" html-шаблонов из папки templates
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for
import functools

import json








@app.route('/notfound')
def not_found_html():
    return render_template('404.html', title='404', err={ 'error': 'Not found', 'code': 404 })

def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))

def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)

def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)

