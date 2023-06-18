let menu_user_matrix_funk_svd_button = document.getElementById("admin__menu_user_matrix_funk_svd");

menu_user_matrix_funk_svd_button.addEventListener("click", function (e) {

    abortController.abort();
    const controller = new AbortController();
    abortController = controller;
    
    let area = document.getElementById('admin__main')

    area.innerHTML = `
        <div class="admin__main-container">
        <h1 class="admin__h1"> Генерация матриц Funk SVD </h1>
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
            <input class="admin__input-button" type="button" value="Запрос" id="matrix_funk_svd_button">
            </div>
        </div>
        <div class="admin__result">
            <h2>Результаты:</h2>
            <div class="admin__result-content" id="admin__user_matrix_funk_svd">

            </div>
        </div>
        </div>
        </div>
        <link rel="stylesheet" href="/static/styles/user_recommendations_menu.css">
    `

    // -----------------------------------------------------------------------------

    let matrix_funk_svd_button = document.getElementById("matrix_funk_svd_button");

    matrix_funk_svd_button.addEventListener("click", function (e) {
        
        abortController.abort();
        const controller = new AbortController();
        abortController = controller;
    
        let factors = document.getElementById('factors').value;
        let learning_rate = document.getElementById('learning_rate').value;
        let regularization = document.getElementById('regularization').value;

        let user_formdata = JSON.stringify({factors: factors,
                                            learning_rate: learning_rate, 
                                            regularization: regularization});

        formparse = JSON.parse(user_formdata);

        let area = document.getElementById('admin__user_matrix_funk_svd')
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
        `

        if (formparse['factors'] != "" && 
            formparse['learning_rate'] != "" && 
            formparse['regularization'] != "") {
            fetch("/api/create_tables_funk_svd",
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

                    let request = data['Генерация матриц'];
                    console.log(request)

                    new_area = `
                        <table>
                            <thead>
                                <tr>
                                    <th>Итерация</th>
                                    <th>RMSE</th>
                                </tr>
                            </thead>
                        <tbody>
                        `;

                    if (request != "") {
                        area.innerHTML += `
                            <div class="admin__recomendation_placeholder">
                                Матрицы факторов сгенерированы.
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
                    else {
                        area.innerHTML += `
                            <div class="admin__recomendation_placeholder">
                                Ошибка работы.
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

    })

    // -----------------------------------------------------------------------------

});