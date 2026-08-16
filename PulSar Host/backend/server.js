import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import helmet from "helmet";
import morgan from "morgan";
import rateLimit from "express-rate-limit";
import database from "./database/db.js";

dotenv.config();

const app = express();

const PORT = process.env.PORT || 3000;


// =====================
// Настройки
// =====================

app.use(cors());

app.use(express.json());

app.use(helmet());

app.use(morgan("dev"));

app.use(rateLimit({
    windowMs: 60 * 1000,
    max: 100
}));


// =====================
// Главная
// =====================

app.get("/", (req,res)=>{

    res.json({
        name:"PulSar-Host",
        version:"1.0.0",
        status:"online",
        message:"Игровой хостинг работает 🚀"
    });

});


// =====================
// Пользователи
// =====================


// Регистрация

app.post("/api/register", async(req,res)=>{

    try {

        const {
            username,
            password,
            email
        } = req.body;


        const user = await database.run(
            `
            INSERT INTO users
            (username,email,password)

            VALUES(?,?,?)
            `,
            [
                username,
                email,
                password
            ]
        );


        res.json({

            success:true,

            user_id:user.lastID

        });


    } catch(error){

        res.status(400).json({

            error:"Пользователь уже существует"

        });

    }

});



// Получить пользователей

app.get("/api/users", async(req,res)=>{

    const users = await database.all(
        "SELECT id,username,role,balance FROM users"
    );


    res.json(users);

});



// =====================
// Игровые серверы
// =====================


// Создать сервер

app.post("/api/servers", async(req,res)=>{


    const {
        user_id,
        name,
        game
    } = req.body;


    const server = await database.run(

        `
        INSERT INTO servers
        (user_id,name,game)

        VALUES(?,?,?)
        `,

        [
            user_id,
            name,
            game
        ]

    );


    res.json({

        success:true,

        server_id:server.lastID

    });


});



// Список серверов

app.get("/api/servers", async(req,res)=>{


    const servers = await database.all(

        "SELECT * FROM servers"

    );


    res.json(servers);


});



// Запуск сервера

app.post("/api/servers/:id/start",async(req,res)=>{


    await database.run(

        `
        UPDATE servers

        SET status='online'

        WHERE id=?

        `,

        [
            req.params.id
        ]

    );


    res.json({

        success:true,

        message:"Сервер запущен"

    });


});



// Остановка сервера

app.post("/api/servers/:id/stop",async(req,res)=>{


    await database.run(

        `
        UPDATE servers

        SET status='offline'

        WHERE id=?

        `,

        [
            req.params.id
        ]

    );


    res.json({

        success:true,

        message:"Сервер остановлен"

    });


});


// =====================
// Промокоды
// =====================


// Проверка промокода

app.post("/api/promo/check",async(req,res)=>{


    const {
        code
    } = req.body;



    const promo = await database.get(

        `
        SELECT *

        FROM promo_codes

        WHERE code=?

        `,

        [
            code
        ]

    );



    if(!promo){

        return res.json({

            valid:false

        });

    }



    res.json({

        valid:true,

        discount:promo.discount

    });



});



// Создание промокода (для админа)

app.post("/api/admin/promo",async(req,res)=>{


    const {
        code,
        discount,
        max_uses
    } = req.body;



    await database.run(

        `
        INSERT INTO promo_codes

        (code,discount,max_uses)

        VALUES(?,?,?)

        `,

        [
            code,
            discount,
            max_uses
        ]

    );


    res.json({

        success:true,

        message:"Промокод создан"

    });


});



// =====================
// Статус
// =====================

app.get("/api/status",(req,res)=>{


    res.json({

        hosting:"PulSar-Host",

        version:"1.0.0",

        online:true,

        uptime:process.uptime()

    });


});



// =====================
// Ошибки
// =====================

app.use((err,req,res,next)=>{


    console.log(err);


    res.status(500).json({

        error:"Ошибка сервера"

    });


});



// =====================
// Запуск
// =====================

app.listen(PORT,()=>{


    console.log(`
🌌 PulSar-Host v1.0

🚀 Сервер запущен
📡 Порт: ${PORT}

    `);


});
