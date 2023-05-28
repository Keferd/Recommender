import os
from datetime import timedelta


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), "recommender_books.sqlite")}'
    # Отключение кэширования в браузере (закомментировать при релизе!)
    SEND_FILE_MAX_AGE_DEFAULT = 0
    # Параметры сессии
    SECRET_KEY = 'anypassword'
    SESSION_COOKIE_NAME = 'user_sid'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)