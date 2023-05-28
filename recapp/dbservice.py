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


