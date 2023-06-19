let menu_user_table = document.getElementById("admin__menu_user_table");

menu_user_table.addEventListener("click", function (e) {

    abortController.abort();
    const controller = new AbortController();
    abortController = controller;

    let area = document.getElementById('admin__main')

    area.innerHTML = `
        <div class="admin__main-container">
        <h1 class="admin__h1"> Таблица пользователей </h1>
        <div class="admin__content">
        <div class="admin__form">
            <div>
                <label for="count_of_output">Минимальное число оценок:</label>
                <input class="admin__input-number" type="number" step="1" min="1" value="20" id="count_rating">
            </div>
            <div>
            <input class="admin__input-button" type="button" value="Запрос" id="user_table_button">
            </div>
        </div>
        <div class="admin__result">
            <h2>Результаты:</h2>
            <div class="admin__result-content" id="admin__result_user_table">

            </div>
        </div>
        </div>
        </div>
        <link rel="stylesheet" href="/static/styles/user_recommendations_menu.css">
    `

    // -----------------------------------------------------------------------------

    let user_table_button = document.getElementById("user_table_button");

    user_table_button.addEventListener("click", function (e) { 
        
        abortController.abort();
        const controller = new AbortController();
        abortController = controller;

        let count_rating = document.getElementById('count_rating').value;

        let user_formdata = JSON.stringify({count_rating: count_rating});

        formparse = JSON.parse(user_formdata);

        console.log(formparse)

        let area = document.getElementById('admin__result_user_table')
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

        if (formparse['count_rating'] != "") {
            fetch("/api/users_by_filter",
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

                    let request = data['table'];
                    let error = data['Ошибка']
                    
                    if (error != 'Ошибка') {
                        new_area = `
                            <table class="result_table">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Средняя оценка</th>
                                        <th>Количество оценок</th>
                                    </tr>
                                </thead>
                            <tbody>
                            `;

                            for (let id in request){
                                new_area +=`
                                <tr>
                                    <td>` + request[id]["id"] + `</td>
                                    <td>` + request[id]["av"] + `</td>
                                    <td>` + request[id]["co"] + `</td>
                                </tr>
                                `;
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
                    else {
                        area.innerHTML += `
                            <div class="admin__recomendation_placeholder">
                                Ошибка, попробуйте понизить минимальное число оценок
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

    });

    // -----------------------------------------------------------------------------

});