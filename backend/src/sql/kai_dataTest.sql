-- Insertar clientes de prueba
INSERT INTO `customers` (`id`, `name`, `phone`, `createdBy`, `updatedBy`, `createdAt`, `updatedAt`) VALUES
(1, 'Laura Gómez',     3011234567, NULL, NULL, NOW(), NOW()),
(2, 'Carlos Pérez',    3029876543, NULL, NULL, NOW(), NOW()),
(3, 'Ana Martínez',    3035554321, NULL, NULL, NOW(), NOW()),
(4, 'María Torres',    3041122334, NULL, NULL, NOW(), NOW()),
(5, 'José Ramírez',    3059988776, NULL, NULL, NOW(), NOW()),
(6, 'Paula López',     3063344556, NULL, NULL, NOW(), NOW()),
(7, 'Luis Herrera',    3077766554, NULL, NULL, NOW(), NOW()),
(8, 'Mónica Díaz',     3084455667, NULL, NULL, NOW(), NOW()),
(9, 'Juan Mejía',      3091122443, NULL, NULL, NOW(), NOW()),
(10, 'Daniela Castro', 3106655443, NULL, NULL, NOW(), NOW()),
(11, 'Felipe Rojas',   3117788990, NULL, NULL, NOW(), NOW()),
(12, 'Camila Núñez',   3123344778, NULL, NULL, NOW(), NOW()),
(13, 'Esteban León',   3135566887, NULL, NULL, NOW(), NOW()),
(14, 'Sara Moreno',    3142233110, NULL, NULL, NOW(), NOW()),
(15, 'David Ortiz',    3159090808, NULL, NULL, NOW(), NOW());

-- Insertar chats de prueba (cada uno ligado a un cliente)
INSERT INTO `chats` (`id`, `customerId`, `lastConnection`, `createdBy`, `updatedBy`, `createdAt`, `updatedAt`) VALUES
(1, 1,  '2025-07-15 08:00:00', NULL, NULL, NOW(), NOW()),
(2, 2,  '2025-07-14 15:30:00', NULL, NULL, NOW(), NOW()),
(3, 3,  '2025-07-13 18:45:00', NULL, NULL, NOW(), NOW()),
(4, 4,  '2025-07-15 09:00:00', NULL, NULL, NOW(), NOW()),
(5, 5,  '2025-07-10 13:15:00', NULL, NULL, NOW(), NOW()),
(6, 6,  '2025-07-15 11:00:00', NULL, NULL, NOW(), NOW()),
(7, 7,  '2025-07-11 10:30:00', NULL, NULL, NOW(), NOW()),
(8, 8,  '2025-07-12 08:45:00', NULL, NULL, NOW(), NOW()),
(9, 9,  '2025-07-13 17:10:00', NULL, NULL, NOW(), NOW()),
(10, 10,'2025-07-15 07:50:00', NULL, NULL, NOW(), NOW()),
(11, 11,'2025-07-14 09:45:00', NULL, NULL, NOW(), NOW()),
(12, 12,'2025-07-13 19:30:00', NULL, NULL, NOW(), NOW()),
(13, 13,'2025-07-12 14:20:00', NULL, NULL, NOW(), NOW()),
(14, 14,'2025-07-11 11:05:00', NULL, NULL, NOW(), NOW()),
(15, 15,'2025-07-10 16:40:00', NULL, NULL, NOW(), NOW());

-- Insertar mensajes de prueba (tipo 0 = entrante, tipo 1 = saliente)
INSERT INTO `messages` (`id`, `type`, `content`, `chatId`, `createdBy`, `updatedBy`, `createdAt`, `updatedAt`) VALUES
(1, 0, 'Hola, ¿me pueden ayudar?', 1, NULL, NULL, NOW(), NOW()),
(2, 1, '¡Claro! ¿En qué necesitas ayuda?', 1, NULL, NULL, NOW(), NOW()),
(3, 0, 'No encuentro mi pedido', 2, NULL, NULL, NOW(), NOW()),
(4, 1, 'Déjame revisar el estado del pedido', 2, NULL, NULL, NOW(), NOW()),
(5, 0, 'Quiero cambiar mi dirección', 3, NULL, NULL, NOW(), NOW()),
(6, 1, '¿Cuál es la nueva dirección?', 3, NULL, NULL, NOW(), NOW()),
(7, 0, '¿Tienen productos nuevos?', 4, NULL, NULL, NOW(), NOW()),
(8, 1, 'Sí, acabamos de añadir nuevos artículos', 4, NULL, NULL, NOW(), NOW()),
(9, 0, '¿Cómo aplico un cupón?', 5, NULL, NULL, NOW(), NOW()),
(10,1, 'Solo debes ingresarlo en el carrito', 5, NULL, NULL, NOW(), NOW()),
(11,0, 'Gracias por su ayuda', 6, NULL, NULL, NOW(), NOW()),
(12,1, 'Con gusto, estamos para servirte', 6, NULL, NULL, NOW(), NOW()),
(13,0, '¿Puedo pagar con Nequi?', 7, NULL, NULL, NOW(), NOW()),
(14,1, 'Sí, aceptamos ese medio de pago', 7, NULL, NULL, NOW(), NOW()),
(15,0, '¿Cuánto demora el envío?', 8, NULL, NULL, NOW(), NOW());

-- Insertar mensajes almacenados (historial o log)
INSERT INTO `messageStorages` (`id`, `sessionId`, `message`, `customerId`) VALUES
(1, 3011234567, 'Histórico: Hola, ¿me pueden ayudar?', 1),
(2, 3029876543, 'Histórico: No encuentro mi pedido', 2),
(3, 3035554321, 'Histórico: Quiero cambiar mi dirección', 3),
(4, 3041122334, 'Histórico: ¿Tienen productos nuevos?', 4),
(5, 3059988776, 'Histórico: ¿Cómo aplico un cupón?', 5),
(6, 3063344556, 'Histórico: Gracias por su ayuda', 6),
(7, 3077766554, 'Histórico: ¿Puedo pagar con Nequi?', 7),
(8, 3084455667, 'Histórico: ¿Cuánto demora el envío?', 8),
(9, 3091122443, 'Histórico: ¿Dónde está mi factura?', 9),
(10,3106655443, 'Histórico: ¿Tienen servicio express?', 10),
(11,3117788990, 'Histórico: Quiero cancelar mi compra', 11),
(12,3123344778, 'Histórico: ¿Tienen soporte técnico?', 12),
(13,3135566887, 'Histórico: Necesito ayuda con el pago', 13),
(14,3142233110, 'Histórico: ¿Cuál es el tiempo de entrega?', 14),
(15,3159090808, 'Histórico: ¿Dónde veo el historial de compras?', 15);
