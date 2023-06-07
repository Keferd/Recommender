let menu_user_recommendation_button = document.getElementById("admin__menu_user_recommendation");

menu_user_recommendation_button.addEventListener("click", function (e) {

    let area = document.getElementById('admin__main')
    
    area.innerHTML = `
        <div class="admin__main-container">
        <h1 class="admin__h1"> Рекомендации пользователю по id </h1>
        <div class="admin__content">
        <div class="admin__form">
            <div>
                <label for="user_id">Id пользователя:</label>
                <input class="admin__input-number" type="number" min="1" id="user_recommendation_id">
            </div>
            <div>
                <label for="count_rating">Минимальное количество оценок от пользователя:</label>
                <input class="admin__input-number" type="number" min="1" value="10" id="count_rating">
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

        let user_id = document.getElementById('user_recommendation_id').value;
        let count_rating = document.getElementById('count_rating').value;
        let number_of_crossings = document.getElementById('number_of_crossings').value;
        let correlation = document.getElementById('correlation').value;
        let normalization_number = document.getElementById('normalization_number').value
        let count_of_output = document.getElementById('count_of_output').value

        let user_formdata = JSON.stringify({id: user_id,
                                            count_rating: count_rating, 
                                            number_of_crossings: number_of_crossings,
                                            correlation: correlation,
                                            normalization_number: normalization_number,
                                            count_of_output: count_of_output});

        formparse = JSON.parse(user_formdata);

        if (formparse['id'] != "") {
            fetch("/api/create_prediction_Pearson",
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

                    let area = document.getElementById('admin__user-recommendations')
                    area.innerHTML = ""

                    let request = data['recommendations'];
                    if (request != "") {
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
                                Для пользователя id/` + formparse['id'] + ` нет рекомендаций.
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