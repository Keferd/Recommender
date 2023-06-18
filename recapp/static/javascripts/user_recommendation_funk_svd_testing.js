let menu_user_recommendation_funk_svd_testing = document.getElementById("admin__menu_user_recommendation_funk_svd_testing");

menu_user_recommendation_funk_svd_testing.addEventListener("click", function (e) {

    abortController.abort();
    const controller = new AbortController();
    abortController = controller;
    
    let area = document.getElementById('admin__main')
    
    area.innerHTML = `
        <div class="admin__main-container">
        <h1 class="admin__h1"> Тестирование рекомендаций по Funk SVD</h1>
        <div class="admin__content">
        <div class="admin__form">
            <div>
                <label for="factors">Количество факторов:</label>
                <input class="admin__input-number" type="number" min="1" value="20" id="factors">
            </div>
            <div>
                <label for="learning_rate">Скорость обучения:</label>
                <input class="admin__input-number" type="number" min="0" value="0.01" step="0.001" id="learning_rate">
            </div>
            <div>
                <label for="regularization">Регуляризация:</label>
                <input class="admin__input-number" type="number" min="0" value="0.01" step="0.001" id="regularization">
            </div>
            <div>
                <label for="gradient_count">Количество итераций:</label>
                <input class="admin__input-number" type="number" min="1" value="20" id="gradient_count">
            </div>
            <div>
                <label for="percentage_tested_ratings">Процент оценок пользователей для тестирования:</label>
                <input class="admin__input-number" type="number" step="0.01" max="1" min="0" value="0.25" id="percentage_tested_ratings">
            </div>

            <div>
            <input class="admin__input-button" type="button" value="Запрос" id="user_recommendation_funk_svd_testing">
            </div>
        </div>
        <div class="admin__result">
            <h2>Результаты:</h2>
            <div class="admin__result-content" id="admin__recommendation_funk_svd_testing">

            </div>
        </div>
        </div>
        </div>
        <link rel="stylesheet" href="/static/styles/user_recommendations_menu.css">
    `


    // -----------------------------------------------------------------------------

    let user_recommendation_funk_svd_testing_button = document.getElementById("user_recommendation_funk_svd_testing");

    user_recommendation_funk_svd_testing_button.addEventListener("click", function (e) {

        abortController.abort();
        const controller = new AbortController();
        abortController = controller;
        
        let factors = document.getElementById('factors').value;
        let learning_rate = document.getElementById('learning_rate').value;
        let regularization = document.getElementById('regularization').value;
        let gradient_count = document.getElementById('gradient_count').value;
        let percentage_tested_ratings = document.getElementById('percentage_tested_ratings').value;


        let user_formdata = JSON.stringify({factors: factors,
                                            learning_rate: learning_rate, 
                                            regularization: regularization,
                                            gradient_count: gradient_count,
                                            percentage_tested_ratings: percentage_tested_ratings});

        formparse = JSON.parse(user_formdata);

        let area = document.getElementById('admin__recommendation_funk_svd_testing')
        area.innerHTML = `
            <div class="admin__recomendation_placeholder">
                <img src="static/img/load_icon.png" alt="loading">
            </div>
            <style>
                .admin__recomendation_placeholder {
                    margin-top: 30px;
                    font-size: 24px;
                    color: gray;
                }

                .admin__recomendation_placeholder img {
                    width: 50px; 
                    height: 50px;
                    animation: move 0.5s infinite linear;
                }
                
                @keyframes move {
                    0% {
                    transform: rotate(0deg);
                    }
                    50% {
                    transform: rotate(180deg);
                    border-radius: 50%;
                    }
                    100% {
                    transform: rotate(360deg);
                    }
                }
            </style>
        `;

        if (formparse['factors'] != "" && 
            formparse['learning_rate'] != "" && 
            formparse['regularization'] != "" && 
            formparse['gradient_count'] != "" && 
            formparse['percentage_tested_ratings'] != "") {
            fetch("/api/testing_prediction_Funk_SVD",
            {
                method: "POST",
                body: user_formdata,
                headers: {
                    'Content-Type': 'application/json'
                },
                signal: controller.signal
            })
            .then(response => {
                response.json().then(function(data) {
                    area.innerHTML = ""

                    let request = data['testing'];
                    
                    if (request != "") {
                        area.innerHTML += `
                        <div class="admin__testing_block">
                            <div>Предсказано оценок:</div>
                            <div>` + request["rating_recommendations_count"] + `</div>
                        </div>
                        <div class="admin__testing_block">
                            <div>Метрика RMSE по средним оценкам:</div>
                            <div>` + request["rmse_metrics_compared"] + `</div>
                        </div>
                        `;

                        info = request["rmse"]

                        new_area = `
                            <table class="result_table">
                                <thead>
                                    <tr>
                                        <th>Итерация</th>
                                        <th>Обучающий RMSE</th>
                                        <th>Тестовый RMSE</th>
                                    </tr>
                                </thead>
                            <tbody>
                            `;

                        if (info != "") {
                            count = 1
                            for (let id in info){
                                new_area +=`
                                <tr>
                                    <td>` + count + `</td>
                                    <td>` + info[id]["init"] + `</td>
                                    <td>` + info[id]["test"] + `</td>
                                </tr>
                                `;
                                count = count + 1
                            };

                            new_area += `
                                </tbody>
                                </table>
                                <style>
                                    .result_table {
                                        border-spacing: 10px;
                                    }
                                </style>
                                <link rel="stylesheet" href="/static/styles/user_recommendations.css">
                            `;
                            area.innerHTML += new_area
                        }


                        area.innerHTML += `
                            <link rel="stylesheet" href="/static/styles/testing.css">
                        `;
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
                        `;
                    }
                })

            })

        }
        else {
            area.innerHTML = `
                            <div class="admin__recomendation_placeholder">
                                Заполните все поля.
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
    });

    // -----------------------------------------------------------------------------

});