from sqlalchemy import true
from recapp import db
from datetime import datetime
from flask import session, make_response, redirect, url_for, jsonify
import bcrypt

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
def create_prediction_Pearson(id):
    # Берутся все пользователи c количеством оценок 20 и больше, кроме выбранного пользователя
    rows_users = db.session.execute(f"SELECT id FROM users WHERE count_rating >= 20 AND id != '{id}'").fetchall()
    rows_of_selected_user = db.session.execute(f"SELECT book_id, rating FROM ratings WHERE user_id = '{id}'").fetchall()
    try:
        con = sqlite3.connect("recommender_books.sqlite")
        cursor = con.cursor()

        # Преобразуется список кортежей в единый кортеж
        users_list = []
        for item in rows_users:
            users_list.append(item[0])
        users_tuple = tuple(users_list)

        # Составляется единый запрос для всех id
        query = "SELECT * FROM ratings WHERE user_id IN ("
        for index, item in enumerate(rows_users):
            if index == len(rows_users) - 1:
                query += str(item[0])
            else:
                query += str(item[0]) + ", "
        query += ") ORDER BY user_id"

        # Получаем все необходимые оценки
        cursor.execute(query)
        rows_ratings = cursor.fetchall()

        # Преобразование списка кортежей в двойной словарь оценок
        ratings_dict = {}
        for item in rows_ratings:
            user_id = item[1]
            if user_id not in ratings_dict:
                ratings_dict[user_id] = {}
                ratings_dict[user_id]["books"] = {}
            ratings_dict[user_id]["books"][item[0]] = item[2]

        # Создание словаря оценок для выбранного пользователя
        ratings_dict_of_selected_user = {}
        for item in rows_of_selected_user:
            ratings_dict_of_selected_user[item[0]] = item[1]
        
        # Подсчитать количество фильмов оцененных выбранным пользователем и каждым из других пользователей
        # Пользователи с недостаточным количеством пересечений убираются
        # Для пользователей с пересечениями подсчитать близость 
        # Нормализация происходит относительно константы
        normalization_number = 3.5
        # Минимальное необходимое количество пересечений
        required_number_of_crossings = 5
        # Минимальное необходимое значение корреляции
        required_correlation = 0.3

        ratings_dict_copy = ratings_dict.copy()

        for user_rating_id in ratings_dict_copy:
            number_of_crossings = 0
            sum_multiplied = 0
            sum_selected_user = 0
            sum_compared_user = 0
            for book_rating_id in ratings_dict_copy[user_rating_id]["books"]:
                if book_rating_id in ratings_dict_of_selected_user:
                    number_of_crossings += 1
                    sum_multiplied += (ratings_dict_copy[user_rating_id]["books"][book_rating_id] - normalization_number)*(ratings_dict_of_selected_user[book_rating_id] - normalization_number)
                    sum_selected_user += (ratings_dict_of_selected_user[book_rating_id] - normalization_number)**2
                    sum_compared_user += (ratings_dict_copy[user_rating_id]["books"][book_rating_id] - normalization_number)**2
            if number_of_crossings < required_number_of_crossings:
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
            if ratings_dict_copy[user_rating_id]["correlation"] < required_correlation:
                ratings_dict.pop(user_rating_id, None)

        # for user_rating_id in ratings_dict:
        #     print((ratings_dict[user_rating_id]["correlation"],ratings_dict[user_rating_id]["crossing"]))


        # Расчёт рекомендаций 
        # Промежуточные вычисления
        recommendations = {}
        for user_rating_id in ratings_dict:
            for book_rating_id in ratings_dict[user_rating_id]["books"]:
                if book_rating_id not in ratings_dict_of_selected_user:
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
                # if recommendations[book_rating_id]["number_of_users"] > 2:
                #     print(recommendations[book_rating_id])

        # Определение существующих рекомендаций
        recommendations_rows_existed = db.session.execute(f"SELECT book_id FROM recommendations_Pearson WHERE user_id = '{id}'").fetchall()
        recommendations_list_existed = []
        for item in recommendations_rows_existed:
           recommendations_list_existed.append(item[0])


        # Разделение новых данных на данные для добавления и данные для обновления
        recommendations_list_insert = []
        recommendations_list_update = []
        for book_rating_id in recommendations:
            if book_rating_id in recommendations_list_existed:
                recommendations_list_update.append((recommendations[book_rating_id]["recommendation"], recommendations[book_rating_id]["number_of_users"], book_rating_id))
            else:
                recommendations_list_insert.append((id, book_rating_id, recommendations[book_rating_id]["recommendation"], recommendations[book_rating_id]["number_of_users"]))


        query = "UPDATE recommendations_Pearson SET recommendation = ?, number_of_users = ? WHERE book_id = ?"
        cursor.executemany(query, recommendations_list_update)
        con.commit()

        query = "INSERT INTO recommendations_Pearson (user_id, book_id, recommendation, number_of_users) VALUES (?, ?, ?, ?)"
        cursor.executemany(query, recommendations_list_insert)
        con.commit()

        return {'message': "Prediction Pearson CREATED!"}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}

# Тестирование рекомендаций по коэффициенту корреляции Пирсона
def testing_prediction_Pearson():
    try:
        return {'message': "Testing"}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}