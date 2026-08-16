// =======================================
// 🌌 PulSar-Host v1.0
// Login System
// =======================================


const API_URL = "http://localhost:3000";

let loginAttempts = 0;
let isLoading = false;



// =======================================
// NOTIFICATION
// =======================================


function showMessage(text, type="error"){


    const message =
    document.getElementById(
        "message"
    );


    message.innerHTML = text;


    message.className =
    "message " + type;


}






// =======================================
// LOGIN
// =======================================


async function login(){


    if(isLoading)
        return;



    const username =
    document.getElementById(
        "username"
    ).value.trim();



    const password =
    document.getElementById(
        "password"
    ).value.trim();



    if(!username || !password){


        showMessage(
            "❌ Заполните все поля"
        );


        return;

    }




    if(loginAttempts >= 5){


        showMessage(
            "⛔ Слишком много попыток. Подождите"
        );


        return;

    }



    isLoading = true;



    const button =
    document.querySelector(
        "button"
    );



    button.disabled = true;

    button.innerHTML =
    "⏳ Проверка...";





    try{


        const response =
        await fetch(

            API_URL + "/api/login",

            {

            method:"POST",

            headers:{

                "Content-Type":
                "application/json"

            },


            body:JSON.stringify({

                username,

                password

            })

            }

        );



        const data =
        await response.json();





        if(!response.ok || !data.success){


            loginAttempts++;


            showMessage(
                "❌ Неверный логин или пароль"
            );


            return;

        }






        // Сохраняем пользователя


        localStorage.setItem(

            "pulsar_user",

            JSON.stringify(
                data.user
            )

        );



        localStorage.setItem(

            "pulsar_token",

            data.token || ""

        );





        showMessage(

            "✅ Вход выполнен. Загрузка..."

            ,"success"

        );





        setTimeout(()=>{


            if(data.user.role === "admin"){


                window.location.href =
                "admin.html";


            }

            else{


                window.location.href =
                "index.html";


            }


        },1000);







    }

    catch(error){


        console.error(error);



        showMessage(

            "⚠️ Сервер недоступен"

        );


    }



    finally{


        isLoading=false;


        button.disabled=false;


        button.innerHTML =
        "🚀 Войти в панель";


    }



}





// =======================================
// AUTO LOGIN
// =======================================


window.onload = ()=>{


    const user =
    localStorage.getItem(
        "pulsar_user"
    );



    if(user){


        console.log(
            "Пользователь уже вошёл"
        );


    }


};
