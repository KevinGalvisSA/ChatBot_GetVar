import "reflect-metadata";
import { DataSource } from "typeorm";
import { Message } from "../domain/entities/message_entity";  // Asegúrate de importar tus entidades aquí

import * as dotenv from "dotenv";
dotenv.config();

export const AppDataSource = new DataSource({
    type: "postgres",                // Usa PostgreSQL
    host: process.env.DB_HOST || "localhost",  // Puedes configurar la variable DB_HOST en .env
    port: parseInt(process.env.DB_PORT || "5432"), // El puerto predeterminado de PostgreSQL
    username: process.env.DB_USER || "postgres", // Usuario de la base de datos
    password: process.env.DB_PASSWORD || "", // Contraseña de la base de datos
    database: process.env.DB_NAME || "chatbot_db", // Nombre de la base de datos
    synchronize: true,  // Asegúrate de cambiarlo a `false` en producción
    logging: true,      // Habilitar logs de las consultas
    entities: [Message], // Agrega todas las entidades que has creado
    migrations: [],  // Aquí puedes agregar las migraciones si las estás usando
    subscribers: [],
});

