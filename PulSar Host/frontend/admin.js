// =======================================
// 🌌 PulSar-Host v1.0
// Admin Control System
// =======================================


const API_URL = "http://localhost:3000";

let adminData = {
    servers: [],
    users: []
};



// =======================================
// API CLIENT
// =======================================


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
                data.error || "Ошибка сервера"
            );

        }


        return data;


    } catch(error){


        console.error(error);


        notify(
            "❌ " + error.message,
            "error"
        );


        return null;

    }

}



// =======================================
// NOTIFICATIONS
// =======================================


function notify(text,type="success"){


    let notification =
    document.createElement("div");


    notification.className =
    "notification " + type;


    notification.innerHTML =
    text;


    document.body.appendChild(
        notification
    );



    setTimeout(()=>{

        notification.remove();

    },3500);


}




// =======================================
// CREATE PROMO
// =======================================


async function createPromo(){


    const code =
    document.getElementById(
        "promoCode"
    ).value.trim();



    const discount =
    Number(
        document.getElementById(
            "discount"
        ).value
    );



    const maxUses =
    Number(
        document.getElementById(
            "maxUses"
        ).value
    );



    if(!code || !discount){


        notify(
            "Введите данные промокода",
            "error"
        );


        return;

    }



    const result =
    await apiRequest(
        "/api/admin/promo",
        {

            method:"POST",

            body:JSON.stringify({

                code,

                discount,

                max_uses:maxUses || 100

            })

        }
    );



    if(result){


        notify(
            "🎁 Промокод создан"
        );


        document.getElementById(
            "promoCode"
        ).value="";


    }


}





// =======================================
// SERVERS
// =======================================


async function loadAdminServers(){


    const servers =
    await apiRequest(
        "/api/servers"
    );


    if(!servers)
        return;



    adminData.servers =
    servers;



    const box =
    document.getElementById(
        "adminServers"
    );



    box.innerHTML="";



    if(servers.length===0){


        box.innerHTML =
        "Нет игровых серверов";


        return;

    }




    servers.forEach(server=>{


        box.innerHTML += `


        <div class="card">


        <h3>
        🎮 ${server.name}
        </h3>


        <p>
        Игра: ${server.game}
        </p>


        <p>
        Статус:
        ${server.status}
        </p>


        <p>
        ID:
        ${server.id}
        </p>


        <button onclick="
        adminStart('${server.id}')
        ">
        ▶ Запустить
        </button>


        <button onclick="
        adminStop('${server.id}')
        ">
        ⏹ Остановить
        </button>


        </div>


        `;


    });


}





async function adminStart(id){


    await apiRequest(

        `/api/servers/${id}/start`,

        {
            method:"POST"
        }

    );


    notify(
        "🚀 Сервер запущен"
    );


    loadAdminServers();


}





async function adminStop(id){


    await apiRequest(

        `/api/servers/${id}/stop`,

        {
            method:"POST"
        }

    );


    notify(
        "⛔ Сервер остановлен"
    );


    loadAdminServers();


}





// =======================================
// USERS
// =======================================


async function loadUsers(){


    const users =
    await apiRequest(
        "/api/users"
    );


    if(!users)
        return;



    adminData.users =
    users;



    const box =
    document.getElementById(
        "users"
    );



    box.innerHTML="";



    users.forEach(user=>{


        box.innerHTML += `


        <div class="card">


        👤 ${user.username}

        <br>

        🛡 Роль:
        ${user.role}


        </div>


        `;


    });



    document.getElementById(
        "totalUsers"
    ).innerHTML =
    users.length;


}





// =======================================
// STATS
// =======================================


async function loadStats(){


    document.getElementById(
        "totalServers"
    ).innerHTML =
    adminData.servers.length;



}



// =======================================
// AUTO UPDATE
// =======================================


function startAutoRefresh(){


    setInterval(()=>{


        loadAdminServers();

        loadUsers();


    },30000);


}





// =================================
