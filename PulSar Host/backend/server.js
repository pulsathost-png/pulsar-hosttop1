import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import helmet from "helmet";
import morgan from "morgan";
import rateLimit from "express-rate-limit";
import { v4 as uuid } from "uuid";

dotenv.config();

const app = express();

const PORT = process.env.PORT || 3000;

// =====================
// Настройки безопасности
// =====================

app.use(helmet());

app.use(cors({
    origin: "*"
}));

app.use(express.json({
    limit: "2mb"
}));

app.use(morgan("combined"));

// Защита от большого количества запросов
app.use(rateLimit({
    windowMs: 60 * 1000,
    max: 100,
    message: {
        error: "Слишком много запросов"
    }
}));


// =====================
// Данные (временно)
// Потом заменим на БД
// =====================

let servers = [];

let promoCodes = [
    {
        code: "PULSAR35",
        discount: 35,
        active: true
    }
];


// =====================
// Главная
// =====================

app.get("/", (req,res)=>{

    res.json({
        project: "PulSar-Host",
        version: "1.0.0",
        status: "online",
        message: "Добро пожаловать в игровой хостинг 🚀"
    });

});


// =====================
// Серверы
// =====================


// Получить все серверы

app.get("/api/servers",(req,res)=>{

    res.json({
        count: servers.length,
        servers
    });

});


// Создать сервер

app.post("/api/servers",(req,res)=>{

    const {name,game} = req.body;


    const server = {

        id: uuid(),

        name: name || "New Server",

        game: game || "Unknown",

        status:"offline",

        cpu:0,

        ram:0,

        players:0,

        created:new Date()

    };


    servers.push(server);


    res.json({
        success:true,
        server
    });


});


// Запуск сервера

app.post("/api/servers/:id/start",(req,res)=>{


    const server =
    servers.find(
        s=>s.id === req.params.id
    );


    if(!server){

        return res.status(404).json({
            error:"Сервер не найден"
        });

    }


    server.status="online";


    res.json({
        success:true,
        message:"Сервер запущен",
        server
    });


});


// Остановка сервера

app.post("/api/servers/:id/stop",(req,res)=>{


    const server =
    servers.find(
        s=>s.id === req.params.id
    );


    if(!server){

        return res.status(404).json({
            error:"Сервер не найден"
        });

    }


    server.status="offline";


    res.json({
        success:true,
        message:"Сервер остановлен",
        server
    });


});


// =====================
// Промокоды
// =====================


app.post("/api/promo/check",(req,res)=>{


    const {code}=req.body;


    const promo =
    promoCodes.find(
        p=>p.code === code
    );


    if(!promo || !promo.active){

        return res.json({
            valid:false
        });

    }


    res.json({

        valid:true,

        discount:promo.discount

    });


});


// =====================
// Статус системы
// =====================


app.get("/api/status",(req,res)=>{


    res.json({

        hosting:"PulSar-Host",

        version:"1.0.0",

        status:"online",

        servers:servers.length,

        uptime:process.uptime()

    });


});


// =====================
// Ошибки
// =====================

app.use((err,req,res,next)=>{


    console.error(err);


    res.status(500).json({

        error:"Внутренняя ошибка сервера"

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
