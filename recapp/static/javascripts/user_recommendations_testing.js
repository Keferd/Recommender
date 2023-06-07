let menu_user_recommendation_testing_button = document.getElementById("admin__menu_user_recommendation_testing");

menu_user_recommendation_testing_button.addEventListener("click", function (e) {

    let area = document.getElementById('admin__main')
    
    area.innerHTML = `
        <div class="admin__main-container">
        <h1 class="admin__h1"> Тестирование рекомендаций </h1>
        <div class="admin__content">
        <div class="admin__form">
            <div>
                <label for="count_rating">Минимальное количество оценок от пользователя:</label>
                <input class="admin__input-number" type="number" min="1" value="100" id="count_rating">
            </div>
            <div>
                <label for="number_of_crossings">Минимальное количество пересечений между пользователями:</label>
                <input class="admin__input-number" type="number" min="1" value="3" id="number_of_crossings">
            </div>
            <div>
                <label for="correlation">Минимальное число корреляции:</label>
                <input class="admin__input-number" type="number" step="0.01" max="1" min="0" value="0.3" id="correlation">
            </div>
            <div>
                <label for="normalization_number">Число, относительно которого происходит нормализация:</label>
                <input class="admin__input-number" type="number" step="0.01" value="3.8" id="normalization_number">
            </div>
            <div>
                <label for="percentage_tested_users">Процент пользователей для тестирования:</label>
                <input class="admin__input-number" type="number" step="0.01" max="1" min="0" value="0.2" id="percentage_tested_users">
            </div>
            <div>
                <label for="percentage_tested_ratings">Процент оценок пользователей для тестирования:</label>
                <input class="admin__input-number" type="number" step="0.01" max="1" min="0" value="0.25" id="percentage_tested_ratings">
            </div>

            <div>
            <input class="admin__input-button" type="button" value="Запрос" id="user_recommendation_testing_button">
            </div>
        </div>
        <div class="admin__result">
            <h2>Результаты:</h2>
            <div class="admin__result-content" id="admin__testing">

            </div>
        </div>
        </div>
        </div>
        <link rel="stylesheet" href="/static/styles/user_recommendations_menu.css">
    `


    // -----------------------------------------------------------------------------

    let user_recommendation_testing_button = document.getElementById("user_recommendation_testing_button");

    user_recommendation_testing_button.addEventListener("click", function (e) {

        let count_rating = document.getElementById('count_rating').value;
        let number_of_crossings = document.getElementById('number_of_crossings').value;
        let correlation = document.getElementById('correlation').value;
        let normalization_number = document.getElementById('normalization_number').value
        let percentage_tested_users = document.getElementById('percentage_tested_users').value;
        let percentage_tested_ratings = document.getElementById('percentage_tested_ratings').value;


        let user_formdata = JSON.stringify({count_rating: count_rating, 
                                            number_of_crossings: number_of_crossings,
                                            correlation: correlation,
                                            normalization_number: normalization_number,
                                            percentage_tested_users: percentage_tested_users,
                                            percentage_tested_ratings: percentage_tested_ratings});

        formparse = JSON.parse(user_formdata);

        if (formparse['count_rating'] != "" && 
            formparse['number_of_crossings'] != "" && 
            formparse['correlation'] != "" && 
            formparse['normalization_number'] != "" &&
            formparse['percentage_tested_users'] != "" && 
            formparse['percentage_tested_ratings'] != "") {
            fetch("/api/testing_prediction_Pearson",
            {
                method: "POST",
                body: user_formdata,
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                response.json().then(function(data) {
                    console.log("hello")

                    let area = document.getElementById('admin__testing')
                    area.innerHTML = ""

                    let request = data['testing'];
                    if (request != "") {
                        area.innerHTML += `
                        <div class="admin__testing_block">
                            <div>Количество тестируемых пользователей:</div>
                            <div>` + request["users_count"] + `</div>
                        </div>
                        <div class="admin__testing_block">
                            <div>Количество тестируемых оценок:</div>
                            <div>` + request["rating_tasting_count"] + `</div>
                        </div>
                        <div class="admin__testing_block">
                            <div>Из них предсказано:</div>
                            <div>` + request["rating_recommendations_count"] + `</div>
                        </div>
                        <div class="admin__testing_block">
                            <div>Метрика MAE по корреляции Пирсона:</div>
                            <div>` + request["mae_metrics"] + `</div>
                        </div>
                        <div class="admin__testing_block">
                            <div>Метрика MAE по средним оценкам:</div>
                            <div>` + request["mae_metrics_compared"] + `</div>
                        </div>
                        <div class="admin__testing_block">
                            <div>Метрика MSE по корреляции Пирсона:</div>
                            <div>` + request["mse_metrics"] + `</div>
                        </div>
                        <div class="admin__testing_block">
                            <div>Метрика MSE по средним оценкам:</div>
                            <div>` + request["mse_metrics_compared"] + `</div>
                        </div>
                        <div class="admin__testing_block">
                            <div>Метрика RMSE по корреляции Пирсона:</div>
                            <div>` + request["rmse_metrics"] + `</div>
                        </div>
                        <div class="admin__testing_block">
                            <div>Метрика RMSE по средним оценкам:</div>
                            <div>` + request["rmse_metrics_compared"] + `</div>
                        </div>
                        `
                        area.innerHTML += `
                            <link rel="stylesheet" href="/static/styles/testing.css">
                        `
                    }
                    else {
                        area.innerHTML += `
                            <div class="admin__recomendation_placeholder">
                                Ошибка тестирования.
                            </div>
                            <style>
                                .admin__recomendation_placeholder {
                                    margin-top: 30px;
                                    font-size: 24px;
                                    color: gray;
                                }
                            </style>
                        `
                    }
                })

            })

        }
    });

    // -----------------------------------------------------------------------------

});