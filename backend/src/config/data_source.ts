import "reflect-metadata";
import { DataSource } from "typeorm";
import { Message } from "../domain/entities/message_entity";  // Asegúrate de importar tus entidades aquí
import { Chat } from "../domain/entities/chat_entity";
import { Customer } from "../domain/entities/customer_entity";
import { MessageStorage } from "../domain/entities/messageStorage_entity";

import * as dotenv from "dotenv";
dotenv.config();

export const AppDataSource = new DataSource({
    type: "mysql",
    driver: require("mysql2"),  // Usar mysql2
    host: process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT || "3306"),
    username: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    synchronize: false,
    logging: true,
    entities: [Message, Chat, Customer, MessageStorage],
    migrations: [],
    subscribers: [],
});