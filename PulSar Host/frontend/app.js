// =====================================
// PulSar-Host v1.0
// Frontend Controller
// =====================================


const API_URL = "http://localhost:3000";


// ===============================
// API запросы
// ===============================


async function apiRequest(endpoint, options = {}) {

    try {

        const response = await fetch(
            API_URL + endpoint,
            {
                headers:{
                    "Content-Type":"application/json"
                },
                ...options
            }
        );


        const data = await response.json();


        if(!response.ok){

            throw new Error(
                data.error || "Ошибка запроса"
            );

        }


        return data;


    } catch(error){

        console.error(
            "API Error:",
            error
        );


        showMessage(
            error.message,
            "error"
        );


        return null;

    }

}




// ===============================
// Уведомления
// ===============================


function showMessage(text,type="success"){


    let box =
    document.createElement("div");


    box.className =
    "notification " + type;


    box.innerText = text;


    document.body.appendChild(box);



    setTimeout(()=>{

        box.remove();

    },3000);


}





// ===============================
// Статус хостинга
// ===============================


async function checkStatus(){


    const data =
    await apiRequest(
        "/api/status"
    );



    if(!data)
        return;



    document.getElementById(
        "status"
    ).innerHTML =
    "🟢 Онлайн";



    document.getElementById(
        "serverCount"
    ).innerHTML =
    data.servers;


}





// ===============================
// Серверы
// ===============================


async function loadServers(){


    const data =
    await apiRequest(
        "/api/servers"
    );



    if(!data)
        return;



    const servers =
    document.getElementById(
        "servers"
    );



    servers.innerHTML="";



    if(data.length === 0){

        servers.innerHTML =
        "Нет созданных серверов";

        return;

    }



    data.forEach(server=>{


        servers.innerHTML += `

        <div class="card">


        <h3>
        🎮 ${server.name}
        </h3>


        <p>
        Игра:
        ${server.game}
        </p>


        <p>
        Статус:
        ${server.status}
        </p>


        <button onclick="
        startServer('${server.id}')
        ">
        ▶ Запустить
        </button>


        <button onclick="
        stopServer('${server.id}')
        ">
        ⏹ Остановить
        </button>


        </div>

        `;


    });


}





// ===============================
// Создание сервера
// ===============================


async function createServer(){


    const name =
    document.getElementById(
        "serverName"
    ).value.trim();



    const game =
    document.getElementById(
        "game"
    ).value.trim();



    if(!name || !game){

        showMessage(
            "Заполни все поля",
            "error"
        );

        return;

    }




    const result =
    await apiRequest(
        "/api/servers",
        {

        method:"POST",

        body:JSON.stringify({

            user_id:1,

            name,

            game

        })

        }
    );



    if(result){


        showMessage(
            "Сервер создан 🚀"
        );


        loadServers();


    }


}






// ===============================
// Запуск сервера
// ===============================


async function startServer(id){


    await apiRequest(
        `/api/servers/${id}/start`,
        {
            method:"POST"
        }
    );


    showMessage(
        "Сервер запускается"
    );


    loadServers();


}






// ===============================
// Остановка сервера
// ===============================


async function stopServer(id){


    await apiRequest(
        `/api/servers/${id}/stop`,
        {
            method:"POST"
        }
    );


    showMessage(
        "Сервер остановлен"
    );


    loadServers();


}






// ===============================
// Промокоды
// ===============================


async function checkPromo(){


    const code =
    document.getElementById(
        "promo"
    ).value.trim();



    if(!code){

        showMessage(
            "Введите промокод",
            "error"
        );

        return;

    }



    const data =
    await apiRequest(
        "/api/promo/check",
        {

        method:"POST",

        body:JSON.stringify({

            code

        })

        }
    );



    const result =
    document.getElementById(
        "promoResult"
    );



    if(data.valid){


        result.innerHTML =
        `✅ Скидка ${data.discount}%`;

    }

    else{


        result.innerHTML =
        "❌ Промокод недействителен";


    }


}






// ===============================
// Запуск панели
// ===============================


window.onload = ()=>{


    checkStatus();

    loadServers();


};
