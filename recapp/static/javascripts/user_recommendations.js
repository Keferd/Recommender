let menu_user_recommendation_button = document.getElementById("admin__menu_user_recommendation");

menu_user_recommendation_button.addEventListener("click", function (e) {

    abortController.abort();
    const controller = new AbortController();
    abortController = controller;

    let area = document.getElementById('admin__main')
    
    area.innerHTML = `
        <div class="admin__main-container">
        <h1 class="admin__h1"> Рекомендации пользователю по корреляции Пирсона </h1>
        <div class="admin__content">
        <div class="admin__form">
            <div>
                <label for="user_recommendation_id">Id пользователя:</label>
                <input class="admin__input-number" type="number" min="1" id="user_recommendation_id">
            </div>
            <div>
                <label for="count_of_output">Сколько вывести рекомендованных книг:</label>
                <input class="admin__input-number" type="number" step="1" min="1" value="20" id="count_of_output">
            </div>
            <div>
            <input class="admin__input-button" type="button" value="Запрос" id="user_recommendation_button">
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

    let user_recommendation_button = document.getElementById("user_recommendation_button");

    user_recommendation_button.addEventListener("click", function (e) {

        abortController.abort();
        const controller = new AbortController();
        abortController = controller;
        
        let user_id = document.getElementById('user_recommendation_id').value;
        let count_of_output = document.getElementById('count_of_output').value

        let user_formdata = JSON.stringify({id: user_id,
                                            count_of_output: count_of_output});

        formparse = JSON.parse(user_formdata);

        let area = document.getElementById('admin__user-recommendations')
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

        if (formparse['id'] != "") {
            fetch("/api/create_prediction_Pearson",
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

                    let request = data['recommendations'];

                    console.log(typeof(request))
                    console.log(request)
                    
                    if (typeof(request) === 'object') {
                        if (request.length > 0) {
                            for (let id in request){
                                area.innerHTML += `
                                <div class="admin__book">
                                    <img src="` + request[id]['small_image_url'] + `" alt="">
                                    <div class="admin__book_inf">
                                    <div class="admin__book_names">
                                        <div class="admin__book_name_1">` + request[id]['title'] + `</div>
                                        <div class="admin__book_name_2">` + request[id]['original_title'] + `</div>
                                    </div>
                                    <div class="admin__book_other">
                                        <div class="admin__book_year">` + request[id]['original_publication_year'] + `</div>
                                        , 
                                        <div class="admin__book_author">` + request[id]['authors'] + `</div>
                                    </div>
                                    </div>
                                </div>
                                `
                            }
                            area.innerHTML += `
                                <link rel="stylesheet" href="/static/styles/user_recommendations.css">
                            `
                        }
                        else {
                            area.innerHTML += `
                                <div class="admin__recomendation_placeholder">
                                    Ошибка, слишком мало данных для получения рекомендаций. Попробуйте выбрать пользователя с большим количеством оценок.
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
                    }
                    else {
                        area.innerHTML += `
                            <div class="admin__recomendation_placeholder">
                                Ошибка, попробуйте ввести другие данные.
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