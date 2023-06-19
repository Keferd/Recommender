from sqlalchemy import true
from recapp import db
from datetime import datetime
from flask import session, make_response, redirect, url_for, jsonify
import bcrypt
import random
import statistics
import math
from . import svd

import sqlite3;
 









""" ------------------------------- BOOKS ------------------------------- """

# Создание таблицы книг
# def create_books_table():
#     rows = db.session.execute("SELECT * FROM books_csv").fetchall()
#     try:
#         con = sqlite3.connect("recommender_books.sqlite")
#         cursor = con.cursor()

#         query = "INSERT INTO books (id,authors, original_publication_year, original_title, title, average_rating, image_url, small_image_url) VALUES (?,?,?,?,?,?,?,?)"
#         cursor.executemany(query, rows)
#         con.commit()

#         return {'message': "Books Table Created!"}
#     except Exception as e:
#         db.session.rollback()
#         return {'message': str(e)}

# Обновление количества и средних оценок книг
def update_books_count_and_average_ratings():
    rows_books = db.session.execute("SELECT id FROM books").fetchall()
    try:
        con = sqlite3.connect("recommender_books.sqlite")
        cursor = con.cursor()

        newrows = []

        for book_id in rows_books:
            rows_ratings = db.session.execute(f"SELECT rating FROM ratings WHERE book_id='{book_id[0]}'").fetchall()
            amount = 0
            sum = 0
            for rating in rows_ratings:
                amount = amount + 1
                sum = sum + rating[0]
            average = 0
            if amount > 0:
                average = round(sum/amount,2)
            newrows.append((average, amount, book_id[0]))

        query = "UPDATE books SET average_rating = ?, count_rating = ? WHERE id = ?"
        cursor.executemany(query, newrows)
        con.commit()

        return {'message': "Books count and average ratings UPDATED!"}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}





""" --------------- BOOKS FREQUENCY --------------- """

# Подсчёт частоты появления количества оценок у книг
def create_frequency_of_books_table():
    rows_books = db.session.execute("SELECT count_rating FROM books").fetchall()
    try:
        con = sqlite3.connect("recommender_books.sqlite")
        cursor = con.cursor()

        frequency_dict = {}

        for item in rows_books:
            item_value = item[0]
            if item_value not in frequency_dict:
                frequency_dict[item_value] = 1
            else:
                frequency_dict[item_value] += 1

        frequency_rows_existed = db.session.execute("SELECT number_of_ratings FROM frequency_of_books").fetchall()

        frequency_list_existed = []
        for item in frequency_rows_existed:
            frequency_list_existed.append(item[0])
        
        frequency_list_insert = []
        frequency_list_update = []

        for number in frequency_dict:
            if number in frequency_list_existed:
                frequency_list_update.append((frequency_dict[number], number))
            else:
                frequency_list_insert.append((number, frequency_dict[number]))

        query = "INSERT INTO frequency_of_books (number_of_ratings, occurrence_frequency) VALUES (?, ?)"
        cursor.executemany(query, frequency_list_insert)
        con.commit()

        query = "UPDATE frequency_of_books SET occurrence_frequency = ? WHERE number_of_ratings = ?"
        cursor.executemany(query, frequency_list_update)
        con.commit()

        cumulative_message = update_cumulative_frequency_of_books()

        return {'message': "Frequency of books table CREATED!" + " + " + cumulative_message['message']}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}

# Подсчёт накопительной частоты появления количества оценок у книг
def update_cumulative_frequency_of_books():
    rows_frequency = db.session.execute("SELECT number_of_ratings, occurrence_frequency FROM frequency_of_books ORDER BY number_of_ratings DESC").fetchall()
    try:
        con = sqlite3.connect("recommender_books.sqlite")
        cursor = con.cursor()

        cumulative_rows = []

        cumulative_sum = 0

        for item in rows_frequency:
            cumulative_sum += item[1]
            cumulative_rows.append((cumulative_sum, item[0]))

        query = "UPDATE frequency_of_books SET cumulative_frequency = ? WHERE number_of_ratings = ?"
        cursor.executemany(query, cumulative_rows)
        con.commit()

        return {'message': "Cumulative_frequency of frequency_of_books table UPDATED!"}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}









""" ------------------------------- USERS ------------------------------- """
    
# Создание таблицы пользователей
# def create_users_table():
#     try:
#         con = sqlite3.connect("recommender_books.sqlite")
#         cursor = con.cursor()

#         rows = []

#         for i in range(1,53425):
#             rows.append((i,))

#         query = "INSERT INTO users (id) VALUES (?)"
#         cursor.executemany(query, rows)
#         con.commit()

#         return {'message': "Users Table Created!"}
#     except Exception as e:
#         db.session.rollback()
#         return {'message': str(e)}

# Обновление количества и средних оценок пользователей
def update_users_count_and_average_ratings():
    rows_users = db.session.execute("SELECT id FROM users").fetchall()
    try:
        con = sqlite3.connect("recommender_books.sqlite")
        cursor = con.cursor()

        newrows = []
        
        query = "UPDATE users SET average_rating = ?, count_rating = ? WHERE id = ?"

        for user_id in rows_users:
            rows_ratings = db.session.execute(f"SELECT rating FROM ratings WHERE user_id='{user_id[0]}'").fetchall()
            amount = 0
            sum = 0
            for rating in rows_ratings:
                amount = amount + 1
                sum = sum + rating[0]
            average = 0
            if amount > 0:
                average = round(sum/amount,2)
            newrows.append((average, amount, user_id[0]))
        
        cursor.executemany(query, newrows)
        con.commit()

        return {'message': "Books count and average ratings UPDATED!"}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}
    



    
""" --------------- USERS FREQUENCY --------------- """

# Подсчёт частоты появления количества оценок у пользователей
def create_frequency_of_users_table():
    rows_users = db.session.execute("SELECT count_rating FROM users").fetchall()
    try:
        con = sqlite3.connect("recommender_books.sqlite")
        cursor = con.cursor()

        frequency_dict = {}

        for item in rows_users:
            item_value = item[0]
            if item_value not in frequency_dict:
                frequency_dict[item_value] = 1
            else:
                frequency_dict[item_value] += 1

        frequency_rows_existed = db.session.execute("SELECT number_of_ratings FROM frequency_of_users").fetchall()

        frequency_list_existed = []
        for item in frequency_rows_existed:
            frequency_list_existed.append(item[0])
        
        frequency_list_insert = []
        frequency_list_update = []

        for number in frequency_dict:
            if number in frequency_list_existed:
                frequency_list_update.append((frequency_dict[number], number))
            else:
                frequency_list_insert.append((number, frequency_dict[number]))

        query = "INSERT INTO frequency_of_users (number_of_ratings, occurrence_frequency) VALUES (?, ?)"
        cursor.executemany(query, frequency_list_insert)
        con.commit()

        query = "UPDATE frequency_of_users SET occurrence_frequency = ? WHERE number_of_ratings = ?"
        cursor.executemany(query, frequency_list_update)
        con.commit()

        cumulative_message = update_cumulative_frequency_of_users()

        return {'message': "Frequency of users table CREATED!" + " + " + cumulative_message['message']}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}

# Подсчёт накопительной частоты появления количества оценок у пользователей
def update_cumulative_frequency_of_users():
    rows_frequency = db.session.execute("SELECT number_of_ratings, occurrence_frequency FROM frequency_of_users ORDER BY number_of_ratings DESC").fetchall()
    try:
        con = sqlite3.connect("recommender_books.sqlite")
        cursor = con.cursor()

        cumulative_rows = []

        cumulative_sum = 0

        for item in rows_frequency:
            cumulative_sum += item[1]
            cumulative_rows.append((cumulative_sum, item[0]))

        query = "UPDATE frequency_of_users SET cumulative_frequency = ? WHERE number_of_ratings = ?"
        cursor.executemany(query, cumulative_rows)
        con.commit()

        return {'message': "Cumulative_frequency of frequency_of_users table UPDATED!"}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}






""" ------------------------------- RATINGS ------------------------------- """

# Создание таблицы оценок
# def create_ratings_table():
#     try:
#         con = sqlite3.connect("recommender_books.sqlite")
#         cursor = con.cursor()

#         newrows = []

#         for k in range(1,10001):
#             rows = db.session.execute(f"SELECT * FROM ratings_csv WHERE book_id='{k}'").fetchall()
#             for i in range(len(rows)): 
#                 check = True
#                 for j in range(0,i):
#                     if rows[i][1] == rows[j][1]:
#                         check = False
#                         break
#                 if check == True:
#                     newrows.append(rows[i])
#             print(k)
        
#         query = "INSERT INTO ratings (book_id, user_id, rating) VALUES (?,?,?)"
#         cursor.executemany(query, newrows)
#         con.commit()

#         return {'message': "Ratings Table Created!"}
#     except Exception as e:
#         db.session.rollback()
#         return {'message': str(e)}











""" ------------------------------- PEARSON CORRELATION ------------------------------- """

# Получение рекомендаций пользователю по коэффициенту корреляции Пирсона
def create_prediction_Pearson(id, count_of_output):
    try:
        if(int(count_of_output) > 0):
            id = int(id)
            rows_ratings = db.session.execute(f"SELECT * FROM ratings").fetchall()

            # Нахождение глобального среднего по обучающим данным 
            r_m = []
            for item in rows_ratings:
                r_m.append(item[2])
            global_mean = statistics.mean(r_m)

            ratings_dict = {}
            for item in rows_ratings:
                book_id = item[0]
                user_id = item[1]
                rating = item[2]

                if user_id not in ratings_dict:
                    ratings_dict[user_id] = {}
                    ratings_dict[user_id][book_id] = rating
                else:
                    ratings_dict[user_id][book_id] = rating

            ratings_dict_rev = {}
            for item in rows_ratings:
                book_id = item[0]
                user_id = item[1]
                rating = item[2]

                if book_id not in ratings_dict_rev:
                    ratings_dict_rev[book_id] = {}
                    ratings_dict_rev[book_id][user_id] = rating
                else:
                    ratings_dict_rev[book_id][user_id] = rating

        
            predictions = svd.pearson_correlation_prediction(ratings_dict_rev, svd.pearson_correlation(ratings_dict, id, global_mean), id)

            predictions_rows = []

            for book_id in predictions:
                predictions_rows.append((id ,book_id, predictions[book_id]))

            con = sqlite3.connect("recommender_books.sqlite")
            cursor = con.cursor()

            cursor.execute(f"DELETE FROM recommendations_Pearson WHERE user_id = {id}")
            con.commit()

            query = "INSERT INTO recommendations_Pearson (user_id, book_id, recommendation) VALUES (?, ?, ?)"
            cursor.executemany(query, predictions_rows)
            con.commit()

            rec = db.session.execute(f"SELECT book_id FROM recommendations_Pearson WHERE user_id='{id}' ORDER BY recommendation DESC LIMIT {count_of_output}").fetchall()


            # Составляется единый запрос для всех book_id
            query = "SELECT * FROM books WHERE id IN ("
            for index, item in enumerate(rec):
                if index == len(rec) - 1:
                    query += str(item[0])
                else:
                    query += str(item[0]) + ", "
            query += ")"

            # Получаем все необходимые книги
            cursor.execute(query)
            books = cursor.fetchall()

            result = []
            for row in books:
                dict_item = {}
                for index, value in enumerate(row):
                    dict_item[cursor.description[index][0]] = value
                result.append(dict_item)

            return {'recommendations': result}
        
        else:
            return {'Ошибка': 'Ошибка'}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}














def create_global_mean():
    try:
        rows_ratings = db.session.execute(f"SELECT * FROM ratings").fetchall()

        r_m = []
        for item in rows_ratings:
            r_m.append(item[2])
        global_mean = statistics.mean(r_m)

        return global_mean
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}
    

# Funk SVD
def create_tables_funk_svd(factors, learning_rate, regularization):
    try:
        rows_ratings = db.session.execute(f"SELECT * FROM ratings").fetchall()

        # Нахождение глобального среднего
        r_m = []
        for item in rows_ratings:
            r_m.append(item[2])
        global_mean = statistics.mean(r_m)

        # Константы
        factors = int(factors)
        learning_rate = float(learning_rate)
        regularization = float(regularization)

        global_mean, books_factors, users_factors = svd.funk_svd(rows_ratings, factors, 100, learning_rate, regularization, 0.01)


        # Сохранение полученных таблиц
        con = sqlite3.connect("recommender_books.sqlite")
        cursor = con.cursor()

        query = "DELETE FROM books_factors"
        cursor.execute(query)
        con.commit()

        query = "DELETE FROM users_factors"
        cursor.execute(query)
        con.commit()

        query = "DELETE FROM global_mean"
        cursor.execute(query)
        con.commit()

        books_factors_list = []
        for book_id in books_factors:
            for factor_id in books_factors[book_id]:
                books_factors_list.append((book_id, factor_id, books_factors[book_id][factor_id]))
        query = "INSERT INTO books_factors (book_id, factor_id, value) VALUES (?, ?, ?)"
        cursor.executemany(query, books_factors_list)
        con.commit()
        
        users_factors_list = []
        for user_id in users_factors:
            for factor_id in users_factors[user_id]:
                users_factors_list.append((user_id, factor_id, users_factors[user_id][factor_id]))
        query = "INSERT INTO users_factors (user_id, factor_id, value) VALUES (?, ?, ?)"
        cursor.executemany(query, users_factors_list)
        con.commit()

        cursor.execute(f"INSERT INTO global_mean (value) VALUES ({global_mean})")
        con.commit()


        return {'Генерация матриц': "Матрицы факторов сгенерированы"}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}

def create_prediction_funk_svd(id, count_of_books):
    try:
        if(int(count_of_books) > 0):
            global_mean = db.session.execute(f"SELECT value FROM global_mean").fetchall()
            global_mean = global_mean[0][0]
            books_factors = db.session.execute(f"SELECT * FROM books_factors").fetchall()
            user_factors = db.session.execute(f"SELECT * FROM users_factors WHERE user_id = '{id}'").fetchall()
            if books_factors.__len__() == 0 or user_factors.__len__() == 0:
                return {'Ошибка': 'Нет матриц'}

            books_factors_dict = {}
            for item in books_factors:
                book_id = item[0]
                factor = item[1]
                value = item[2]
                if book_id not in books_factors_dict:
                    books_factors_dict[book_id] = {}
                    books_factors_dict[book_id][factor] = value
                else:
                    books_factors_dict[book_id][factor] = value

            user_factors_dict = {}
            for item in user_factors:
                book_id = item[1]
                value = item[2]
                user_factors_dict[book_id] = value

            predictions = []
            for book_id in books_factors_dict:
                prediction = global_mean
                for factor in books_factors_dict[book_id]:
                    prediction += books_factors_dict[book_id][factor] * user_factors_dict[factor]
                predictions.append((id,book_id,prediction))

            con = sqlite3.connect("recommender_books.sqlite")
            cursor = con.cursor()

            cursor.execute(f"DELETE FROM recommendations_Funk_SVD WHERE user_id = '{id}'")
            con.commit()

            query = "INSERT INTO recommendations_Funk_SVD (user_id, book_id, recommendation) VALUES (?, ?, ?)"
            cursor.executemany(query, predictions)
            con.commit()

            rec = db.session.execute(f"SELECT book_id FROM recommendations_Funk_SVD WHERE user_id='{id}' ORDER BY recommendation DESC LIMIT {count_of_books}").fetchall()

            # Составляется единый запрос для всех book_id
            query = "SELECT * FROM books WHERE id IN ("
            for index, item in enumerate(rec):
                if index == len(rec) - 1:
                    query += str(item[0])
                else:
                    query += str(item[0]) + ", "
            query += ")"

            # Получаем все необходимые книги
            cursor.execute(query)
            books = cursor.fetchall()

            result = []
            for row in books:
                dict_item = {}
                for index, value in enumerate(row):
                    dict_item[cursor.description[index][0]] = value
                result.append(dict_item)

            if result.__len__() > 0:
                return {'recommendations': result}
            else:
                return {'Ошибка': 'Ошибка'}
        else:
            return {'Ошибка': 'Ошибка'}

    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}











# Рекомендации по Funk SVD
# def create_prediction_Funk_SVD(id, count_of_output):
    try:
        user_book_id = db.session.execute(f"SELECT book_id FROM ratings WHERE user_id = '{id}'").fetchall()
        users_p_list = db.session.execute(f"SELECT factor_id, value FROM users_p WHERE user_id = '{id}'").fetchall()
        users_deviation = db.session.execute(f"SELECT deviation FROM users_deviation WHERE user_id = '{id}'").fetchone()


        global_mean = create_global_mean()

        con = sqlite3.connect("recommender_books.sqlite")
        cursor = con.cursor()

        query = "SELECT * FROM books_deviation WHERE book_id NOT IN ("
        for index, item in enumerate(user_book_id):
            if index == len(user_book_id) - 1:
                query += str(item[0])
            else:
                query += str(item[0]) + ", "
        query += ")"

        cursor.execute(query)
        books_deviation_list = cursor.fetchall()

        query = "SELECT * FROM books_q WHERE book_id NOT IN ("
        for index, item in enumerate(user_book_id):
            if index == len(user_book_id) - 1:
                query += str(item[0])
            else:
                query += str(item[0]) + ", "
        query += ")"

        cursor.execute(query)
        books_q_list = cursor.fetchall()

        books_q = {}
        for item in books_q_list:
            if item[0] not in books_q:
                books_q[item[0]] = {}
            books_q[item[0]][item[1]] = item[2]
            

        users_p = {}
        for item in users_p_list:
            users_p[item[0]] = item[1]

        # Генерация рекомендаций 
        recommendations = {}
        for book_deviation in books_deviation_list:
            book_id = book_deviation[0]
            recommendations[book_id] = global_mean + users_deviation[0] + book_deviation[1]
            for factor_id in users_p:
                recommendations[book_id] += users_p[factor_id] * books_q[book_id][factor_id]

        



        # Определение существующих рекомендаций
        recommendations_rows_existed = db.session.execute(f"SELECT book_id FROM recommendations_Funk_SVD WHERE user_id = '{id}'").fetchall()
        recommendations_list_existed = []
        for item in recommendations_rows_existed:
           recommendations_list_existed.append(item[0])


        # Разделение новых данных на данные для добавления и данные для обновления
        recommendations_list_insert = []
        recommendations_list_update = []
        for book_rating_id in recommendations:
            if book_rating_id in recommendations_list_existed:
                recommendations_list_update.append((recommendations[book_rating_id], book_rating_id, id))
            else:
                recommendations_list_insert.append((id, book_rating_id, recommendations[book_rating_id]))


        query = "UPDATE recommendations_Funk_SVD SET recommendation = ? WHERE book_id = ? AND user_id = ?"
        cursor.executemany(query, recommendations_list_update)
        con.commit()

        query = "INSERT INTO recommendations_Funk_SVD (user_id, book_id, recommendation) VALUES (?, ?, ?)"
        cursor.executemany(query, recommendations_list_insert)
        con.commit()
        


        top_recommendation = db.session.execute(f"SELECT book_id FROM recommendations_Funk_SVD WHERE user_id = '{id}' ORDER BY recommendation DESC LIMIT '{int(count_of_output)}'").fetchall()

        # Составляется единый запрос для всех book_id
        query = "SELECT * FROM books WHERE id IN ("
        for index, item in enumerate(top_recommendation):
            if index == len(top_recommendation) - 1:
                query += str(item[0])
            else:
                query += str(item[0]) + ", "
        query += ")"

        # Получаем все необходимые книги
        cursor.execute(query)
        books = cursor.fetchall()

        result = []
        for row in books:
            dict_item = {}
            for index, value in enumerate(row):
                dict_item[cursor.description[index][0]] = value
            result.append(dict_item)

        return {'recommendations': result}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}









# Тестирование рекомендаций
def testing_prediction_Pearson(count_rating, required_number_of_crossings, required_correlation, normalization_number, percentage_tested_users, percentage_tested_ratings):
    # Берутся все пользователи c количеством оценок 10 и больше
    rows_users = db.session.execute(f"SELECT id FROM users WHERE count_rating >= '{count_rating}'").fetchall()
    try:
        # Перемешивание id пользователей
        random.shuffle(rows_users)

        # Разделение списка пользователей на исходные и тестовые данные
        users_len = len(rows_users)
        percentage_len = users_len * float(percentage_tested_users)
        initial_users_rows = []
        testing_users_rows = []
        for i in range(users_len):
            if i < percentage_len:
                testing_users_rows.append(rows_users[i])
            else:
                initial_users_rows.append(rows_users[i])

        

        con = sqlite3.connect("recommender_books.sqlite")
        cursor = con.cursor()

        # Для тестируемых пользователей запрашиваются оценки
        # Составляется единый запрос для всех id
        query = "SELECT * FROM ratings WHERE user_id IN ("
        for index, item in enumerate(testing_users_rows):
            if index == len(testing_users_rows) - 1:
                query += str(item[0])
            else:
                query += str(item[0]) + ", "
        query += ") ORDER BY user_id"

        # Получаем все необходимые оценки
        cursor.execute(query)
        rows_testing_ratings = cursor.fetchall()

        # Преобразование списка кортежей в двойной словарь оценок
        ratings_testing_dict = {}
        for item in rows_testing_ratings:
            user_id = item[1]
            if user_id not in ratings_testing_dict:
                ratings_testing_dict[user_id] = {}
                ratings_testing_dict[user_id]["books"] = {}
            ratings_testing_dict[user_id]["books"][item[0]] = item[2]


        # Для исходных пользователей запрашиваются оценки
        # Составляется единый запрос для всех id
        query = "SELECT * FROM ratings WHERE user_id IN ("
        for index, item in enumerate(initial_users_rows):
            if index == len(initial_users_rows) - 1:
                query += str(item[0])
            else:
                query += str(item[0]) + ", "
        query += ") ORDER BY user_id"

        # Получаем все необходимые оценки
        cursor.execute(query)
        rows_initial_ratings = cursor.fetchall()

        # Преобразование списка кортежей в двойной словарь оценок
        ratings_initial_dict = {}
        for item in rows_initial_ratings:
            user_id = item[1]
            if user_id not in ratings_initial_dict:
                ratings_initial_dict[user_id] = {}
                ratings_initial_dict[user_id]["books"] = {}
            ratings_initial_dict[user_id]["books"][item[0]] = item[2]


        # # Запрос списка средних значений для книг
        # books_avarage_ratings_list = db.session.execute(f"SELECT id, average_rating FROM books").fetchall()
        # books_avarage_ratings_dict = {}
        # for item in books_avarage_ratings_list:
        #     books_avarage_ratings_dict[item[0]] = item[1]

        # # Запрос списка средних значений для пользователей
        # users_avarage_ratings_list = db.session.execute(f"SELECT id, average_rating FROM users").fetchall()
        # users_avarage_ratings_dict = {}
        # for item in users_avarage_ratings_list:
        #     users_avarage_ratings_dict[item[0]] = item[1]

























        """ --------------------------------------------------------------------------------------------------------------------------------------------------- """

        # Нахождение глобального среднего
        r_m = []
        for item in rows_initial_ratings:
            r_m.append(item[2])
        global_mean = statistics.mean(r_m)

        # Константы
        factors = 10 #int(factors)
        learning_rate = 0.001 #float(learning_rate)
        regularization = 0.02 #float(regularization)
        gradient_count = 20 #int(gradient_count)

        books_av = {}
        users_av = {}
        for item in rows_initial_ratings:
            book_id = item[0]
            user_id = item[1]
            rating = item[2]
            if user_id not in users_av:
                users_av[user_id] = {}
                users_av[user_id]["sum"] = rating
                users_av[user_id]["count"] = 1
            else:
                users_av[user_id]["sum"] += rating
                users_av[user_id]["count"] += 1
                
            if book_id not in books_av:
                books_av[book_id] = {}
                books_av[book_id]["sum"] = rating
                books_av[book_id]["count"] = 1
            else:
                books_av[book_id]["sum"] += rating
                books_av[book_id]["count"] += 1
            
        for book_id in books_av:
            books_av[book_id]["av"] = books_av[book_id]["sum"] / books_av[book_id]["count"]

        for user_id in users_av:
            users_av[user_id]["av"] = users_av[user_id]["sum"] / users_av[user_id]["count"]


        # Инициализация матриц факторов
        users_p = {}
        users_dev = {}
        books_q = {}
        books_dev = {}
        for item in rows_initial_ratings:
            book_id = item[0]
            user_id = item[1]
            rating = item[2]
            if user_id not in users_dev:
                users_p[user_id] = {}
                for i in range(factors):
                    users_p[user_id][i] = 0.1
                users_dev[user_id] = users_av[user_id]["av"] - global_mean
            
            if book_id not in books_dev:
                books_q[book_id] = {}
                for i in range(factors):
                    books_q[book_id][i] = 0.1
                books_dev[book_id] = books_av[book_id]["av"] - global_mean

        # Генерация матриц факторов
        deviation = 0
        rat_len = rows_initial_ratings.__len__()
        print(rat_len)
        for factor in range(factors):
            finished = False
            iterations_counter = 0
            deviation = 0
            rating_init_rmse = 0
            while not finished:
                for item in rows_initial_ratings:
                    user_id = item[1]
                    book_id = item[0] 
                    rating = item[2]
                    rating_prediction = global_mean + users_dev[user_id] + books_dev[book_id]
                    for i in range(factors):
                        rating_prediction += users_p[user_id][i] * books_q[book_id][i]
                    e = rating - rating_prediction
                    users_dev[user_id] += learning_rate * (e - regularization * users_dev[user_id])
                    books_dev[book_id] += learning_rate * (e - regularization * books_dev[book_id])

                    user_p_val = users_p[user_id][factor]
                    book_q_val = books_q[book_id][factor]
                    users_p[user_id][factor] += learning_rate * (e * book_q_val - regularization * user_p_val)
                    books_q[book_id][factor] += learning_rate * (e * user_p_val - regularization * book_q_val)

                old_rating_init_rmse = rating_init_rmse
                rating_init_rmse = 0
                for item in rows_initial_ratings:
                    user_id = item[1]
                    book_id = item[0] 
                    rating = item[2]  
                    rating_prediction = global_mean + users_dev[user_id] + books_dev[book_id]
                    for i in range(factors):
                        rating_prediction += users_p[user_id][i] * books_q[book_id][i]
                    rating_init_rmse += (rating - rating_prediction)**2
                rating_init_rmse = (rating_init_rmse/rat_len)**(0.5)


                old_deviation = deviation
                deviation = 0
                for item in rows_initial_ratings:
                    user_id = item[1]
                    book_id = item[0] 
                    rating = item[2]  
                    rating_prediction = global_mean + users_dev[user_id] + books_dev[book_id]
                    for i in range(factors):
                        rating_prediction += users_p[user_id][i] * books_q[book_id][i]
                    deviation += abs(rating - rating_prediction)

                reg_users = 0
                for key in users_dev:
                    for i in range(factors):
                        reg_users += users_p[key][i]**2
                reg_users = reg_users**(0.5)

                reg_books = 0
                for key in books_dev:
                    for i in range(factors):
                        reg_books += books_q[key][i]**2
                reg_books = reg_books**(0.5)

                deviation += regularization * (reg_users + reg_books)

                iterations_counter += 1
                if iterations_counter > 1 and (((old_rating_init_rmse - rating_init_rmse) < 0.001) or (iterations_counter >= gradient_count) or (old_deviation < deviation)):
                    finished = True


                print("Фактор", factor+1, "Итерация", iterations_counter)
                print(rating_init_rmse, "---", deviation)
                print("---------------------------------------------------")
                # result["rmse"][grad] = {}
                # result["rmse"][grad]["init"] = deviation
                # result["rmse"][grad]["test"] = rmse_metrics

        # Рекомендации
        rmse_of_testing_funk_svd = 0
        rmse_of_testing_funk_svd_count = 0
        for selected_user in testing_users_rows:
            selecter_user_id = selected_user[0]
            ratings_dict_of_selected_user_all = ratings_testing_dict[selecter_user_id]["books"].copy()

            # Разделение списка пользователей на исходные и тестовые данные
            ratings_len = len(ratings_dict_of_selected_user_all)
            ratings_percentage_len = ratings_len * float(percentage_tested_ratings)


            ratings_dict_of_selected_user = {}
            ratings_dict_of_selected_user_testing = {}

            ratings_list_of_selected_user_all = list(ratings_dict_of_selected_user_all.items())

            random.shuffle(ratings_list_of_selected_user_all)
            counter = 0
            for key, value in ratings_list_of_selected_user_all:
                if counter < ratings_percentage_len:
                    ratings_dict_of_selected_user_testing[key] = value
                else:
                    ratings_dict_of_selected_user[key] = value
                counter += 1

            # Генерация матриц факторов и отклонений пользователя
            users_p[selecter_user_id] = {}
            for i in range(factors):
                users_p[selecter_user_id][i] = 0
            selected_user_av = 0
            selected_user_av_counter = 0
            for book_id in ratings_dict_of_selected_user:
                selected_user_av += ratings_dict_of_selected_user[book_id]
                selected_user_av_counter +=1
                if book_id in books_q:
                    for i in range(factors):
                        users_p[selecter_user_id][i] += ratings_dict_of_selected_user[book_id] * books_q[book_id][i]
            if selected_user_av_counter != 0:
                users_dev[selecter_user_id] = (selected_user_av / selected_user_av_counter) - global_mean
                print(users_dev[selecter_user_id])

            # Генерация оценок и подсчёт rmse
            for book_rating_id in ratings_dict_of_selected_user_testing:
                if book_rating_id in books_dev and selecter_user_id in users_dev:
                    rating_prediction = global_mean + users_dev[selecter_user_id] + books_dev[book_rating_id]
                    for i in range(factors):
                        rating_prediction += users_p[selecter_user_id][i] * books_q[book_rating_id][i]
                    rmse_of_testing_funk_svd += (ratings_dict_of_selected_user_testing[book_rating_id] - rating_prediction)**2
                    rmse_of_testing_funk_svd_count += 1

        print(users_p)
        if rmse_of_testing_funk_svd_count > 0:
            rmse_of_testing_funk_svd = (rmse_of_testing_funk_svd/rmse_of_testing_funk_svd_count)**(0.5)

        print("RMSE по Funk SVD: ", rmse_of_testing_funk_svd)
            





























        """ --------------------------------------------------------------------------------------------------------------------------------------------------- """

        # Нормализация происходит относительно константы
        normalization_number = float(normalization_number)
        # Количество тестируемых пользователей
        users_count = 0
        # Количество тестируемых оценок
        rating_tasting_count = 0
        # Количество рекомендованннхы оценок
        rating_recommendations_count = 0
        # mae, mse, rmse
        mae_metrics = 0
        mse_metrics = 0
        rmse_metrics = 0
        mae_metrics_compared = 0
        mse_metrics_compared = 0
        rmse_metrics_compared = 0

        # Генерация рекомендаций по корреляции Пирсона и по средним оценкам
        for selected_user in testing_users_rows:

            ratings_dict_of_selected_user_all = ratings_testing_dict[selected_user[0]]["books"].copy()

            
            # Разделение списка пользователей на исходные и тестовые данные
            ratings_len = len(ratings_dict_of_selected_user_all)
            ratings_percentage_len = ratings_len * float(percentage_tested_ratings)


            ratings_dict_of_selected_user = {}
            ratings_dict_of_selected_user_testing = {}

            ratings_list_of_selected_user_all = list(ratings_dict_of_selected_user_all.items())

            random.shuffle(ratings_list_of_selected_user_all)

            counter = 0
            for key, value in ratings_list_of_selected_user_all:
                if counter < ratings_percentage_len:
                    ratings_dict_of_selected_user_testing[key] = value
                else:
                    ratings_dict_of_selected_user[key] = value
                counter += 1


            ratings_dict = ratings_initial_dict.copy()
            ratings_dict_copy = ratings_dict.copy()


            # Подсчитать количество фильмов оцененных выбранным пользователем и каждым из других пользователей
            # Пользователи с недостаточным количеством пересечений убираются
            # Для пользователей с пересечениями подсчитать близость 
            for user_rating_id in ratings_dict_copy:
                number_of_crossings = 0
                # Для нормализации по константе
                sum_multiplied = 0
                sum_selected_user = 0
                sum_compared_user = 0
                for book_rating_id in ratings_dict_copy[user_rating_id]["books"]:
                    if book_rating_id in ratings_dict_of_selected_user:
                        number_of_crossings += 1
                        # Для нормализации по константе
                        sum_multiplied += (ratings_dict_copy[user_rating_id]["books"][book_rating_id] - normalization_number)*(ratings_dict_of_selected_user[book_rating_id] - normalization_number)
                        sum_selected_user += (ratings_dict_of_selected_user[book_rating_id] - normalization_number)**2
                        sum_compared_user += (ratings_dict_copy[user_rating_id]["books"][book_rating_id] - normalization_number)**2
                if number_of_crossings < int(required_number_of_crossings):
                    ratings_dict.pop(user_rating_id, None) 
                else:
                    ratings_dict[user_rating_id]["crossing"] = number_of_crossings
                    multiplied_sum = (sum_selected_user*sum_compared_user)**(0.5)
                    if multiplied_sum == 0:
                        correlation_number = 0
                    else:
                        correlation_number = sum_multiplied / multiplied_sum
                    ratings_dict[user_rating_id]["correlation"] = correlation_number

            # Отсев пользователей с недостаточным показателем корреляции
            ratings_dict_copy = ratings_dict.copy()

            for user_rating_id in ratings_dict_copy:
                if ratings_dict_copy[user_rating_id]["correlation"] < float(required_correlation):
                    ratings_dict.pop(user_rating_id, None)


            # Расчёт рекомендаций 
            # Промежуточные вычисления
            recommendations = {}
            for user_rating_id in ratings_dict:
                for book_rating_id in ratings_dict[user_rating_id]["books"]:
                    if book_rating_id not in ratings_dict_of_selected_user and book_rating_id in ratings_dict_of_selected_user_testing:
                        if book_rating_id not in recommendations:
                            recommendations[book_rating_id] = {}
                            recommendations[book_rating_id]["sum_correlation_and_rating"] = ratings_dict[user_rating_id]["correlation"]*ratings_dict[user_rating_id]["books"][book_rating_id]
                            recommendations[book_rating_id]["sum_correlation"] = ratings_dict[user_rating_id]["correlation"]
                            recommendations[book_rating_id]["number_of_users"] = 1
                        else:
                            recommendations[book_rating_id]["sum_correlation_and_rating"] += ratings_dict[user_rating_id]["correlation"]*ratings_dict[user_rating_id]["books"][book_rating_id]
                            recommendations[book_rating_id]["sum_correlation"] += ratings_dict[user_rating_id]["correlation"]
                            recommendations[book_rating_id]["number_of_users"] += 1

            # Подсчёт рекомендаций
            for book_rating_id in recommendations:
                if recommendations[book_rating_id]["sum_correlation"] != 0:
                    recommendations[book_rating_id]["recommendation"] = recommendations[book_rating_id]["sum_correlation_and_rating"] / recommendations[book_rating_id]["sum_correlation"]
                    mae_metrics += abs(recommendations[book_rating_id]["recommendation"]-ratings_dict_of_selected_user_testing[book_rating_id])
                    mse_metrics += (recommendations[book_rating_id]["recommendation"]-ratings_dict_of_selected_user_testing[book_rating_id])**2
                    mae_metrics_compared += abs(books_av[book_id]["av"]-ratings_dict_of_selected_user_testing[book_rating_id])
                    mse_metrics_compared += (books_av[book_id]["av"]-ratings_dict_of_selected_user_testing[book_rating_id])**2

            users_count += 1
            rating_tasting_count += len(ratings_dict_of_selected_user_testing)
            rating_recommendations_count += len(recommendations)

        if rating_recommendations_count != 0:
            mae_metrics = mae_metrics / rating_recommendations_count
            mse_metrics = mse_metrics / rating_recommendations_count
            rmse_metrics = mse_metrics**(0.5)
            mae_metrics_compared = mae_metrics_compared / rating_recommendations_count
            mse_metrics_compared = mse_metrics_compared / rating_recommendations_count
            rmse_metrics_compared = mse_metrics_compared**(0.5)

        print(users_count,rating_tasting_count,rating_recommendations_count,(mae_metrics,mae_metrics_compared),(mse_metrics,mse_metrics_compared),(rmse_metrics,rmse_metrics_compared))

        result = {}
        result["users_count"] = users_count
        result["rating_tasting_count"] = rating_tasting_count
        result["rating_recommendations_count"] = rating_recommendations_count
        result["mae_metrics"] = mae_metrics
        result["mae_metrics_compared"] = mae_metrics_compared
        result["mse_metrics"] = mse_metrics
        result["mse_metrics_compared"] = mse_metrics_compared
        result["rmse_metrics"] = rmse_metrics
        result["rmse_metrics_compared"] = rmse_metrics_compared

        return {'testing': result}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}
    












































def testing_prediction_Funk_SVD(factors, learning_rate, regularization, gradient_count, percentage_tested_ratings):
    try:
        rows_users = db.session.execute(f"SELECT id FROM users WHERE count_rating >= 100").fetchall()
        # Перемешивание id пользователей
        random.shuffle(rows_users)

        # Разделение списка пользователей на исходные и тестовые данные
        users_len = len(rows_users)
        percentage_len = users_len * float(percentage_tested_ratings)
        rows_initial_users = []
        rows_testing_users = []
        for i in range(users_len):
            if i < percentage_len:
                rows_testing_users.append(rows_users[i])
            else:
                rows_initial_users.append(rows_users[i])

        

        con = sqlite3.connect("recommender_books.sqlite")
        cursor = con.cursor()

        # Для тестируемых пользователей запрашиваются оценки
        # Составляется единый запрос для всех id
        query = "SELECT * FROM ratings WHERE user_id IN ("
        for index, item in enumerate(rows_testing_users):
            if index == len(rows_testing_users) - 1:
                query += str(item[0])
            else:
                query += str(item[0]) + ", "
        query += ") ORDER BY user_id"

        # Получаем все необходимые оценки
        cursor.execute(query)
        rows_testing_ratings = cursor.fetchall()

        # Преобразование списка кортежей в двойной словарь оценок
        testing_ratings_dict = {}
        for item in rows_testing_ratings:
            user_id = item[1]
            if user_id not in testing_ratings_dict:
                testing_ratings_dict[user_id] = {}
                testing_ratings_dict[user_id]["books"] = {}
            testing_ratings_dict[user_id]["books"][item[0]] = item[2]


        # Для исходных пользователей запрашиваются оценки
        # Составляется единый запрос для всех id
        query = "SELECT * FROM ratings WHERE user_id IN ("
        for index, item in enumerate(rows_initial_users):
            if index == len(rows_initial_users) - 1:
                query += str(item[0])
            else:
                query += str(item[0]) + ", "
        query += ") ORDER BY user_id"

        # Получаем все необходимые оценки
        cursor.execute(query)
        rows_initial_ratings = cursor.fetchall()

        # Преобразование списка кортежей в двойной словарь оценок
        initial_ratings_dict = {}
        for item in rows_initial_ratings:
            user_id = item[1]
            if user_id not in initial_ratings_dict:
                initial_ratings_dict[user_id] = {}
                initial_ratings_dict[user_id]["books"] = {}
            initial_ratings_dict[user_id]["books"][item[0]] = item[2]


        # Нахождение глобального среднего
        r_m = []
        for item in rows_initial_ratings:
            r_m.append(item[2])
        global_mean = statistics.mean(r_m)

        # Константы
        factors = 10 #int(factors)
        learning_rate = 0.001 #float(learning_rate)
        regularization = 0.02 #float(regularization)
        gradient_count = 20 #int(gradient_count)

        books_av = {}
        users_av = {}
        for item in rows_initial_ratings:
            book_id = item[0]
            user_id = item[1]
            rating = item[2]
            if user_id not in users_av:
                users_av[user_id] = {}
                users_av[user_id]["sum"] = rating
                users_av[user_id]["count"] = 1
            else:
                users_av[user_id]["sum"] += rating
                users_av[user_id]["count"] += 1
                
            if book_id not in books_av:
                books_av[book_id] = {}
                books_av[book_id]["sum"] = rating
                books_av[book_id]["count"] = 1
            else:
                books_av[book_id]["sum"] += rating
                books_av[book_id]["count"] += 1
            
        for book_id in books_av:
            books_av[book_id]["av"] = books_av[book_id]["sum"] / books_av[book_id]["count"]

        for user_id in users_av:
            users_av[user_id]["av"] = users_av[user_id]["sum"] / users_av[user_id]["count"]


        # Инициализация матриц факторов
        users_p = {}
        users_dev = {}
        books_q = {}
        books_dev = {}
        for item in rows_initial_ratings:
            book_id = item[0]
            user_id = item[1]
            rating = item[2]
            if user_id not in users_dev:
                users_p[user_id] = {}
                for i in range(factors):
                    users_p[user_id][i] = 0.1
                users_dev[user_id] = users_av[user_id]["av"] - global_mean
            
            if book_id not in books_dev:
                books_q[book_id] = {}
                for i in range(factors):
                    books_q[book_id][i] = 0.1
                books_dev[book_id] = books_av[book_id]["av"] - global_mean

        # Количество рекомендованннхы оценок
        rating_recommendations_count = 0
        # mse, rmse
        mse_metrics_compared = 0
        rmse_metrics_compared = 0
            
        for item in rows_initial_users:
            test_user_id = item[1]
            test_book_id = item[0]
            test_rating = item[2]
            recommendation = global_mean + users_dev[test_user_id] + books_dev[test_book_id]
            mse_metrics_compared += (recommendation - test_rating)**2
            rating_recommendations_count += 1
        if rating_recommendations_count != 0:
            mse_metrics_compared = mse_metrics_compared / rating_recommendations_count
            rmse_metrics_compared = mse_metrics_compared**(0.5)


        print("------------------")
        print("Исходное значение", rmse_metrics_compared)
        print("------------------")

        result = {}
        result["rmse"] = {}

        deviation = 0
        rat_len = rows_initial_users.__len__()
        print(rat_len)
        # iterations_counter = 0
        rating_init_pred = 0
        for epoch in range(100):
            for factor in range(factors):
                deviation = 0
                
                for item in rows_initial_users:
                    user_id = item[1]
                    book_id = item[0] 
                    rating = item[2]
                    rating_prediction = global_mean + users_dev[user_id] + books_dev[book_id]
                    for i in range(factors):
                        rating_prediction += users_p[user_id][i] * books_q[book_id][i]
                    e = rating - rating_prediction
                    users_dev[user_id] += learning_rate * (e - regularization * users_dev[user_id])
                    books_dev[book_id] += learning_rate * (e - regularization * books_dev[book_id])

                    user_p_val = users_p[user_id][factor]
                    book_q_val = books_q[book_id][factor]
                    users_p[user_id][factor] += learning_rate * (e * book_q_val - regularization * user_p_val)
                    books_q[book_id][factor] += learning_rate * (e * user_p_val - regularization * book_q_val)

                old_rating_init_pred = rating_init_pred
                rating_init_pred = 0
                for item in rows_initial_users:
                    user_id = item[1]
                    book_id = item[0] 
                    rating = item[2]  
                    rating_prediction = global_mean + users_dev[user_id] + books_dev[book_id]
                    for i in range(factors):
                        rating_prediction += users_p[user_id][i] * books_q[book_id][i]
                    rating_init_pred += (rating - rating_prediction)**2
                rating_init_pred = (rating_init_pred/rat_len)**(0.5)


                old_deviation = deviation
                deviation = 0
                for item in rows_initial_users:
                    user_id = item[1]
                    book_id = item[0] 
                    rating = item[2]  
                    rating_prediction = global_mean + users_dev[user_id] + books_dev[book_id]
                    for i in range(factors):
                        rating_prediction += users_p[user_id][i] * books_q[book_id][i]
                    deviation += abs(rating - rating_prediction)

                reg_users = 0
                for key in users_dev:
                    for i in range(factors):
                        reg_users += users_p[key][i]**2
                reg_users = reg_users**(0.5)

                reg_books = 0
                for key in books_dev:
                    for i in range(factors):
                        reg_books += books_q[key][i]**2
                reg_books = reg_books**(0.5)

                deviation += regularization * (reg_users + reg_books)

                # iterations_counter += 1
                # if iterations_counter > 1 and ((iterations_counter >= gradient_count) or ((old_deviation - deviation) < 100)):
                #     finished = True

                rating_recommendations_count = 0
                mse_metrics = 0
                rmse_metrics = 0
                for item in rows_testing_users:
                    test_user_id = item[1]
                    test_book_id = item[0]
                    test_rating = item[2]
                    recommendation = global_mean + users_dev[test_user_id] + books_dev[test_book_id]
                    for factor_id in range(factors):
                        recommendation += users_p[test_user_id][factor_id] * books_q[test_book_id][factor_id]
                    mse_metrics += (recommendation - test_rating)**2
                    rating_recommendations_count += 1
                if rating_recommendations_count != 0:
                    mse_metrics = mse_metrics / rating_recommendations_count
                    rmse_metrics = mse_metrics**(0.5)

                print("Эпока", epoch+1,"Фактор", factor+1)
                print(rmse_metrics, rating_recommendations_count, "---", deviation)
                print("---------------------------------------------------")
                # result["rmse"][grad] = {}
                # result["rmse"][grad]["init"] = deviation
                # result["rmse"][grad]["test"] = rmse_metrics

        
        

        result["rating_recommendations_count"] = rating_recommendations_count
        result["rmse_metrics_compared"] = rmse_metrics_compared

        return {'testing': result}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}








def create_users_by_filter(count_rating):
    try:
        users_row = db.session.execute(f"SELECT * FROM users WHERE count_rating >= {count_rating}").fetchall()
        users_dict = {}
        for item in users_row:
            users_dict[item[0]] = {}
            users_dict[item[0]]["id"] = item[0]
            users_dict[item[0]]["av"] = item[1]
            users_dict[item[0]]["co"] = item[2]

        if users_dict.__len__() == 0:
            return {'Ошибка': 'Ошибка'}

        return {'table': users_dict}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}

    













def work():
    try:
        # Константы
        percentage_tested_ratings = 0.1
        factors_count = 10
        epoch_count = 100
        learning_rate = 0.001
        regularization = 0.02

        # Получаем строки оценок
        rows_rating = db.session.execute(f"SELECT ratings.book_id, ratings.user_id, ratings.rating FROM ratings JOIN users, books ON ratings.user_id = users.id AND ratings.book_id = books.id WHERE users.count_rating >= 20 AND books.count_rating >= 20").fetchall()

        # Преобразуем в словарь
        dict_rating = {}
        for item in rows_rating:
            book_id = item[0]
            user_id = item[1]
            rating_value = item[2]
            if user_id not in dict_rating:
                dict_rating[user_id] = {}
                dict_rating[user_id][book_id] = rating_value
            else:
                dict_rating[user_id][book_id] = rating_value

        # Разделение оценок у каждого пользователя на обучающие и тестовые
        rows_train_rating = []
        rows_test_rating = []
        for user_id in dict_rating:
            user_len = len(dict_rating[user_id])
            percentage_len = user_len * percentage_tested_ratings

            rows_rating_of_user = []
            for book_id in dict_rating[user_id]:
                rows_rating_of_user.append((book_id, user_id, dict_rating[user_id][book_id]))

            random.shuffle(rows_rating_of_user)

            counter = 0
            for item in rows_rating_of_user:
                if counter < percentage_len:
                    rows_test_rating.append(item)
                else:
                    rows_train_rating.append(item)
                counter += 1

        print("Тестовых оценок: ", rows_test_rating.__len__())
        print("Обучаюших оценок: ", rows_train_rating.__len__())

        # Нахождение глобального среднего по обучающим данным 
        r_m = []
        for item in rows_train_rating:
            r_m.append(item[2])
        global_mean = statistics.mean(r_m)

        # Инициализация матриц факторов
        users_factors = {}
        books_factors = {}
        for item in rows_train_rating:
            book_id = item[0]
            user_id = item[1]
            rating_value = item[2]

            if book_id not in books_factors:
                books_factors[book_id] = {}
                for i in range(factors_count):
                    books_factors[book_id][i] = 0.1

            if user_id not in users_factors:
                users_factors[user_id] = {}
                for i in range(factors_count):
                    users_factors[user_id][i] = 0.1
        
        testing_rmse = 0
        testing_rmse_count = 0
        for item in rows_test_rating:
            book_id = item[0]
            user_id = item[1]
            rating_value = item[2]

            if book_id in books_factors:
                rating_prediction = global_mean
                for i in range(factors_count):
                    rating_prediction += users_factors[user_id][i] * books_factors[book_id][i]
                e = rating_value - rating_prediction

                testing_rmse += e**2
                testing_rmse_count += 1
        
        if testing_rmse_count > 0:
            testing_rmse = (testing_rmse / testing_rmse_count)**(0.5)
        
        print("Тестовый RMSE: ", testing_rmse, " Получено ", testing_rmse_count, " оценок из ", rows_test_rating.__len__())

        # Генерация матриц на обучающих данных
        rmse_of_train = 0
        minimization_value = 0
        for epoch in range(epoch_count):
            for factor in range(factors_count):
                for item in rows_train_rating:
                    book_id = item[0]
                    user_id = item[1]
                    rating_value = item[2]

                    rating_prediction = global_mean
                    for i in range(factors_count):
                        rating_prediction += users_factors[user_id][i] * books_factors[book_id][i]
                    e = rating_value - rating_prediction

                    current_user_factor = users_factors[user_id][factor]
                    current_book_factor = books_factors[book_id][factor]
                    users_factors[user_id][factor] += learning_rate * (e * current_book_factor - regularization * current_user_factor)
                    books_factors[book_id][factor] += learning_rate * (e * current_user_factor - regularization * current_book_factor)

                old_rmse_of_train = rmse_of_train
                old_minimization_value = minimization_value
                rmse_of_train = 0
                counter_of_rmse = 0
                minimization_value = 0
                for item in rows_train_rating:
                    book_id = item[0]
                    user_id = item[1]
                    rating_value = item[2]

                    rating_prediction = global_mean
                    for i in range(factors_count):
                        rating_prediction += users_factors[user_id][i] * books_factors[book_id][i]
                    e = rating_value - rating_prediction
                    
                    minimization_value += abs(e)
                    rmse_of_train += e**2
                    counter_of_rmse += 1
                
                if counter_of_rmse > 0:
                    rmse_of_train = (rmse_of_train/counter_of_rmse)**(0.5)

                
                minimization_books_factors = 0
                minimization_users_factors = 0
                
                for book_id in books_factors:
                    for i in range(factors_count):
                        minimization_books_factors += books_factors[book_id][i]
                for user_id in users_factors:
                    for i in range(factors_count):
                        minimization_users_factors += users_factors[user_id][i]

                minimization_value += regularization * (minimization_books_factors + minimization_users_factors)
                
                print("Эпоха: ",epoch + 1," Фактор: ", factor + 1, " RMSE: ", rmse_of_train, " Значение минимизации: ", minimization_value)



        # Тестирование на тестовых данных
        
            testing_rmse = 0
            testing_rmse_count = 0
            for item in rows_test_rating:
                book_id = item[0]
                user_id = item[1]
                rating_value = item[2]

                if book_id in books_factors:
                    rating_prediction = global_mean
                    for i in range(factors_count):
                        rating_prediction += users_factors[user_id][i] * books_factors[book_id][i]
                    e = rating_value - rating_prediction

                    testing_rmse += e**2
                    testing_rmse_count += 1
            
            if testing_rmse_count > 0:
                testing_rmse = (testing_rmse / testing_rmse_count)**(0.5)
            
            print("Тестовый RMSE: ", testing_rmse, " Получено ", testing_rmse_count, " оценок из ", rows_test_rating.__len__())





        return 0
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}