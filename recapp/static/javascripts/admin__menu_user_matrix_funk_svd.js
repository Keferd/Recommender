let menu_user_matrix_funk_svd_button = document.getElementById("admin__menu_user_matrix_funk_svd");

menu_user_matrix_funk_svd_button.addEventListener("click", function (e) {

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
                <label for="gradient_count">Количество итераций:</label>
                <input class="admin__input-number" type="number" min="1" value="20" id="gradient_count">
            </div>
            <div>
            <input class="admin__input-button" type="button" value="Запрос" id="matrix_funk_svd_button">
            </div>
        </div>
        <div class="admin__result">
            <h2>Результаты:</h2>
            <div class="admin__result-content" id="admin__user-recommendations">

            </div>
        </div>
        </div>
        </div>
        <link rel="stylesheet" href="/static/styles/user_recommendations_menu.css">
    `

    // -----------------------------------------------------------------------------

    let matrix_funk_svd_button = document.getElementById("matrix_funk_svd_button");

    matrix_funk_svd_button.addEventListener("click", function (e) {
        
        let factors = document.getElementById('factors').value;
        let learning_rate = document.getElementById('learning_rate').value;
        let regularization = document.getElementById('regularization').value;
        let gradient_count = document.getElementById('gradient_count').value;

        let user_formdata = JSON.stringify({factors: factors,
                                            learning_rate: learning_rate, 
                                            regularization: regularization,
                                            gradient_count: gradient_count});

        formparse = JSON.parse(user_formdata);

        if (formparse['factors'] != "" && 
            formparse['learning_rate'] != "" && 
            formparse['regularization'] != "" && 
            formparse['gradient_count'] != "") {
            fetch("/api/create_tables_funk_svd",
            {
                method: "POST",
                body: user_formdata,
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                response.json().then(function(data) {
                    

                    let area = document.getElementById('admin__user-recommendations')
                    area.innerHTML = ""

                    let request = data['rmse'];

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
                        count = 1
                        for (let id in request){
                            new_area +=`
                            <tr>
                                <td>` + count + `</td>
                                <td>` + request[id] + `</td>
                            </tr>
                            `;
                            count = count + 1
                        };

                        new_area += `
                            </tbody>
                            </table>
                            <link rel="stylesheet" href="/static/styles/user_recommendations.css">
                         `;
                        area.innerHTML += new_area
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
            let area = document.getElementById('admin__testing')
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