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


