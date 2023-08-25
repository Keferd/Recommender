from sqlalchemy import true
from recapp import db
from datetime import datetime
from flask import session, make_response, redirect, url_for, jsonify
import bcrypt
import random
import statistics
import math

import sqlite3;





def get_prediction(global_mean, factors_count, user_factors, book_factors):
    rating_prediction = global_mean
    for i in range(factors_count):
        rating_prediction += user_factors[i] * book_factors[i]

    return rating_prediction

def get_rmse(ratings, books_factors, users_factors, global_mean, factors_count):

    rmse = 0
    count = 0

    for item in ratings:
        book_id = item[0]
        user_id = item[1]
        rating_value = item[2]

        if book_id in books_factors:
            rating_prediction = get_prediction(global_mean, factors_count, users_factors[user_id], books_factors[book_id])
            e = rating_value - rating_prediction
            rmse += e**2
            count += 1
    
    if count > 0:
        rmse = (rmse / count)**(0.5)

    return rmse

def get_rmse_with_count(ratings, books_factors, users_factors, global_mean, factors_count):

    rmse = 0
    count = 0

    for item in ratings:
        book_id = item[0]
        user_id = item[1]
        rating_value = item[2]

        if book_id in books_factors:
            rating_prediction = get_prediction(global_mean, factors_count, users_factors[user_id], books_factors[book_id])
            e = rating_value - rating_prediction
            rmse += e**2
            count += 1
    
    if count > 0:
        rmse = (rmse / count)**(0.5)

    return rmse, count

def get_rmse_with_sum(ratings, books_factors, users_factors, global_mean, factors_count):

    rmse = 0
    count = 0
    sum = 0

    for item in ratings:
        book_id = item[0]
        user_id = item[1]
        rating_value = item[2]

        if book_id in books_factors:
            rating_prediction = get_prediction(global_mean, factors_count, users_factors[user_id], books_factors[book_id])
            e = rating_value - rating_prediction
            rmse += e**2
            count += 1

    sum = rmse 
    
    if count > 0:
        rmse = (rmse / count)**(0.5)

    return rmse, sum




# Funk SVD стохастический градиентный спуск
def funk_svd(rows_rating, factors_count, epoch_count, learning_rate, regularization, percentage_val_ratings):
    # Параметры
    factors_count = int(factors_count)
    epoch_count = int(epoch_count)
    learning_rate = float(learning_rate)
    regularization = float(regularization)
    percentage_val_ratings = float(percentage_val_ratings)

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
    rows_val_rating = []
    for user_id in dict_rating:
        user_len = len(dict_rating[user_id])
        percentage_len = user_len * percentage_val_ratings

        rows_rating_of_user = []
        for book_id in dict_rating[user_id]:
            rows_rating_of_user.append((book_id, user_id, dict_rating[user_id][book_id]))

        random.shuffle(rows_rating_of_user)

        counter = 0
        for item in rows_rating_of_user:
            if counter < percentage_len:
                rows_val_rating.append(item)
            else:
                rows_train_rating.append(item)
            counter += 1

    print("-------------------------------------------------------------------------------------------------------")
    print("Валидационных оценок: ", rows_val_rating.__len__())
    print("Обучающих оценок: ", rows_train_rating.__len__())


    # Нахождение глобального среднего по обучающим данным 
    r_m = []
    for item in rows_train_rating:
        r_m.append(item[2])
    global_mean = statistics.mean(r_m)
        
    # Инициализация матриц факторов
    users_factors = {}
    books_factors = {}
    for item in rows_rating:
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

    val_rmse, val_rmse_count = get_rmse_with_count(rows_val_rating, books_factors, users_factors, global_mean, factors_count)

    print("-------------------------------------------------------------------------------------------------------")
    print("Валидационный RMSE: ", val_rmse, " Получено ", val_rmse_count, " оценок из ", rows_val_rating.__len__())

    # Генерация матриц на обучающих данных
    rmse_of_train = 0
    minimization_value = 0
    end_value = False
    current_epoch = 0
    while not end_value:
        for factor in range(factors_count):
            for item in rows_train_rating:
                book_id = item[0]
                user_id = item[1]
                rating_value = item[2]

                rating_prediction = get_prediction(global_mean, factors_count, users_factors[user_id], books_factors[book_id])
                e = rating_value - rating_prediction

                current_user_factor = users_factors[user_id][factor]
                current_book_factor = books_factors[book_id][factor]
                users_factors[user_id][factor] += learning_rate * (e * current_book_factor - regularization * current_user_factor)
                books_factors[book_id][factor] += learning_rate * (e * current_user_factor - regularization * current_book_factor)

        old_rmse_of_train = rmse_of_train
        old_minimization_value = minimization_value

        rmse_of_train, minimization_value = get_rmse_with_sum(rows_train_rating, books_factors, users_factors, global_mean, factors_count)
        
        minimization_books_factors = 0
        minimization_users_factors = 0
        
        for book_id in books_factors:
            for i in range(factors_count):
                minimization_books_factors += books_factors[book_id][i]
        for user_id in users_factors:
            for i in range(factors_count):
                minimization_users_factors += users_factors[user_id][i]

        minimization_value += regularization * (minimization_books_factors + minimization_users_factors)

        if old_rmse_of_train - rmse_of_train < 0.001 or old_minimization_value < minimization_value:
            learning_rate *= 0.5
            regularization *= 0.5

        old_val_rmse = val_rmse
        # Тестирование на валидационных данных
        val_rmse, val_rmse_count = get_rmse_with_count(rows_val_rating, books_factors, users_factors, global_mean, factors_count)

        
        current_epoch += 1
        print("-------------------------------------------------------------------------------------------------------")
        print("Эпоха: ",current_epoch, " Обучающий RMSE: ", rmse_of_train, " Значение минимизации: ", minimization_value, " Валидациооный RMSE: ", val_rmse)
        
        if old_val_rmse < val_rmse or current_epoch >= epoch_count:
            end_value = True

    for factor in range(factors_count):
        for item in rows_val_rating:
            book_id = item[0]
            user_id = item[1]
            rating_value = item[2]

            rating_prediction = get_prediction(global_mean, factors_count, users_factors[user_id], books_factors[book_id])
            e = rating_value - rating_prediction

            current_user_factor = users_factors[user_id][factor]
            current_book_factor = books_factors[book_id][factor]
            users_factors[user_id][factor] += learning_rate * (e * current_book_factor - regularization * current_user_factor)
            books_factors[book_id][factor] += learning_rate * (e * current_user_factor - regularization * current_book_factor)

    rmse_of_train, minimization_value = get_rmse_with_sum(rows_train_rating, books_factors, users_factors, global_mean, factors_count)
    
    minimization_books_factors = 0
    minimization_users_factors = 0
    
    for book_id in books_factors:
        for i in range(factors_count):
            minimization_books_factors += books_factors[book_id][i]
    for user_id in users_factors:
        for i in range(factors_count):
            minimization_users_factors += users_factors[user_id][i]

    minimization_value += regularization * (minimization_books_factors + minimization_users_factors)

    val_rmse, val_rmse_count = get_rmse_with_count(rows_val_rating, books_factors, users_factors, global_mean, factors_count)

    print("-------------------------------------------------------------------------------------------------------")
    print("Эпоха дообучения, Обучающий RMSE: ", rmse_of_train, " Значение минимизации: ", minimization_value, " Валидациооный RMSE: ", val_rmse)
        
    return global_mean, books_factors, users_factors




# Нахождений средних оклонений
def averages(rows_train_rating):
    # Нахождение глобального среднего по обучающим данным 
    r_m = []
    for item in rows_train_rating:
        r_m.append(item[2])
    global_mean = statistics.mean(r_m)

    # Подсчёт средних по обучающим данным
    book_averages = {}
    user_averages = {}
    book_averages_counter = {}
    user_averages_counter = {}
    for item in rows_train_rating:
        book_id = item[0]
        user_id = item[1]
        rating_value = item[2]

        if book_id not in book_averages:
            book_averages[book_id] = rating_value
            book_averages_counter[book_id] = 1
        else:
            book_averages[book_id] += rating_value
            book_averages_counter[book_id] += 1

        if user_id not in user_averages:
            user_averages[user_id] = rating_value
            user_averages_counter[user_id] = 1
        else:
            user_averages[user_id] += rating_value
            user_averages_counter[user_id] += 1

    for book_id in book_averages:
        book_averages[book_id] = book_averages[book_id] / book_averages_counter[book_id] - global_mean

    for user_id in user_averages:
        user_averages[user_id] = user_averages[user_id] / user_averages_counter[user_id] - global_mean      

    return book_averages, user_averages

# Тестирование рекомендаций по средним оценкам
def averages_testing(rows_test_rating, rows_train_rating, book_averages, user_averages):
        
    # Нахождение глобального среднего по обучающим данным 
    r_m = []
    for item in rows_train_rating:
        r_m.append(item[2])
    global_mean = statistics.mean(r_m)

    # RMSE по средним отклонениям
    rmse = 0
    count = 0

    for item in rows_test_rating:
        book_id = item[0]
        user_id = item[1]
        rating_value = item[2]

        if book_id in book_averages:
            rating_prediction = global_mean + book_averages[book_id] + user_averages[user_id]
            e = rating_value - rating_prediction
            rmse += e**2
            count += 1
    
    if count > 0:
        rmse = (rmse / count)**(0.5)

    return rmse, count




def pearson_correlation_prediction(ratings, correlation, current_user_id):

    current_user_id = int(current_user_id)

    predictions = {}
    for book_id in ratings:
        if current_user_id not in ratings[book_id]:
            sum_correlation_and_rating = 0
            sum_correlation = 0
            number_of_users = 0
            for user_id in ratings[book_id]:
                if user_id in correlation:
                    number_of_users += 1
                    sum_correlation += correlation[user_id]
                    sum_correlation_and_rating += correlation[user_id] * ratings[book_id][user_id]
            
            if number_of_users > 0 and sum_correlation != 0:
                predictions[book_id] = sum_correlation_and_rating / sum_correlation

    return predictions

def pearson_correlation(ratings, current_user_id, global_mean):

    current_user_id = int(current_user_id)
    global_mean = float(global_mean)

    correlation = {}
    for user_id in ratings:
        if user_id != current_user_id:
            number_of_crossings = 0
            sum_multiplied = 0
            sum_current_user = 0
            sum_compared_user = 0
            for book_id in ratings[user_id]:
                if book_id in ratings[current_user_id]:
                    number_of_crossings += 1
                    sum_multiplied += (ratings[user_id][book_id] - global_mean)*(ratings[current_user_id][book_id] - global_mean)
                    sum_current_user += (ratings[current_user_id][book_id] - global_mean)**2
                    sum_compared_user += (ratings[user_id][book_id] - global_mean)**2
            if number_of_crossings > 2 and sum_current_user != 0 and sum_compared_user != 0:
                correlation_value = sum_multiplied / ((sum_current_user*sum_compared_user)**(0.5))
                if correlation_value > 0.5:
                    correlation[user_id] = correlation_value

    return correlation


def pearson_testing(rows_train_rating, rows_test_rating):
    
    # Нахождение глобального среднего по обучающим данным 
    r_m = []
    for item in rows_train_rating:
        r_m.append(item[2])
    global_mean = statistics.mean(r_m)

    ratings_dict = {}
    for item in rows_train_rating:
        book_id = item[0]
        user_id = item[1]
        rating = item[2]

        if user_id not in ratings_dict:
            ratings_dict[user_id] = {}
            ratings_dict[user_id][book_id] = rating
        else:
            ratings_dict[user_id][book_id] = rating

    ratings_dict_rev = {}
    for item in rows_train_rating:
        book_id = item[0]
        user_id = item[1]
        rating = item[2]

        if book_id not in ratings_dict_rev:
            ratings_dict_rev[book_id] = {}
            ratings_dict_rev[book_id][user_id] = rating
        else:
            ratings_dict_rev[book_id][user_id] = rating

    predictions = {}
    count = 0
    for user_id in ratings_dict:
        predictions[user_id] = pearson_correlation_prediction(ratings_dict_rev, pearson_correlation(ratings_dict, user_id, global_mean), user_id)
        count += 1
        print(count)

    rmse = 0
    count = 0

    for item in rows_test_rating:
        book_id = item[0]
        user_id = item[1]
        rating_value = item[2]

        if book_id in predictions[user_id]:
            e = rating_value - predictions[user_id][book_id]
            rmse += e**2
            count += 1
    
    if count > 0:
        rmse = (rmse / count)**(0.5)

    return rmse, count




def work():
    try:
        percentage_tested_ratings = 0.01
        percentage_tested_ratings = float(percentage_tested_ratings)
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

        print("-------------------------------------------------------------------------------------------------------")
        print("Тестовых оценок: ", rows_test_rating.__len__())
        print("Обучающих оценок: ", rows_train_rating.__len__())

        result = {}

        # Тестирование рекомендаций по средним оценкам
        book_averages, user_averages = averages(rows_train_rating)
        rmse_average, count = averages_testing(rows_test_rating, rows_train_rating, book_averages, user_averages)
        print("-------------------------------------------------------------------------------------------------------")
        print("RMSE по средним: ", rmse_average, " Получено ", count, " оценок из ", rows_test_rating.__len__())
        result['rmse_average'] = rmse_average

        # Тестирование рекомендаций по Funk SVD
        factors_count = 10
        epoch_count = 100
        learning_rate = 0.05
        regularization = 0.1
        percentage_val_ratings = 0.01
        global_mean, books_factors, users_factors = funk_svd(rows_train_rating, factors_count, epoch_count, learning_rate, regularization, percentage_val_ratings)
        test_funk_svd, test_funk_svd_count = get_rmse_with_count(rows_test_rating, books_factors, users_factors, global_mean, factors_count)
        print("-------------------------------------------------------------------------------------------------------")
        print("RMSE по Funk SVD: ", test_funk_svd, " Получено ", test_funk_svd_count, " оценок из ", rows_test_rating.__len__())
        result['test_funk_svd'] = test_funk_svd
        

        # Тестирование рекомендаций по корреляции Пирсона
        # rmse_pearson, rmse_pearson_count = pearson_testing(rows_train_rating, rows_test_rating)
        # print("-------------------------------------------------------------------------------------------------------")
        # print("RMSE по корреляции Пирсона: ", rmse_pearson, " Получено ", rmse_pearson_count, " оценок из ", rows_test_rating.__len__())
        # result['rmse_pearson'] = rmse_pearson


        return result
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}
    











