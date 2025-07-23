-- Tabla que almacena mensajes sin procesar o históricos
CREATE TABLE IF NOT EXISTS messageStorage (
    `id` MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_customer` MEDIUMINT UNSIGNED NOT NULL,
    `id_session` BIGINT NOT NULL,
    `message` TEXT NOT NULL,
    `message_type` VARCHAR(50) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

-- Tabla principal de clientes
CREATE TABLE `customer` (
    `id` MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, -- ID único del cliente
    `name` VARCHAR(100) NOT NULL,     -- Nombre del cliente
    `phone_number` BIGINT NOT NULL,          -- Número de teléfono del cliente (usado también como session_id en messageStorages)
    `createdBy` MEDIUMINT NULL,       -- ID del usuario que creó este cliente (nullable)
    `updatedBy` MEDIUMINT NULL,       -- ID del usuario que actualizó este cliente (nullable)
    `createdAt` TIMESTAMP NOT NULL,   -- Fecha y hora de creación del registro
    `updatedAt` TIMESTAMP NOT NULL    -- Fecha y hora de la última actualización del registro
);

-- Tabla que almacena los mensajes dentro de un chat
CREATE TABLE `messages` (
    `id` MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, -- ID único del mensaje
    `type` TINYINT NOT NULL,          -- Tipo de mensaje (0 = entrante, 1 = saliente, etc.)
    `content` TEXT NOT NULL,          -- Contenido del mensaje
    `chatId` MEDIUMINT NOT NULL,      -- ID del chat al que pertenece este mensaje
    `createdBy` MEDIUMINT NULL,       -- ID del usuario que creó este mensaje (nullable)
    `updatedBy` MEDIUMINT NULL,       -- ID del usuario que actualizó este mensaje (nullable)
    `createdAt` TIMESTAMP NOT NULL,   -- Fecha y hora de creación del mensaje
    `updatedAt` TIMESTAMP NOT NULL    -- Fecha y hora de última modificación del mensaje
);

-- Tabla que representa una conversación entre el cliente y el sistema
CREATE TABLE `chat` (
    `id` MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, -- ID único del chat
    `id_customer` MEDIUMINT NOT NULL, -- ID del cliente asociado a este chat
    `last_connection` DATETIME NOT NULL, -- Última conexión del cliente al chat
    `createdBy` MEDIUMINT NULL,      -- ID del usuario que creó este chat (nullable)
    `updatedBy` MEDIUMINT NULL,      -- ID del usuario que actualizó este chat (nullable)
    `createdAt` TIMESTAMP NOT NULL,  -- Fecha de creación del chat
    `updatedAt` TIMESTAMP NOT NULL,   -- Fecha de última actualización del chat
    `state`  TINYINT NOT NULL -- Estado de la conversacion (0 = inactivo, 1 = activo)
);

-- Relaciones (Foreign Keys)

-- Cada mensaje apunta al chat al que pertenece
ALTER TABLE `messages`
ADD CONSTRAINT `messages_chatid_foreign`
FOREIGN KEY (`chatId`) REFERENCES `chat`(`id`);

-- messageStorages.session_id se relaciona con el teléfono del cliente
ALTER TABLE `messageStorages`
ADD CONSTRAINT `messagestorages_session_id_foreign`
FOREIGN KEY (`session_id`) REFERENCES `customer`(`phone_number`);

-- messageStorages.id_customer se relaciona con el ID del cliente
ALTER TABLE `messageStorages`
ADD CONSTRAINT `messagestorages_id_customer_foreign`
FOREIGN KEY (`id_customer`) REFERENCES `customer`(`id`);

-- chats.id_customer se relaciona con el ID del cliente
ALTER TABLE `chats`
ADD CONSTRAINT `chats_id_customer_foreign`
FOREIGN KEY (`id_customer`) REFERENCES `customer`(`id`);
